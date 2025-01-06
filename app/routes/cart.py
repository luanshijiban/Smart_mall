from flask import Blueprint, redirect, url_for, flash, request, render_template
from flask_login import login_required, current_user
from app.models.cart import CartItem
from app.models.product import Product
from app import db

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/list')
@login_required
def list():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    # 计算总金额
    total_amount = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart/list.html', cart_items=cart_items, total_amount=total_amount)

@cart_bp.route('/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    cart_item = CartItem.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()
    
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(
            user_id=current_user.id,
            product_id=product_id,
            quantity=1
        )
        db.session.add(cart_item)
    
    db.session.commit()
    flash('商品已添加到购物车')
    return redirect(url_for('cart.list'))

@cart_bp.route('/update', methods=['POST'])
@login_required
def update_cart():
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))
    
    if quantity < 1:
        quantity = 1
        
    cart_item = CartItem.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first_or_404()
    
    cart_item.quantity = quantity
    db.session.commit()
    
    return redirect(url_for('cart.list'))

@cart_bp.route('/cart/delete/<string:product_id>', methods=['POST'])
@login_required
def delete_from_cart(product_id):
    CartItem.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).delete()
    
    db.session.commit()
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/cart')
@login_required
def view_cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    return render_template('cart/cart.html', cart_items=cart_items) 