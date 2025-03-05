#数据库模型
from extensions import db

# 用户类型表
class UserType(db.Model):
    __tablename__ = 'user_type'
    # 用户类型主键
    type_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 用户类型名称
    typename = db.Column(db.String(40), nullable=False)
    # 获取所有当前类型的用户
    users = db.relationship('User', back_populates='user_belong')

# 用户表
class User(db.Model):
    __tablename__ = 'user'
    # 用户主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 用户邮箱，同时作为用户名
    email = db.Column(db.String(100), unique=True, nullable=False)
    # 用户密码
    password = db.Column(db.String(100), nullable=False)
    # 用户类型，外键关联到用户类型表
    user_type_id = db.Column(
        db.Integer,
        db.ForeignKey('user_type.type_id'),
        nullable=False,
        default=2
    )
    # 获取当前用户属于哪种类型
    user_belong = db.relationship('UserType', back_populates='users')

# 学科表
class Subject(db.Model):
    __tablename__ = 'subject'
    # 学科主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 学科名称
    name = db.Column(db.String(100), nullable=False, unique=True)
    # 学科描述
    description = db.Column(db.Text(65536), nullable=True)
    # 获取所拥有的章节
    chapters = db.relationship('Chapter', back_populates='subject_belong')

# 章节表
class Chapter(db.Model):
    __tablename__ = 'chapter'
    # 章节主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 章节名称
    name = db.Column(db.String(100), nullable=False)
    # 章节描述
    description = db.Column(db.Text(65536), nullable=True)
    # 所属学科，外键关联到学科表
    subject_id = db.Column(
        db.Integer,
        db.ForeignKey('subject.id'),
        nullable=False
    )
    # 获取所属学科
    subject_belong = db.relationship('Subject', back_populates='chapters')
    # 获取所拥有的题目
    questions = db.relationship('Question', back_populates='chapter_belong')
    
    # 添加复合唯一约束，确保每个学科下章节名称唯一
    __table_args__ = (
        db.UniqueConstraint('name', 'subject_id', name='uix_chapter_name_subject'),
    )

# 题型表
class QuestionType(db.Model):
    __tablename__ = 'question_type'
    # 题型主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 题型名称
    name = db.Column(db.String(100), nullable=False)
    # 获取所拥有的题目
    questions = db.relationship('Question', back_populates='question_type_belong')

# 题目表
class Question(db.Model):
    __tablename__ = 'question'
    # 题目主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 题目描述
    description = db.Column(db.JSON, nullable=True)
    # 所属章节，外键关联到章节表
    chapter_id = db.Column(
        db.Integer,
        db.ForeignKey('chapter.id'),
        nullable=False)
    # 所属题型，外键关联到题型表
    question_type_id = db.Column(
        db.Integer,
        db.ForeignKey('question_type.id'),
        nullable=False)
    # 获取所属章节
    chapter_belong = db.relationship('Chapter', back_populates='questions')
    # 获取所属题型
    question_type_belong = db.relationship('QuestionType', back_populates='questions')