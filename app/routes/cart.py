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
    # 获取已选中的商品ID列表
    selected_items = session.get('selected_items', [])
    return render_template('cart/list.html', 
                         cart_items=cart_items, 
                         total_amount=total_amount,
                         selected_items=selected_items)

@cart_bp.route('/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    try:
        # 获取数量，从表单中获取
        quantity = int(request.form.get('quantity', 1))
        print(f"Debug - Quantity from form: {quantity}")
        
        product = Product.query.get_or_404(product_id)
        print(f"Debug - Product found: {product.name}")

        cart_item = CartItem.query.filter_by(
            user_id=current_user.id,
            product_id=product_id
        ).first()
        
        if cart_item:
            cart_item.quantity += quantity
            print(f"Debug - Updated quantity: {cart_item.quantity}")
        else:
            cart_item = CartItem(
                user_id=current_user.id,
                product_id=product_id,
                quantity=quantity
            )
            db.session.add(cart_item)
            print(f"Debug - New cart item created")
        
        db.session.commit()
        
        # 更新 session 中的选中状态
        selected_items = session.get('selected_items', [])
        if str(product_id) not in selected_items:
            selected_items.append(str(product_id))
            session['selected_items'] = selected_items
        
        flash(f'已将 {quantity} 件商品添加到购物车', 'success')
        return redirect(url_for('cart.list'))
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        db.session.rollback()
        flash('添加到购物车失败，请重试', 'danger')
        return redirect(url_for('product.detail', id=product_id))

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

@cart_bp.route('/remove', methods=['POST'])
@login_required
def remove_from_cart():
    product_id = request.form.get('product_id')
    if not product_id:
        return jsonify({'status': 'error', 'message': '商品ID不能为空'}), 400
        
    try:
        product = CartItem.query.filter_by(
            user_id=current_user.id,
            product_id=product_id
        ).first()
        
        if product:
            CartItem.query.filter_by(
                user_id=current_user.id,
                product_id=product_id
            ).delete()
            db.session.commit()
            return jsonify({
                'status': 'success',
                'message': '商品已从购物车中移除',
                'type': 'success'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': '商品不存在',
                'type': 'error'
            })
    except:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': '删除失败，请重试',
            'type': 'error'
        })

@cart_bp.route('/clear', methods=['POST'])
@login_required
def clear_cart():
    try:
        CartItem.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        flash('购物车已清空', 'success')
    except:
        db.session.rollback()
        flash('清空购物车失败，请重试', 'error')
    return redirect(url_for('cart.list'))

@cart_bp.route('/save-selected-items', methods=['POST'])
@login_required
def save_selected_items():
    try:
        if request.is_json:
            data = request.get_json()
            selected_items = data.get('selected_items', [])
            # 确保所有项都是字符串类型
            selected_items = [str(item) for item in selected_items]
            session['selected_items'] = selected_items
            return jsonify({'status': 'success'})
        return jsonify({'status': 'error', 'message': '无效的请求格式'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}) 