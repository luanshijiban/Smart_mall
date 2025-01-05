from flask import Blueprint

# 创建蓝图
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
product_bp = Blueprint('product', __name__)
cart_bp = Blueprint('cart', __name__, url_prefix='/cart')
order_bp = Blueprint('order', __name__, url_prefix='/orders')

# 导入视图函数
from . import main
from . import auth
from . import product
from . import cart
from . import order 