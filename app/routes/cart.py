from flask import Blueprint, redirect, url_for, flash, request, render_template, jsonify, session
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
    
    # 获取数量，如果是JSON请求则从请求体获取，否则默认为1
    if request.is_json:
        quantity = request.json.get('quantity', 1)
    else:
        quantity = 1

    cart_item = CartItem.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            user_id=current_user.id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)
    
    # 在 session 中标记新添加的商品，但不清除其他选中状态
    session['last_added_item'] = product_id
    if 'selected_items' not in session:
        session['selected_items'] = []
    
    db.session.commit()
    flash(f'已将 {quantity} 件商品添加到购物车')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'status': 'success', 
            'product_id': product_id,
            'checked': True
        })
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

@cart_bp.route('/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_from_cart(product_id):
    CartItem.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).delete()
    
    db.session.commit()
    return redirect(url_for('cart.list'))

@cart_bp.route('/cart')
@login_required
def view_cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    return render_template('cart/cart.html', cart_items=cart_items)

@cart_bp.route('/clear', methods=['POST'])
@login_required
def clear_cart():
    try:
        CartItem.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        flash('购物车已清空')
    except Exception as e:
        db.session.rollback()
        flash('清空购物车失败，请重试')
    return redirect(url_for('cart.list'))

@cart_bp.route('/save-selected-items', methods=['POST'])
@login_required
def save_selected_items():
    if request.is_json:
        data = request.get_json()
        session['selected_items'] = data.get('selected_items', [])
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'}) 