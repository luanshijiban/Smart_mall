USE smart_mall;
-- 插入商品分类数据
INSERT INTO category (name, description) VALUES
('电子产品', '各种电子产品，如手机、电脑、平板'),
('家用电器', '家用电器，如冰箱、洗衣机、空调'),
('服饰', '各种服装及配饰，如衣服、鞋子、包包'),
('食品饮料', '各类食品和饮料，包括零食、酒水'),
('家具', '家居家具，如沙发、床、桌椅'),
('图书', '书籍和杂志，涵盖各类题材'),
('运动用品', '运动相关用品，如健身器材、户外装备'),
('美容护肤', '美容护肤品，如化妆品、护肤品'),
('母婴用品', '母婴相关用品，如奶粉、尿布'),
('汽车用品', '汽车配件及用品，如车载设备、养护产品'),
('医疗保健', '医疗及健康相关产品，如保健品、医疗器械'),
('宠物用品', '宠物相关商品，如食品、玩具'),
('办公用品', '办公文具及设备，如打印机、投影仪'),
('珠宝饰品', '珠宝首饰及手表'),
('游戏娱乐', '游戏设备及娱乐用品，如电子游戏、乐器');

-- 插入商品数据
-- 电子产品 (category_id = 1)
INSERT INTO product (sku, name, manufacturer, price, description, stock, category_id, image_url) VALUES
('EP001', 'MacBook Pro 14英寸', 'Apple', 12999.00, 'M2芯片，16GB内存，512GB固态硬盘', 100, 1, 'https://www.helloimg.com/i/2025/01/08/677dec28ce3cc.png'),
('EP002', 'iPhone 15 Pro', 'Apple', 8999.00, '256GB，暗夜紫色，A17芯片', 200, 1, 'https://www.helloimg.com/i/2025/01/08/677def033005b.png'),
('EP003', 'iPad Air 5', 'Apple', 4799.00, 'M1芯片，8GB内存，256GB存储', 150, 1, 'https://www.helloimg.com/i/2025/01/08/677de8a261d54.png'),
('EP004', 'Galaxy S23 Ultra', 'Samsung', 8999.00, '12GB+256GB，骁龙8 Gen 2', 100, 1, 'https://www.helloimg.com/i/2025/01/08/677de8a343e66.png'),
('EP005', 'ThinkPad X1 Carbon', 'Lenovo', 9999.00, '英特尔i7，16GB内存，1TB固态', 80, 1, 'https://www.helloimg.com/i/2025/01/08/677decc7ec85a.png');

-- 家用电器 (category_id = 2)
INSERT INTO product (sku, name, manufacturer, price, description, stock, category_id, image_url) VALUES
('HA001', '智能变频空调', '格力', 3999.00, '1.5匹，节能静音，智能控制', 50, 2, 'https://www.helloimg.com/i/2025/01/08/677dec8fbbb9b.png'),
('HA002', '对开门冰箱', '海尔', 4599.00, '501升，风冷无霜，智能控温', 30, 2, 'https://www.helloimg.com/i/2025/01/08/677decc774bdc.png'),
('HA003', '全自动洗衣机', '西门子', 3799.00, '9kg，变频节能，静音设计', 40, 2, 'https://www.helloimg.com/i/2025/01/08/677dec67d4cfa.png'),
('HA004', '智能电视', '小米', 2999.00, '55英寸4K高清，AI语音控制', 60, 2, 'https://www.helloimg.com/i/2025/01/08/677dec4841353.png'),
('HA005', '嵌入式烤箱', '方太', 3599.00, '70L大容量，多功能烘焙', 25, 2, 'https://www.helloimg.com/i/2025/01/08/677ded145db0a.png');

-- 服饰 (category_id = 3)
INSERT INTO product (sku, name, manufacturer, price, description, stock, category_id, image_url) VALUES
('CL001', '羽绒服', 'The North Face', 1999.00, '800蓬松度鹅绒，防水透气', 100, 3, 'https://www.helloimg.com/i/2025/01/08/677dec941d78f.png'),
('CL002', '牛仔裤', 'Levi\'s', 599.00, '修身直筒，经典蓝色', 200, 3, 'https://www.helloimg.com/i/2025/01/08/677deda9dc205.png'),
('CL003', '运动鞋', 'Nike', 899.00, 'Air Max系列，缓震舒适', 150, 3, NULL),
('CL004', '真皮皮带', 'Gucci', 2999.00, '头层牛皮，双G扣头', 50, 3, NULL),
('CL005', '羊毛大衣', 'Burberry', 12999.00, '英伦风格，经典格纹', 30, 3, NULL);

-- 食品饮料 (category_id = 4)
INSERT INTO product (sku, name, manufacturer, price, description, stock, category_id, image_url) VALUES
('FD001', '茅台酒', '贵州茅台', 2499.00, '53度，500ml，酱香型', 20, 4, NULL),
('FD002', '进口红酒', '拉菲', 3999.00, '法国原装，干红葡萄酒', 30, 4, NULL),
('FD003', '坚果礼盒', '三只松鼠', 199.00, '混合坚果，年货礼盒', 300, 4, NULL),
('FD004', '巧克力礼盒', 'Godiva', 599.00, '比利时进口，精选巧克力', 100, 4, NULL),
('FD005', '咖啡豆', 'Starbucks', 199.00, '中度烘焙，阿拉比卡豆', 200, 4, NULL);

-- 家具 (category_id = 5)
INSERT INTO product (sku, name, manufacturer, price, description, stock, category_id, image_url) VALUES
('FN001', '真皮沙发', 'IKEA', 5999.00, '北欧风格，三人座', 20, 5, NULL),
('FN002', '实木餐桌', '全友家私', 2999.00, '橡木材质，六人座', 30, 5, NULL),
('FN003', '书柜组合', '欧派', 1999.00, '现代简约，大容量', 40, 5, NULL),
('FN004', '双人床', '慕思', 4999.00, '1.8米宽，软硬适中', 25, 5, NULL),
('FN005', '书房办公桌', '林氏木业', 1599.00, '带书架，环保材质', 35, 5, NULL);

-- 图书 (category_id = 6)
INSERT INTO product (sku, name, manufacturer, price, description, stock, category_id, image_url) VALUES
('BK001', '人类简史', '中信出版社', 68.00, '尤瓦尔·赫拉利著，全球畅销书', 200, 6, NULL),
('BK002', '算法导论', '机械工业出版社', 128.00, '计算机科学经典教材', 100, 6, NULL),
('BK003', '经济学原理', '中国人民大学出版社', 88.00, '曼昆著，经济学入门', 150, 6, NULL),
('BK004', '金融学', '高等教育出版社', 79.00, '研究生教材，理论与实践', 120, 6, NULL),
('BK005', '深度学习', '人民邮电出版社', 119.00, 'AI领域必读书籍', 80, 6, NULL);

-- 运动用品 (category_id = 7)
INSERT INTO product (sku, name, manufacturer, price, description, stock, category_id, image_url) VALUES
('SP001', '跑步机', '舒华', 3999.00, '家用静音，可折叠', 30, 7, NULL),
('SP002', '瑜伽垫', 'Keep', 129.00, 'NBR材质，防滑耐用', 200, 7, NULL),
('SP003', '哑铃套装', '德克力', 499.00, '可调节重量，10-40kg', 100, 7, NULL),
('SP004', '篮球', 'Spalding', 299.00, '室内外通用，标准7号', 150, 7, NULL),
('SP005', '游泳镜', 'Speedo', 199.00, '防雾防水，高清镜片', 120, 7, NULL);

-- 美容护肤 (category_id = 8)
INSERT INTO product (sku, name, manufacturer, price, description, stock, category_id, image_url) VALUES
('BC001', '精华液', 'SK-II', 1299.00, '神仙水，230ml，改善肤质', 100, 8, NULL),
('BC002', '面霜', 'La Mer', 2499.00, '精华面霜，50ml，深层保湿', 50, 8, NULL),
('BC003', '防晒霜', 'Anessa', 299.00, 'SPF50+，60ml，防水防汗', 200, 8, NULL),
('BC004', '洁面乳', '雅诗兰黛', 299.00, '温和清洁，125ml', 150, 8, NULL),
('BC005', '面膜套装', '兰蔻', 699.00, '补水保湿，10片装', 100, 8, NULL);

-- 母婴用品 (category_id = 9)
INSERT INTO product (sku, name, manufacturer, price, description, stock, category_id, image_url) VALUES
('BB001', '婴儿奶粉', '惠氏', 299.00, '1段，900g，0-6个月', 100, 9, NULL),
('BB002', '纸尿裤', '花王', 199.00, 'L码，54片，9-14kg', 200, 9, NULL),
('BB003', '婴儿推车', 'Cybex', 2999.00, '可坐可躺，轻便折叠', 30, 9, NULL),
('BB004', '婴儿床', 'Stokke', 5999.00, '多功能成长床，实木', 20, 9, NULL),
('BB005', '奶瓶套装', 'Philips Avent', 399.00, '防胀气奶瓶，3个装', 100, 9, NULL);

-- 汽车用品 (category_id = 10)
INSERT INTO product (sku, name, manufacturer, price, description, stock, category_id, image_url) VALUES
('AT001', '行车记录仪', '70迈', 299.00, '1080P高清，停车监控', 100, 10, NULL),
('AT002', '汽车座垫', '3M', 599.00, '四季通用，全包围', 50, 10, NULL),
('AT003', '车载充电器', 'Anker', 99.00, '双USB快充，金属材质', 200, 10, NULL),
('AT004', '车载香氛', 'Diptyque', 399.00, '车载香薰，持久留香', 100, 10, NULL),
('AT005', '汽车脚垫', '3M', 499.00, '专车专用，全包围', 80, 10, NULL);

-- 医疗保健 (category_id = 11)
INSERT INTO product (sku, name, manufacturer, price, description, stock, category_id, image_url) VALUES
('MD001', '血压计', '欧姆龙', 399.00, '上臂式，智能测量', 100, 11, NULL),
('MD002', '血糖仪', '罗氏', 299.00, '家用血糖仪，试纸50片', 80, 11, NULL),
('MD003', '制氧机', '鱼跃', 2999.00, '家用吸氧机，3L', 30, 11, NULL),
('MD004', '雾化器', 'Philips', 399.00, '家用雾化器，静音设计', 50, 11, NULL),
('MD005', '按摩仪', 'OSIM', 1999.00, '颈椎按摩仪，智能加热', 40, 11, NULL);

-- 宠物用品 (category_id = 12)
INSERT INTO product (sku, name, manufacturer, price, description, stock, category_id, image_url) VALUES
('PT001', '狗粮', 'Royal Canin', 399.00, '成犬粮，10kg，提升免疫', 100, 12, NULL),
('PT002', '猫砂', '开饭乐', 59.00, '豆腐猫砂，6L，除臭', 200, 12, NULL),
('PT003', '宠物窝', 'Petkit', 299.00, '智能恒温窝，可拆洗', 50, 12, NULL),
('PT004', '猫爬架', 'Catit', 599.00, '多层猫爬架，带猫窝', 30, 12, NULL),
('PT005', '宠物玩具', 'Kong', 99.00, '耐咬玩具，互动训练', 150, 12, NULL);

-- 办公用品 (category_id = 13)
INSERT INTO product (sku, name, manufacturer, price, description, stock, category_id, image_url) VALUES
('OF001', '打印机', 'HP', 1999.00, '彩色喷墨，无线打印', 50, 13, NULL),
('OF002', '办公椅', 'Herman Miller', 5999.00, '人体工学，网布透气', 30, 13, NULL),
('OF003', '文件柜', '得力', 599.00, '三层抽屉，带锁', 40, 13, NULL),
('OF004', '碎纸机', '范罗士', 999.00, '静音碎纸，自动进纸', 30, 13, NULL),
('OF005', '投影仪', 'EPSON', 3999.00, '1080P高清，无线投屏', 20, 13, NULL);

-- 珠宝饰品 (category_id = 14)
INSERT INTO product (sku, name, manufacturer, price, description, stock, category_id, image_url) VALUES
('JW001', '钻石项链', 'Tiffany', 29999.00, '18K金，1克拉钻石', 10, 14, NULL),
('JW002', '珍珠耳环', 'Mikimoto', 5999.00, '天然海水珍珠，18K金', 20, 14, NULL),
('JW003', '手表', 'Rolex', 89999.00, '劳力士日志型，自动机械', 5, 14, NULL),
('JW004', '手镯', 'Cartier', 39999.00, '卡地亚LOVE系列，18K金', 10, 14, NULL),
('JW005', '戒指', 'Bvlgari', 19999.00, '宝格丽B.zero1系列，玫瑰金', 15, 14, NULL);

-- 游戏娱乐 (category_id = 15)
INSERT INTO product (sku, name, manufacturer, price, description, stock, category_id, image_url) VALUES
('GM001', 'PlayStation 5', 'Sony', 3899.00, '数字版，1TB存储', 50, 15, NULL),
('GM002', 'Switch', 'Nintendo', 2099.00, 'OLED版，白色', 100, 15, NULL),
('GM003', '游戏手柄', 'Xbox', 499.00, 'Xbox无线控制器，黑色', 150, 15, NULL),
('GM004', '游戏耳机', 'SteelSeries', 999.00, '7.1环绕声，RGB灯效', 80, 15, NULL),
('GM005', '电竞椅', 'DXRacer', 1999.00, '人体工学，可躺可调', 40, 15, NULL);

