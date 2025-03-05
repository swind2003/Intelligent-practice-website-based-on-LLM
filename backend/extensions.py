from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
from flask_redis import FlaskRedis
from flask_cors import CORS

# 数据库对象
db = SQLAlchemy()
# 邮箱对象
mail = Mail()
# redis 对象
redis_client = FlaskRedis()
# CORS 对象
cors = CORS()

# 初始化数据库
def init_database(app):
    db.init_app(app)

# 测试数据库连接
def test_database(app):
    try:
        with app.app_context():
            with db.engine.connect():
                print("数据库连接成功")
    except Exception as e:
        print(f"数据库连接失败: {e}")

# ORM迁移
def init_migrate(app):
    return Migrate(app, db)

# 初始化邮箱
def init_mail(app):
    mail.init_app(app)

# 初始化redis
def init_redis(app):
    redis_client.init_app(app, decode_responses=True)

# 初始化CORS
def init_cors(app):
    cors.init_app(app)

