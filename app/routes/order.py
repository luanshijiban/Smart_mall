from flask import Blueprint, redirect, url_for, render_template, flash
from flask_login import login_required, current_user
from app.models.order import Order, OrderItem
from app.models.cart import CartItem
from app import db
import datetime

order_bp = Blueprint('order', __name__)

@order_bp.route('/order/create', methods=['POST'])
@login_required
def create_order():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash('购物车为空，无法创建订单')
        return redirect(url_for('cart.view_cart'))
    
    # 创建订单
    order = Order(
        user_id=current_user.id,
        order_number=datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
        status='pending'
    )
    db.session.add(order)
    
    total_amount = 0
    # 添加订单项
    for item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.product.price
        )
        total_amount += item.quantity * item.product.price
        db.session.add(order_item)
    
    order.total_amount = total_amount
    
    # 清空购物车
    CartItem.query.filter_by(user_id=current_user.id).delete()
    
    db.session.commit()
    return redirect(url_for('order.view_orders'))

@order_bp.route('/orders')
@login_required
def view_orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('order/orders.html', orders=orders) 