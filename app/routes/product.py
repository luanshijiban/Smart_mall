from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from app.models.product import Product
from app.models.category import Category
from app.models.cart import CartItem
from flask_login import login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from math import ceil

product_bp = Blueprint('product', __name__)
db = SQLAlchemy()

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

@product_bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    try:
        # 从表单中获取数量，确保是整数
        quantity = int(request.form.get('quantity', 1))
        
        if quantity < 1:
            flash('无效的商品数量', 'danger')
            return redirect(url_for('product.detail', id=product_id))
        
        # 检查商品是否存在
        product = Product.query.get_or_404(product_id)
        
        # 检查购物车中是否已有此商品
        cart_item = CartItem.query.filter_by(
            user_id=current_user.id,
            product_id=product_id
        ).first()
        
        if cart_item:
            # 如果已存在，更新数量
            cart_item.quantity += quantity
        else:
            # 如果不存在，创建新的购物车项
            cart_item = CartItem(
                user_id=current_user.id,
                product_id=product_id,
                quantity=quantity
            )
            db.session.add(cart_item)
        
        db.session.commit()
        flash('成功添加到购物车', 'success')
        return redirect(url_for('cart.list'))
        
    except ValueError:
        flash('无效的商品数量', 'danger')
        return redirect(url_for('product.detail', id=product_id))
    except Exception as e:
        print(f"Error: {str(e)}")  # 添加调试信息
        db.session.rollback()
        flash('添加到购物车失败，请重试', 'danger')
        return redirect(url_for('product.detail', id=product_id)) 