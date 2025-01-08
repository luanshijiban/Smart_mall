from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# 创建数据库实例
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_message = '请先登录后再访问此页面'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # 注册蓝图
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.product import product_bp
    from app.routes.cart import cart_bp
    from app.routes.order import order_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(product_bp, url_prefix='/product')
    app.register_blueprint(cart_bp, url_prefix='/cart')
    app.register_blueprint(order_bp, url_prefix='/order')
    
    return app

# 在文件末尾导入模型
from app.models.user import User
from app.models.product import Product
from app.models.category import Category
from app.models.cart import CartItem
from app.models.order import Order, OrderItem
from app.models.after_sale import AfterSale 