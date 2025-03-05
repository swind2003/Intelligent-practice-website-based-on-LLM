# MYSQL 配置
# 主机名
HOSTNAME = '127.0.0.1'
# 端口号
PORT = 3306
# 数据库名
DATABASE = 'bysj'
# 用户名
USERNAME = 'manager'
# 密码
PASSWORD = '314159'
# 数据库连接字符串
DB_URI = 'mysql+pymysql://' \
f'{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4'
SQLALCHEMY_DATABASE_URI = DB_URI

# 配置邮箱
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = '1974796835@qq.com'
MAIL_PASSWORD = 'llnmcxydxxlmcjih'
MAIL_DEFAULT_SENDER = '1974796835@qq.com'

# redis 配置
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 0


