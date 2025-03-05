from flask import Blueprint, request, jsonify
from flask_mail import Message
from models import User
from extensions import mail, redis_client, db
import random
import hashlib

# 登录/注册/忘记密码蓝图
bp_login = Blueprint('login', __name__, url_prefix='/')

# 加密密码的函数 - 使用与前端相同的方法 (SHA-256)
def encrypt_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 验证码验证函数
def verify_code(user_mail, verification_code):
    """
    验证用户提供的验证码是否正确
    
    Args:
        user_mail: 用户邮箱
        verification_code: 用户提供的验证码
        
    Returns:
        dict: 包含验证结果的字典, 成功返回None, 失败返回错误信息
    """
    # 从Redis中获取验证码（只能在后端验证）
    stored_code = redis_client.get(user_mail)
    
    # 判断验证码是否存在
    if not stored_code:
        return {'code': 400, 'message': '验证码已过期，请重新获取'}
    
    # 判断验证码是否正确 - 根据stored_code类型做适当处理
    if isinstance(stored_code, bytes):
        # 如果是bytes类型，需要解码
        if verification_code != stored_code.decode():
            return {'code': 400, 'message': '验证码错误'}
    else:
        # 如果已经是字符串类型，直接比较
        if verification_code != stored_code:
            return {'code': 400, 'message': '验证码错误'}
    
    # 验证通过
    return None

# 发送邮箱验证码
@bp_login.route('/send_email/', methods=['POST'])
def send_email():
    # 获取请求参数
    user_mail = request.form.get('user_mail')
    
    # 参数验证（必要的后端验证）
    if not user_mail:
        return jsonify({'code': 400, 'message': '邮箱不能为空'})
    
    try:
        # 检查redis中是否已存在该邮箱的验证码，如果存在则删除
        if redis_client.exists(user_mail):
            redis_client.delete(user_mail)
            
        # 生成6位随机验证码
        verification_code = ''.join(str(random.randint(0, 9)) for _ in range(6))
        
        # 发送邮件
        message = Message(
            subject='验证码', 
            recipients=[user_mail], 
            body=f'[月锦鲤] 验证码为: {verification_code}, 有效期为10分钟, 请勿泄露。'
        )
        mail.send(message)
        
        # 将验证码存储到redis
        redis_client.set(user_mail, verification_code, ex=600)
        
        return jsonify({'code': 200, 'message': '验证码发送成功'})
    except Exception as e:
        return jsonify({'code': 500, 'message': f'验证码发送失败: {str(e)}'})

# 注册
@bp_login.route('/register/', methods=['POST'])
def register():
    # 获取请求参数
    user_mail = request.form.get('user_mail')
    user_password = request.form.get('user_password')  # 前端已加密
    verification_code = request.form.get('verification_code')
    
    # 参数验证（必要的后端验证）
    if not all([user_mail, user_password, verification_code]):
        return jsonify({'code': 400, 'message': '请填写所有必填项'})
    
    # 判断用户是否存在（只能在后端验证）
    user = User.query.filter_by(email=user_mail).first()
    if user:
        return jsonify({'code': 400, 'message': '该邮箱已被注册'})
    
    # 验证验证码
    verify_result = verify_code(user_mail, verification_code)
    if verify_result:
        return jsonify(verify_result)
    
    # 创建新用户
    try:
        new_user = User(
            email=user_mail,
            password=user_password,  # 已加密的密码
            user_type_id=2  # 普通用户
        )
        
        # 添加用户到数据库
        db.session.add(new_user)
        db.session.commit()
        # 刷新数据库
        db.session.refresh(new_user)
        # 注册成功后删除Redis中的验证码
        redis_client.delete(user_mail)
        
        return jsonify({'code': 200, 'message': '注册成功'})
    
    except Exception as e:
        # 回滚事务
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'注册失败: {str(e)}'})

# 登录
@bp_login.route('/login/', methods=['POST'])
def login():
    # 获取请求参数
    user_mail = request.form.get('user_mail')
    user_password = request.form.get('user_password')  # 前端已加密
    
    # 参数验证
    if not all([user_mail, user_password]):
        return jsonify({'code': 400, 'message': '请填写邮箱和密码'})
    
    # 查询用户（后端业务逻辑验证）
    user = User.query.filter_by(email=user_mail).first()
    
    # 判断用户是否存在
    if not user:
        return jsonify({'code': 400, 'message': '用户不存在'})
    
    # 如果是管理员用户,需要对数据库中的密码进行额外加密以匹配前端加密
    if user.user_type_id == 1:
        # 使用SHA256进行加密,与前端保持一致
        user.password = encrypt_password(user.password)
    
    # 判断密码是否正确
    if user.password != user_password:
        return jsonify({'code': 400, 'message': '密码错误'})
    
    # 登录成功
    return jsonify({
        'code': 200, 
        'message': '登录成功', 
        'user_id': user.id,
        'user_mail': user.email,
        'user_type': user.user_type_id,
    })

# 重置密码
@bp_login.route('/reset_password/', methods=['POST'])
def reset_password():
    # 获取请求参数
    user_mail = request.form.get('user_mail')
    new_password = request.form.get('new_password')  # 前端已加密
    verification_code = request.form.get('verification_code')
    
    # 参数验证
    if not all([user_mail, new_password, verification_code]):
        return jsonify({'code': 400, 'message': '请填写所有必填项'})
    
    # 判断用户是否存在（只能在后端验证）
    user = User.query.filter_by(email=user_mail).first()
    if not user:
        return jsonify({'code': 400, 'message': '用户不存在'})
    
    # 验证验证码
    verify_result = verify_code(user_mail, verification_code)
    if verify_result:
        return jsonify(verify_result)
    
    try:
        # 更新密码
        user.password = new_password
        db.session.commit()
        # 刷新数据库
        db.session.refresh(user)
        # 重置成功后删除Redis中的验证码
        redis_client.delete(user_mail)
        
        return jsonify({'code': 200, 'message': '密码重置成功'})
    
    except Exception as e:
        # 回滚事务
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'密码重置失败: {str(e)}'})

