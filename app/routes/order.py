from flask import Blueprint, redirect, url_for, render_template, flash, request, jsonify
from flask_login import login_required, current_user
from app.models.order import Order, OrderItem
from app.models.cart import CartItem
from app.models.after_sale import AfterSale
from app import db
import datetime

order_bp = Blueprint('order', __name__)

@order_bp.route('/confirm')
@login_required
def confirm_order():
    selected_items = request.args.get('selected_items', '')
    if not selected_items:
        flash('请选择要结算的商品', 'error')
        return redirect(url_for('cart.list'))
    
    product_ids = [int(id) for id in selected_items.split(',')]
    cart_items = CartItem.query.filter(
        CartItem.user_id == current_user.id,
        CartItem.product_id.in_(product_ids)
    ).all()
    
    if not cart_items:
        flash('未找到选中的商品', 'error')
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
        flash('请选择要结算的商品', 'error')
        return redirect(url_for('cart.list'))
    
    product_ids = [int(id) for id in selected_items.split(',') if id]
    cart_items = CartItem.query.filter(
        CartItem.user_id == current_user.id,
        CartItem.product_id.in_(product_ids)
    ).all()
    
    if not cart_items:
        flash('未找到选中的商品', 'error')
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
        flash('订单创建成功', 'success')
        return redirect(url_for('order.view_orders'))
        
    except Exception as e:
        db.session.rollback()
        flash('订单创建失败，请重试', 'error')
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
        flash('订单已经完成', 'error')
        return redirect(url_for('order.view_orders'))
    
    try:
        order.is_completed = True
        db.session.commit()
        flash('订单已确认收货', 'success')
    except:
        db.session.rollback()
        flash('操作失败，请重试', 'error')
    
    return redirect(url_for('order.view_orders'))

@order_bp.route('/refund/<int:order_id>', methods=['POST'])
@login_required
def refund_order(order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    
    if not order.can_refund:
        flash('订单不符合退款条件', 'error')
        # 根据来源页面决定重定向
        if request.referrer and 'list' in request.referrer:
            return redirect(url_for('order.view_orders'))
        return redirect(url_for('order.detail', order_id=order_id))
    
    try:
        order.refund_status = 'completed'
        order.status = 'refunded'
        db.session.commit()
        flash('退款成功', 'success')
    except:
        db.session.rollback()
        flash('退款失败，请重试', 'error')
    
    # 根据来源页面决定重定向
    if request.referrer and 'list' in request.referrer:
        return redirect(url_for('order.view_orders'))
    return redirect(url_for('order.detail', order_id=order_id))

@order_bp.route('/delete/<int:order_id>', methods=['POST'])
@login_required
def delete_order(order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    
    # 检查订单是否可以删除
    if not order.can_delete:
        if order.status == Order.STATUS_AFTER_SALE:
            flash('售后处理中的订单不能删除', 'error')
        else:
            flash('订单正在处理中，无法删除', 'error')
        
        # 根据来源页面决定重定向
        if request.referrer and 'detail' in request.referrer:
            return redirect(url_for('order.detail', order_id=order_id))
        return redirect(url_for('order.view_orders'))
    
    try:
        # 先删除订单项
        OrderItem.query.filter_by(order_id=order.id).delete()
        # 再删除订单
        db.session.delete(order)
        db.session.commit()
        flash('订单已删除', 'success')
        return redirect(url_for('order.view_orders'))
    except:
        db.session.rollback()
        flash('删除失败，请重试', 'error')
        if request.referrer and 'detail' in request.referrer:
            return redirect(url_for('order.detail', order_id=order_id))
        return redirect(url_for('order.view_orders'))

@order_bp.route('/after-sale/<int:order_id>')
@login_required
def after_sale(order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    if not order.can_apply_after_sale:
        flash('该订单不满足申请售后条件', 'warning')
        return redirect(url_for('order.detail', order_id=order_id))
    return render_template('order/after_sale.html', order=order)

@order_bp.route('/after-sale/<int:order_id>/submit', methods=['POST'])
@login_required
def submit_after_sale(order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    if not order.can_apply_after_sale:
        flash('该订单不满足申请售后条件', 'warning')
        return redirect(url_for('order.view_orders'))
    
    try:
        # 创建售后申请
        after_sale = AfterSale(
            order_id=order_id,
            user_id=current_user.id,
            type=request.form.get('type'),
            reason=request.form.get('reason')
        )
        db.session.add(after_sale)
        
        # 更新订单状态为售后中
        order.status = Order.STATUS_AFTER_SALE
        
        db.session.commit()
        flash('售后申请已提交', 'success')
        
        # 根据表单中的 source 参数决定重定向
        if request.form.get('source') == 'list':
            return redirect(url_for('order.view_orders'))
        return redirect(url_for('order.detail', order_id=order_id))
        
    except:
        db.session.rollback()
        flash('申请提交失败，请重试', 'error')
        return redirect(url_for('order.after_sale', order_id=order_id))

@order_bp.route('/cancel-after-sale/<int:order_id>', methods=['POST'])
@login_required
def cancel_after_sale(order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    
    if order.status != Order.STATUS_AFTER_SALE:
        flash('订单不是售后状态，无法取消售后', 'error')
    else:
        try:
            # 删除售后申请记录
            AfterSale.query.filter_by(order_id=order.id).delete()
            # 将订单状态改回已完成
            order.status = Order.STATUS_COMPLETED
            order.is_completed = True
            db.session.commit()
            flash('已取消售后申请', 'success')
        except:
            db.session.rollback()
            flash('操作失败，请重试', 'error')
    
    # 根据来源页面决定重定向
    if request.referrer and 'list' in request.referrer:
        return redirect(url_for('order.view_orders'))
    return redirect(url_for('order.detail', order_id=order_id))