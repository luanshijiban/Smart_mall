from app import db
from datetime import datetime
from sqlalchemy import Numeric

class Order(db.Model):
    STATUS_PENDING = 'pending'      # 待处理
    STATUS_COMPLETED = 'completed'  # 已完成
    STATUS_AFTER_SALE = 'after_sale'  # 售后中
    STATUS_REFUNDED = 'refunded'    # 已退款

    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_amount = db.Column(Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    is_completed = db.Column(db.Boolean, default=False, nullable=False)
    receiver_name = db.Column(db.String(50), nullable=False)
    shipping_address = db.Column(db.String(200), nullable=False)
    contact_phone = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    refund_status = db.Column(db.String(20), default='none', nullable=False)

    user = db.relationship('User', back_populates='orders')
    items = db.relationship('OrderItem', back_populates='order', lazy=True)
    after_sales = db.relationship('AfterSale', backref='order', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def can_refund(self):
        return not self.is_completed and self.refund_status == 'none'

    @property
    def can_apply_after_sale(self):
        # 订单已完成且未申请过售后且不是退款状态
        return (self.is_completed and 
                self.after_sales.first() is None and 
                self.status != self.STATUS_REFUNDED)

    @property
    def can_delete(self):
        """
        判断订单是否可以删除
        - 售后中的订单不能删除
        - 待处理的订单不能删除
        - 已退款或已完成的订单可以删除
        """
        return (self.status != self.STATUS_AFTER_SALE and 
                (self.is_completed or self.status == self.STATUS_REFUNDED))

class OrderItem(db.Model):
    __tablename__ = 'order_item'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    order = db.relationship('Order', back_populates='items')
    product = db.relationship('Product', back_populates='order_items')
    
    @property
    def subtotal(self):
        return float(self.price * self.quantity) 