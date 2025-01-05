from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models.product import Product
from app.models.category import Category
from flask_login import login_required

product_bp = Blueprint('product', __name__)

@product_bp.route('/list')
def list():
    products = Product.query.all()
    return render_template('product/list.html', products=products)

@product_bp.route('/search')
def search():
    keyword = request.args.get('keyword', '')
    products = Product.query.filter(Product.name.like(f'%{keyword}%')).all()
    return render_template('product/search.html', products=products, keyword=keyword)

@product_bp.route('/<int:id>')
def detail(id):
    product = Product.query.get_or_404(id)
    return render_template('product/detail.html', product=product) 