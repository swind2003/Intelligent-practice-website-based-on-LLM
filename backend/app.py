from flask import Flask
import models # 只是为了保证所有模型都被导入
import config
from blueprints.login import bp_login
from blueprints.admin import bp_admin
from extensions import (
    init_database,
    test_database, 
    init_migrate,
    init_mail,
    init_redis,
    init_cors
)

# 初始化app
app = Flask(__name__)
# 初始化配置
app.config.from_object(config)
# 在不需要时禁用信号机制
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 初始化数据库连接
init_database(app)
# 初始化redis
init_redis(app)
# 测试数据库连接
test_database(app)
# 初始化ORM迁移
migrate = init_migrate(app)
# ORM映射三步
# 1. flask db init
# 2. flask db migrate
# 3. flask db upgrade
# 初始化邮箱
init_mail(app)
# 初始化CORS
init_cors(app)
# 注册蓝图
app.register_blueprint(bp_login)
app.register_blueprint(bp_admin)

# 运行
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
