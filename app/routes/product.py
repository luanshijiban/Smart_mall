from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.models.product import Product
from sqlalchemy import or_

product_bp = Blueprint('product', __name__)

@product_bp.route('/products/search')
def search():
    search_type = request.args.get('type', 'name')
    search_term = request.args.get('q', '')
    
    if not search_term:
        return redirect(url_for('product.list'))
        
    if search_type == 'sku':
        products = Product.query.filter_by(sku=search_term).all()
    elif search_type == 'price':
        try:
            min_price, max_price = map(float, search_term.split('-'))
            products = Product.query.filter(
                Product.price >= min_price,
                Product.price <= max_price
            ).all()
        except ValueError:
            flash('价格格式不正确')
            products = []
    else:  # name
        products = Product.query.filter(
            Product.name.like(f'%{search_term}%')
        ).all()
    
    return render_template('product/list.html', products=products)

@product_bp.route('/products')
def list():
    page = request.args.get('page', 1, type=int)
    products = Product.query.paginate(
        page=page, 
        per_page=12,
        error_out=False
    )
    return render_template('product/list.html', products=products) 