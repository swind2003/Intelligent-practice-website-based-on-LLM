from flask import Blueprint, request, jsonify
from models import Subject, Chapter, Question, QuestionType
from extensions import db

# 管理员蓝图
bp_admin = Blueprint('admin', __name__, url_prefix='/admin')


# 从数据库获取所有学科
@bp_admin.route('/get_subjects/', methods=['GET'])
def get_subjects():
    try:
        # 查询数据库中的所有学科记录
        subjects = Subject.query.all()
        # 初始化空列表用于存储学科数据
        subjects_list = []
        
        # 遍历所有学科记录
        for subject in subjects:
            # 将每个学科的信息添加到列表中
            subjects_list.append({
                'id': subject.id,
                'name': subject.name,
                'description': subject.description
            })
        
        # 返回成功响应，包含学科列表数据
        return jsonify({
            'code': 200,
            'message': '获取学科列表成功',
            'data': subjects_list
        })
    except Exception as e:
        # 捕获并处理异常情况
        # 返回错误响应，包含错误信息
        return jsonify({
            'code': 500,
            'message': f'获取学科列表失败: {str(e)}'
        }), 500


# 按名称搜索学科
@bp_admin.route('/search_subject/', methods=['GET'])
def search_subject():
    try:
        # 从请求参数中获取学科名称
        name = request.args.get('name', '')
        
        # 验证名称参数是否为空
        if not name:
            # 如果名称为空，返回错误响应
            return jsonify({
                'code': 400,
                'message': '学科名称不能为空'
            })
        
        # 使用模糊匹配搜索学科
        subject = Subject.query.filter(Subject.name.like(f'%{name}%')).first()
        
        # 检查是否找到匹配的学科
        if not subject:
            # 如果未找到匹配学科，返回错误响应
            return jsonify({
                'code': 404,
                'message': '未找到匹配的学科'
            })
        
        # 返回成功响应，包含找到的学科信息
        return jsonify({
            'code': 200,
            'message': '搜索学科成功',
            'data': {
                'id': subject.id,
                'name': subject.name,
                'description': subject.description
            }
        })
    except Exception as e:
        # 捕获并处理异常情况
        # 返回错误响应，包含错误信息
        return jsonify({
            'code': 500,
            'message': f'搜索学科失败: {str(e)}'
        })


# 获取单个学科信息
@bp_admin.route('/get_subject/<int:subject_id>', methods=['GET'])
def get_subject(subject_id):
    try:
        # 根据ID查询学科
        subject = Subject.query.get(subject_id)
        
        # 检查学科是否存在
        if not subject:
            # 如果学科不存在，返回404错误
            return jsonify({
                'code': 404,
                'message': '学科不存在'
            }), 404
        
        # 返回成功响应，包含学科详细信息
        return jsonify({
            'code': 200,
            'message': '获取学科信息成功',
            'data': {
                'id': subject.id,
                'name': subject.name,
                'description': subject.description
            }
        })
    except Exception as e:
        # 捕获并处理异常情况
        # 返回错误响应，包含错误信息
        return jsonify({
            'code': 500,
            'message': f'获取学科信息失败: {str(e)}'
        }), 500


# 获取学科下的章节列表
@bp_admin.route('/get_chapters/<int:subject_id>', methods=['GET'])
def get_chapters(subject_id):
    try:
        # 根据ID查询学科
        subject = Subject.query.get(subject_id)
        
        # 检查学科是否存在
        if not subject:
            # 如果学科不存在，返回404错误
            return jsonify({
                'code': 404,
                'message': '学科不存在'
            }), 404
        
        # 查询指定学科下的所有章节
        chapters = Chapter.query.filter_by(subject_id=subject_id).all()
        # 初始化空列表用于存储章节数据
        chapters_list = []
        
        # 遍历所有章节记录
        for chapter in chapters:
            # 将每个章节的信息添加到列表中
            chapters_list.append({
                'id': chapter.id,
                'name': chapter.name,
                'description': chapter.description,
                'subject_id': chapter.subject_id
            })
        
        # 返回成功响应，包含章节列表数据
        return jsonify({
            'code': 200,
            'message': '获取章节列表成功',
            'data': chapters_list
        })
    except Exception as e:
        # 捕获并处理异常情况
        # 返回错误响应，包含错误信息
        return jsonify({
            'code': 500,
            'message': f'获取章节列表失败: {str(e)}'
        }), 500


# 获取所有题型
@bp_admin.route('/get_question_types/', methods=['GET'])
def get_question_types():
    try:
        # 查询所有题型记录
        types = QuestionType.query.all()
        # 初始化空列表用于存储题型数据
        types_list = []
        
        # 遍历所有题型记录
        for type in types:
            # 将每个题型的信息添加到列表中
            types_list.append({
                'id': type.id,
                'name': type.name
            })
        
        # 返回成功响应，包含题型列表数据
        return jsonify({
            'code': 200,
            'message': '获取题型列表成功',
            'data': types_list
        })
    except Exception as e:
        # 捕获并处理异常情况
        # 返回错误响应，包含错误信息
        return jsonify({
            'code': 500,
            'message': f'获取题型列表失败: {str(e)}'
        }), 500


# 获取学科下的所有题目
@bp_admin.route('/get_questions/<int:subject_id>', methods=['GET'])
def get_questions(subject_id):
    try:
        # 验证学科是否存在
        subject = Subject.query.get(subject_id)
        # 如果学科不存在，返回404错误
        if not subject:
            return jsonify({
                'code': 404,
                'message': '学科不存在'
            }), 404
        
        # 获取该学科下所有章节的ID
        chapter_ids = [chapter.id for chapter in Chapter.query.filter_by(subject_id=subject_id).all()]
        
        # 如果没有章节，则返回空列表
        if not chapter_ids:
            return jsonify({
                'code': 200,
                'message': '获取题目列表成功',
                'data': []
            })
        
        # 获取这些章节下的所有题目
        questions = Question.query.filter(Question.chapter_id.in_(chapter_ids)).all()
        # 初始化空列表用于存储题目数据
        questions_list = []
        
        # 遍历所有题目记录
        for question in questions:
            # 将每个题目的信息添加到列表中
            questions_list.append({
                'id': question.id,
                'description': question.description,
                'chapter_id': question.chapter_id,
                'question_type_id': question.question_type_id,
                'difficulty': question.description.get('difficulty', '未设置') if question.description else '未设置'
            })
        
        # 返回成功响应，包含题目列表数据
        return jsonify({
            'code': 200,
            'message': '获取题目列表成功',
            'data': questions_list
        })
    except Exception as e:
        # 捕获并处理异常情况
        # 返回错误响应，包含错误信息
        return jsonify({
            'code': 500,
            'message': f'获取题目列表失败: {str(e)}'
        }), 500


# 创建章节
@bp_admin.route('/create_chapter/', methods=['POST'])
def create_chapter():
    try:
        # 获取请求中的JSON数据
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['subject_id', 'name']
        # 遍历检查每个必填字段
        for field in required_fields:
            # 如果字段不存在或为空，返回400错误
            if field not in data or not data[field]:
                return jsonify({
                    'code': 400,
                    'message': f'缺少必填字段: {field}'
                }), 400
        
        # 验证学科是否存在
        subject = Subject.query.get(data['subject_id'])
        # 如果学科不存在，返回404错误
        if not subject:
            return jsonify({
                'code': 404,
                'message': '学科不存在'
            }), 404
        
        # 创建新章节对象
        chapter = Chapter(
            name=data['name'],
            description=data.get('description', ''),
            subject_id=data['subject_id']
        )
        
        # 保存到数据库
        db.session.add(chapter)
        # 提交事务
        db.session.commit()
        
        # 返回成功响应，包含新创建的章节信息
        return jsonify({
            'code': 200,
            'message': '创建章节成功',
            'data': {
                'id': chapter.id,
                'name': chapter.name,
                'description': chapter.description,
                'subject_id': chapter.subject_id
            }
        })
    except Exception as e:
        # 发生异常时回滚事务
        db.session.rollback()
        
        # 处理违反唯一约束的错误
        if 'uix_chapter_name_subject' in str(e):
            # 如果是章节名称在同一学科下重复，返回400错误
            return jsonify({
                'code': 400,
                'message': '该学科下已存在同名章节'
            }), 400
        
        # 返回一般错误响应，包含错误信息
        return jsonify({
            'code': 500,
            'message': f'创建章节失败: {str(e)}'
        }), 500


# 更新章节
@bp_admin.route('/update_chapter/<int:chapter_id>', methods=['PUT'])
def update_chapter(chapter_id):
    try:
        # 检查章节是否存在
        chapter = Chapter.query.get(chapter_id)
        # 如果章节不存在，返回404错误
        if not chapter:
            return jsonify({
                'code': 404,
                'message': '章节不存在'
            }), 404
        
        # 获取请求中的JSON数据
        data = request.get_json()
        
        # 更新章节名称（如果提供了有效的名称）
        if 'name' in data and data['name']:
            chapter.name = data['name']
        
        # 更新章节描述（如果提供了描述字段）
        if 'description' in data:
            chapter.description = data['description']
        
        # 保存到数据库
        db.session.commit()
        
        # 返回成功响应，包含更新后的章节信息
        return jsonify({
            'code': 200,
            'message': '更新章节成功',
            'data': {
                'id': chapter.id,
                'name': chapter.name,
                'description': chapter.description,
                'subject_id': chapter.subject_id
            }
        })
    except Exception as e:
        # 发生异常时回滚事务
        db.session.rollback()
        
        # 处理违反唯一约束的错误
        if 'uix_chapter_name_subject' in str(e):
            # 如果是章节名称在同一学科下重复，返回400错误
            return jsonify({
                'code': 400,
                'message': '该学科下已存在同名章节'
            }), 400
        
        # 返回一般错误响应，包含错误信息
        return jsonify({
            'code': 500,
            'message': f'更新章节失败: {str(e)}'
        }), 500


# 删除章节
@bp_admin.route('/delete_chapter/<int:chapter_id>', methods=['DELETE'])
def delete_chapter(chapter_id):
    try:
        # 检查章节是否存在
        chapter = Chapter.query.get(chapter_id)
        # 如果章节不存在，返回404错误
        if not chapter:
            return jsonify({
                'code': 404,
                'message': '章节不存在'
            }), 404
        
        # 删除章节下的所有题目
        Question.query.filter_by(chapter_id=chapter_id).delete()
        
        # 删除章节
        db.session.delete(chapter)
        # 提交事务
        db.session.commit()
        
        # 返回成功响应
        return jsonify({
            'code': 200,
            'message': '删除章节成功'
        })
    except Exception as e:
        # 发生异常时回滚事务
        db.session.rollback()
        # 返回错误响应，包含错误信息
        return jsonify({
            'code': 500,
            'message': f'删除章节失败: {str(e)}'
        }), 500


# 删除题目
@bp_admin.route('/delete_question/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    try:
        # 检查题目是否存在
        question = Question.query.get(question_id)
        # 如果题目不存在，返回404错误
        if not question:
            return jsonify({
                'code': 404,
                'message': '题目不存在'
            }), 404
        
        # 删除题目
        db.session.delete(question)
        # 提交事务
        db.session.commit()
        
        # 返回成功响应
        return jsonify({
            'code': 200,
            'message': '删除题目成功'
        })
    except Exception as e:
        # 发生异常时回滚事务
        db.session.rollback()
        # 返回错误响应，包含错误信息
        return jsonify({
            'code': 500,
            'message': f'删除题目失败: {str(e)}'
        }), 500


# 创建新学科
@bp_admin.route('/create_subject/', methods=['POST'])
def create_subject():
    try:
        # 获取前端传来的学科信息
        data = request.get_json()
        # 获取学科名称
        name = data.get('name')
        # 获取学科描述，如果没有则默认为空字符串
        description = data.get('description', '')
        
        # 参数验证：检查学科名称是否为空
        if not name:
            # 如果名称为空，返回400错误
            return jsonify({
                'code': 400,
                'message': '学科名称不能为空',
                'data': None
            })
        
        # 检查学科名称是否已存在
        existing_subject = Subject.query.filter_by(name=name).first()
        # 如果学科名称已存在，返回400错误
        if existing_subject:
            return jsonify({
                'code': 400,
                'message': f'学科名称 "{name}" 已存在',
                'data': None
            })
        
        # 创建新学科对象
        new_subject = Subject(name=name, description=description)
        # 添加到数据库会话
        db.session.add(new_subject)
        # 提交事务
        db.session.commit()
        # 刷新对象以获取数据库生成的ID
        db.session.refresh(new_subject)
        
        # 返回成功响应，包含新创建的学科信息
        return jsonify({
            'code': 200,
            'message': f'学科 "{name}" 创建成功',
            'data': {
                'id': new_subject.id,
                'name': new_subject.name,
                'description': new_subject.description
            }
        })
    except Exception as e:
        # 发生错误时回滚会话
        db.session.rollback()
        # 返回错误响应，包含错误信息
        return jsonify({
            'code': 500,
            'message': f'创建学科失败: {str(e)}',
            'data': None
        })

# 删除单个学科
@bp_admin.route('/delete_subject/<int:subject_id>', methods=['DELETE'])
def delete_subject(subject_id):
    try:
        # 查找要删除的学科
        subject = Subject.query.get(subject_id)
        
        # 检查学科是否存在
        if not subject:
            # 如果学科不存在，返回404错误
            return jsonify({
                'code': 404,
                'message': f'学科ID {subject_id} 不存在',
                'data': None
            })
        
        # 保存学科名称以便在响应中使用
        subject_name = subject.name
        
        # 删除学科
        db.session.delete(subject)
        # 提交事务
        db.session.commit()
        # 刷新对象
        db.session.refresh(subject)
        # 返回成功响应
        return jsonify({
            'code': 200,
            'message': f'学科 "{subject_name}" 删除成功',
            'data': {'id': subject_id}
        })
    except Exception as e:
        # 发生错误时回滚会话
        db.session.rollback()
        # 返回错误响应，包含错误信息
        return jsonify({
            'code': 500,
            'message': f'删除学科失败: {str(e)}',
            'data': None
        })

# 批量删除学科
@bp_admin.route('/batch_delete_subjects/', methods=['POST'])
def batch_delete_subjects():
    try:
        # 获取要删除的学科ID列表
        data = request.get_json()
        # 从请求数据中获取ID列表，如果没有则默认为空列表
        subject_ids = data.get('ids', [])
        
        # 检查是否提供了ID列表
        if not subject_ids:
            # 如果没有提供ID列表，返回400错误
            return jsonify({
                'code': 400,
                'message': '没有提供要删除的学科ID',
                'data': None
            })
        
        # 查找所有要删除的学科
        subjects = Subject.query.filter(Subject.id.in_(subject_ids)).all()
        # 获取实际找到的学科ID列表
        found_ids = [subject.id for subject in subjects]
        
        # 检查是否所有ID都有效
        missing_ids = set(subject_ids) - set(found_ids)
        # 如果有无效ID，返回404错误
        if missing_ids:
            return jsonify({
                'code': 404,
                'message': f'以下学科ID不存在: {", ".join(map(str, missing_ids))}',
                'data': None
            })
        
        # 删除所有找到的学科
        for subject in subjects:
            db.session.delete(subject)
        
        # 提交事务
        db.session.commit()
        # 刷新对象
        db.session.refresh(subjects)
        
        # 返回成功响应
        return jsonify({
            'code': 200,
            'message': f'成功删除 {len(found_ids)} 个学科',
            'data': {'ids': found_ids}
        })
    except Exception as e:
        # 发生错误时回滚会话
        db.session.rollback()
        # 返回错误响应，包含错误信息
        return jsonify({
            'code': 500,
            'message': f'批量删除学科失败: {str(e)}',
            'data': None
        })




