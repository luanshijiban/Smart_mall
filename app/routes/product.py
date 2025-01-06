from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models.product import Product
from app.models.category import Category
from flask_login import login_required
from math import ceil

product_bp = Blueprint('product', __name__)

@product_bp.route('/list')
def list():
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category_id', type=int)
    keyword = request.args.get('keyword', '')
    per_page = 12
    
    # 基础查询
    query = Product.query
    
    # 如果有关键词，添加搜索条件
    if keyword:
        query = query.filter(Product.name.ilike(f'%{keyword}%'))
    
    # 如果指定了分类，则筛选对应分类的商品
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    # 获取分页数据
    pagination = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    products = pagination.items
    categories = Category.query.all()
    
    return render_template(
        'product/list.html',
        products=products,
        categories=categories,
        pagination=pagination,
        category_id=category_id,
        keyword=keyword
    )

@product_bp.route('/search')
def search():
    keyword = request.args.get('keyword', '')
    page = request.args.get('page', 1, type=int)
    per_page = 12
    
    if keyword:
        query = Product.query.filter(
            Product.name.ilike(f'%{keyword}%')
        )
    else:
        query = Product.query
    
    pagination = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    products = pagination.items
    categories = Category.query.all()
    
    return render_template(
        'product/list.html',
        products=products,
        categories=categories,
        pagination=pagination,
        keyword=keyword
    )

@product_bp.route('/<int:id>')
def detail(id):
    product = Product.query.get_or_404(id)
    return render_template('product/detail.html', product=product) 