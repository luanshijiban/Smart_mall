from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import login_required, current_user
from app.models.order import Order, OrderItem
from app.models.cart import CartItem
from app import db
import datetime

order_bp = Blueprint('order', __name__)

@order_bp.route('/confirm')
@login_required
def confirm_order():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash('购物车为空，无法创建订单')
        return redirect(url_for('cart.list'))
    
    total_amount = sum(item.quantity * item.product.price for item in cart_items)
    return render_template('order/confirm.html', 
                         cart_items=cart_items, 
                         total_amount=total_amount,
                         default_name=current_user.real_name,
                         default_phone=current_user.phone)

@order_bp.route('/create', methods=['POST'])
@login_required
def create_order():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash('购物车为空，无法创建订单')
        return redirect(url_for('cart.list'))
    
    # 获取表单数据
    receiver_name = request.form.get('receiver_name')
    shipping_address = request.form.get('shipping_address')
    contact_phone = request.form.get('contact_phone')
    
    if not all([receiver_name, shipping_address, contact_phone]):
        flash('请填写完整的收货信息')
        return redirect(url_for('order.confirm_order'))
    
    # 计算总金额
    total_amount = sum(item.quantity * item.product.price for item in cart_items)
    
    # 创建订单
    order = Order(
        user_id=current_user.id,
        order_number=datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
        status='pending',
        total_amount=total_amount,
        receiver_name=receiver_name,
        shipping_address=shipping_address,
        contact_phone=contact_phone,
        is_completed=False  # 新订单默认未完成
    )
    db.session.add(order)
    db.session.flush()
    
    # 添加订单项
    for item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.product.price
        )
        db.session.add(order_item)
    
    # 清空购物车
    CartItem.query.filter_by(user_id=current_user.id).delete()
    
    try:
        db.session.commit()
        flash('订单创建成功！')
    except Exception as e:
        db.session.rollback()
        flash('订单创建失败，请重试')
        return redirect(url_for('cart.list'))
        
    return redirect(url_for('order.view_orders'))

@order_bp.route('/list')
@login_required
def view_orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('order/list.html', orders=orders)

@order_bp.route('/detail/<int:order_id>')
@login_required
def detail(order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    return render_template('order/detail.html', order=order)

@order_bp.route('/complete/<int:order_id>', methods=['POST'])
@login_required
def complete_order(order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    
    if order.is_completed:
        flash('订单已经完成')
        # 获取来源页面
        if request.referrer and 'detail' in request.referrer:
            return redirect(url_for('order.detail', order_id=order_id))
        return redirect(url_for('order.view_orders'))
    
    order.is_completed = True
    try:
        db.session.commit()
        flash('订单已确认收货')
    except:
        db.session.rollback()
        flash('操作失败，请重试')
    
    # 根据来源页面决定重定向
    if request.referrer and 'detail' in request.referrer:
        return redirect(url_for('order.detail', order_id=order_id))
    return redirect(url_for('order.view_orders')) 