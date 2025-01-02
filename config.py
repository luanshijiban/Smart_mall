import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'dev'  # 开发环境使用简单密钥，生产环境需要更改
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/smart_mall'  # 数据库名改为smart_mall
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 上传文件配置
    UPLOAD_FOLDER = os.path.join(basedir, 'app/static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max-limit 