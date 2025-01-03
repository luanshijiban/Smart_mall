from flask import Blueprint, render_template
from app.models.product import Product

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')  # 直接使用根目录下的 index.html