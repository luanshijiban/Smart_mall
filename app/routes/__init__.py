from flask import Blueprint

# 创建蓝图
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
product_bp = Blueprint('product', __name__, url_prefix='/products')
cart_bp = Blueprint('cart', __name__, url_prefix='/cart')
order_bp = Blueprint('order', __name__, url_prefix='/orders')

# 导入路由处理函数
from .main import main_bp
from .auth import auth_bp
from .product import product_bp
from .cart import cart_bp
from .order import order_bp

# 不要删除这些导入，它们是必需的
from . import main
from . import auth
from . import product
from . import cart
from . import order 