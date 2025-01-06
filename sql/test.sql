-- 切换到数据库
USE smart_mall;

-- 插入用户数据
INSERT INTO user (username, password_hash, phone, address, real_name) VALUES
('user1', 'hashed_password1', '12345678901', '地址1', '张三'),
('user2', 'hashed_password2', '12345678902', '地址2', '李四'),
('user3', 'hashed_password3', '12345678903', '地址3', '王五');

-- 插入商品分类数据
INSERT INTO category (name, description) VALUES
('电子产品', '各种电子产品，如手机、电脑'),
('家用电器', '家用电器，如冰箱、洗衣机'),
('服饰', '各类服装和配饰');

-- 插入商品数据
INSERT INTO product (sku, name, manufacturer, price, description, stock, category_id, image_url) VALUES
('SKU001', '智能手机', '某品牌', 4999.99, '高性能智能手机', 50, 1, 'http://example.com/image1.jpg'),
('SKU002', '笔记本电脑', '某品牌', 8999.99, '轻薄便携笔记本电脑', 30, 1, 'http://example.com/image2.jpg'),
('SKU003', '洗衣机', '某品牌', 1999.99, '全自动洗衣机', 20, 2, 'http://example.com/image3.jpg'),
('SKU004', '羽绒服', '某品牌', 799.99, '冬季保暖羽绒服', 100, 3, 'http://example.com/image4.jpg');

-- 插入购物车数据
INSERT INTO cart (user_id, product_id, quantity) VALUES
(1, 1, 2),
(1, 3, 1),
(2, 2, 1),
(3, 4, 3);

-- 插入订单数据
INSERT INTO `order` (order_number, user_id, total_amount, status, shipping_address, contact_phone) VALUES
('ORD001', 1, 9999.97, 'pending', '地址1', '12345678901'),
('ORD002', 2, 8999.99, 'completed', '地址2', '12345678902');

-- 插入订单详情数据
INSERT INTO order_item (order_id, product_id, quantity, price) VALUES
(1, 1, 2, 4999.99),
(2, 2, 1, 8999.99);



select * from user;
select * from category; 
select * from product;
select * from cart; 
select * from `order`;
select * from order_item;