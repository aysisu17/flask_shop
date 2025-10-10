import sqlite3

def get_db_connection():
    conn = sqlite3.connect('shop.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_tables():
    """Создает все необходимые таблицы"""
    conn = get_db_connection()
    
    #таблица товаров
    conn.execute('''
        CREATE TABLE IF NOT EXISTS product (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            image TEXT
        )
    ''')
    
    #таблица заказов
    conn.execute('''
        CREATE TABLE IF NOT EXISTS order_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            customer_email TEXT NOT NULL,
            customer_phone TEXT NOT NULL,
            customer_address TEXT NOT NULL,
            total_amount REAL NOT NULL,
            order_date TEXT NOT NULL
        )
    ''')
    
    #таблица элементов заказа
    conn.execute('''
        CREATE TABLE IF NOT EXISTS order_item (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES order_table (id),
            FOREIGN KEY (product_id) REFERENCES product (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Таблицы созданы")

def init_products():
    """Добавляет товары одежды в базу данных"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    #проверяем, есть ли уже товары
    cursor.execute('SELECT COUNT(*) as count FROM product')
    if cursor.fetchone()[0] == 0:
        
        products = [
            
            ('Кожаная куртка', 8999.99, 'Стильная кожаная куртка черного цвета', 'leather_jacket.jpg'),
            ('Джинсовая куртка', 3499.99, 'Классическая джинсовая куртка', 'denim_jacket.jpg'),
            ('Пальто шерстяное', 12999.99, 'Теплое шерстяное пальто для холодной погоды', 'wool_coat.jpg'),
            ('Пуховик зимний', 15999.99, 'Теплый пуховик для морозной зимы', 'winter_jacket.jpg'),
            ('Плащ дождевик', 5999.99, 'Водоотталкивающий плащ для дождливой погоды', 'raincoat.jpg'),
            
            
            ('Футболка хлопковая', 1499.99, 'Мягкая хлопковая футболка белого цвета', 'cotton_tshirt.jpg'),
            ('Футболка с принтом', 1999.99, 'Футболка с уникальным графическим принтом', 'graphic_tshirt.jpg'),
            ('Поло классическое', 2999.99, 'Элегантная поло из качественного хлопка', 'polo_shirt.jpg'),
            ('Футболка базовая', 999.99, 'Базовая футболка для повседневной носки', 'basic_tshirt.jpg'),
            ('Футболка oversize', 2499.99, 'Модная футболка oversize кроя', 'oversize_tshirt.jpg'),
            
            
            ('Рубашка офисная', 4599.99, 'Классическая рубашка для офиса', 'office_shirt.jpg'),
            ('Рубашка фланелевая', 3299.99, 'Теплая фланелевая рубашка в клетку', 'flannel_shirt.jpg'),
            ('Рубашка деним', 3899.99, 'Стильная рубашка из денима', 'denim_shirt.jpg'),
            ('Рубашка поло', 2799.99, 'Спортивная рубашка поло', 'polo_shirt2.jpg'),
            ('Рубашка шелковая', 8999.99, 'Роскошная шелковая рубашка', 'silk_shirt.jpg'),
            
            
            ('Джинсы скинни', 4999.99, 'Облегающие джинсы скинни фасон', 'skinny_jeans.jpg'),
            ('Джинсы прямые', 4599.99, 'Классические прямые джинсы', 'straight_jeans.jpg'),
            ('Брюки чинос', 3899.99, 'Универсальные брюки чинос', 'chino_pants.jpg'),
            ('Брюки классические', 5999.99, 'Классические офисные брюки', 'dress_pants.jpg'),
            ('Джинсы бойфренды', 5299.99, 'Модные джинсы бойфренды свободного кроя', 'boyfriend_jeans.jpg'),
            
            
            ('Юбка-карандаш', 4299.99, 'Элегантная юбка-карандаш для офиса', 'pencil_skirt.jpg'),
            ('Юбка миди', 3699.99, 'Стильная юбка миди длины', 'midi_skirt.jpg'),
            ('Платье коктейльное', 8999.99, 'Элегантное коктейльное платье', 'cocktail_dress.jpg'),
            ('Платье повседневное', 5999.99, 'Удобное повседневное платье', 'casual_dress.jpg'),
            ('Платье макси', 7599.99, 'Длинное платье макси', 'maxi_dress.jpg'),
            
            
            ('Свитер шерстяной', 6899.99, 'Теплый шерстяной свитер', 'wool_sweater.jpg'),
            ('Свитер кашемир', 15999.99, 'Роскошный кашемировый свитер', 'cashmere_sweater.jpg'),
            ('Кардиган вязаный', 5299.99, 'Уютный вязаный кардиган', 'knit_cardigan.jpg'),
            ('Свитер оверсайз', 5999.99, 'Модный свитер оверсайз', 'oversize_sweater.jpg'),
            ('Худи с капюшоном', 4299.99, 'Удобный худи с капюшоном', 'hoodie.jpg'),
            
            
            ('Спортивные штаны', 2799.99, 'Удобные спортивные штаны для тренировок', 'sweatpants.jpg'),
            ('Спортивный костюм', 8999.99, 'Стильный спортивный костюм', 'tracksuit.jpg'),
            ('Леггинсы спортивные', 3299.99, 'Качественные спортивные леггинсы', 'leggings.jpg'),
            ('Футболка для фитнеса', 1999.99, 'Специальная футболка для занятий спортом', 'fitness_tshirt.jpg'),
            ('Шорты спортивные', 2299.99, 'Удобные спортивные шорты', 'sport_shorts.jpg'),
            
            
            ('Шарф шерстяной', 1899.99, 'Теплый шерстяной шарф', 'wool_scarf.jpg'),
            ('Шапка вязаная', 1499.99, 'Стильная вязаная шапка', 'knit_hat.jpg'),
            ('Перчатки кожаные', 2999.99, 'Качественные кожаные перчатки', 'leather_gloves.jpg'),
            ('Ремень кожаный', 2299.99, 'Классический кожаный ремень', 'leather_belt.jpg'),
            ('Шейный платок', 999.99, 'Элегантный шейный платок', 'neck_scarf.jpg'),
            
            
            ('Кроссовки повседневные', 7999.99, 'Стильные повседневные кроссовки', 'sneakers.jpg'),
            ('Туфли классические', 12999.99, 'Элегантные классические туфли', 'dress_shoes.jpg'),
            ('Ботинки кожаные', 15999.99, 'Качественные кожаные ботинки', 'leather_boots.jpg'),
            ('Сапоги зимние', 18999.99, 'Теплые зимние сапоги', 'winter_boots.jpg'),
            ('Лоферы', 8999.99, 'Стильные лоферы для повседневной носки', 'loafers.jpg'),
            
            
            ('Комплект белья', 2999.99, 'Качественный комплект нижнего белья', 'lingerie_set.jpg'),
            ('Боди кружевное', 3999.99, 'Элегантное кружевное боди', 'lace_bodysuit.jpg'),
            ('Пижама хлопковая', 3499.99, 'Удобная хлопковая пижама', 'cotton_pajamas.jpg'),
            ('Халат банный', 4999.99, 'Мягкий банный халат', 'bathrobe.jpg'),
            ('Носки хлопковые', 499.99, 'Комфортные хлопковые носки', 'cotton_socks.jpg')
        ]
        
        for product in products:
            cursor.execute(
                'INSERT INTO product (name, price, description, image) VALUES (?, ?, ?, ?)',
                product
            )
        
        print(f" Добавлено {len(products)} товаров одежды в базу данных")
    else:
        cursor.execute('SELECT COUNT(*) as count FROM product')
        count = cursor.fetchone()[0]
        print(f"В базе данных уже есть {count} товаров")
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_tables()  
    init_products()  