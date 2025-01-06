from flask import Blueprint, redirect, url_for, render_template, flash, request, jsonify
from flask_login import login_required, current_user
from app.models.order import Order, OrderItem
from app.models.cart import CartItem
from app import db
import datetime

order_bp = Blueprint('order', __name__)

@order_bp.route('/confirm')
@login_required
def confirm_order():
    selected_items = request.args.get('selected_items', '')
    if not selected_items:
        flash('请选择要结算的商品')
        return redirect(url_for('cart.list'))
    
    product_ids = [int(id) for id in selected_items.split(',')]
    cart_items = CartItem.query.filter(
        CartItem.user_id == current_user.id,
        CartItem.product_id.in_(product_ids)
    ).all()
    
    if not cart_items:
        flash('未找到选中的商品')
        return redirect(url_for('cart.list'))
    
    total_amount = sum(item.quantity * item.product.price for item in cart_items)
    return render_template('order/confirm.html', 
                         cart_items=cart_items, 
                         total_amount=total_amount)

@order_bp.route('/create', methods=['POST'])
@login_required
def create_order():
    selected_items = request.form.get('selected_items', '')
    if not selected_items:
        flash('请选择要结算的商品')
        return redirect(url_for('cart.list'))
    
    product_ids = [int(id) for id in selected_items.split(',') if id]
    cart_items = CartItem.query.filter(
        CartItem.user_id == current_user.id,
        CartItem.product_id.in_(product_ids)
    ).all()
    
    if not cart_items:
        flash('未找到选中的商品')
        return redirect(url_for('cart.list'))
    
    try:
        # 创建订单
        order = Order(
            user_id=current_user.id,
            order_number=datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
            status='pending',
            total_amount=sum(item.quantity * item.product.price for item in cart_items),
            receiver_name=request.form.get('receiver_name'),
            shipping_address=request.form.get('shipping_address'),
            contact_phone=request.form.get('contact_phone')
        )
        db.session.add(order)
        db.session.flush()
        
        # 添加订单项
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            db.session.add(order_item)
        
        # 删除已下单的购物车项
        CartItem.query.filter(
            CartItem.user_id == current_user.id,
            CartItem.product_id.in_(product_ids)
        ).delete(synchronize_session=False)
        
        db.session.commit()
        flash('订单创建成功！')
        return redirect(url_for('order.view_orders'))
        
    except Exception as e:
        db.session.rollback()
        flash('订单创建失败，请重试')
        return redirect(url_for('cart.list'))

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