from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = '请先登录'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    
    # 确保所有模型都被导入
    from .models import User, Product, Category, CartItem, Order, OrderItem
    
    # 导入蓝图
    from .routes.main import main_bp
    from .routes.auth import auth_bp
    from .routes.product import product_bp
    from .routes.cart import cart_bp
    from .routes.order import order_bp
    
    # 注册蓝图
    app.register_blueprint(main_bp)  # 主页蓝图应该放在最前面
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(product_bp, url_prefix='/products')
    app.register_blueprint(cart_bp, url_prefix='/cart')
    app.register_blueprint(order_bp, url_prefix='/orders')
    
    return app 