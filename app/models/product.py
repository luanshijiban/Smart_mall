from app import db
from datetime import datetime
from sqlalchemy import Numeric

class Product(db.Model):
    __tablename__ = 'product'
    
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(30), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    manufacturer = db.Column(db.String(100))
    price = db.Column(Numeric(10, 2), nullable=False)
    description = db.Column(db.Text)
    stock = db.Column(db.Integer, nullable=False, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系 - 使用字符串引用而不是直接导入
    category = db.relationship('Category', back_populates='products')
    cart_items = db.relationship('CartItem', back_populates='product', cascade='all, delete-orphan')
    order_items = db.relationship('OrderItem', back_populates='product')

    def __repr__(self):
        return f'<Product {self.name}>' 