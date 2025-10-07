import sqlite3
from datetime import datetime

#подключение к базе данных
def get_db_connection():
    conn = sqlite3.connect('shop.db')
    conn.row_factory = sqlite3.Row
    return conn

#создание таблиц
def init_db():
    """Инициализация базы данных - создает только таблицы"""
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

#класс для запросов к продуктам
class ProductQuery:
    def all(self):
        conn = get_db_connection()
        products_data = conn.execute('SELECT * FROM product').fetchall()
        conn.close()
        
        products = []
        for row in products_data:
            product = Product()
            product.id = row['id']
            product.name = row['name']
            product.price = row['price']
            product.description = row['description']
            product.image = row['image']
            products.append(product)
        return products
    
    def get(self, product_id):
        conn = get_db_connection()
        product_data = conn.execute('SELECT * FROM product WHERE id = ?', (product_id,)).fetchone()
        conn.close()
        
        if product_data:
            product = Product()
            product.id = product_data['id']
            product.name = product_data['name']
            product.price = product_data['price']
            product.description = product_data['description']
            product.image = product_data['image']
            return product
        return None
    
    def get_or_404(self, product_id):
        product = self.get(product_id)
        if product is None:
            from flask import abort
            abort(404)
        return product

#класс для запросов к заказам
class OrderQuery:
    def all(self):
        conn = get_db_connection()
        orders_data = conn.execute('SELECT * FROM order_table ORDER BY order_date DESC').fetchall()
        conn.close()
        
        orders = []
        for row in orders_data:
            order = Order()
            order.id = row['id']
            order.customer_name = row['customer_name']
            order.customer_email = row['customer_email']
            order.customer_phone = row['customer_phone']
            order.customer_address = row['customer_address']
            order.total_amount = row['total_amount']
            order.order_date = row['order_date']
            orders.append(order)
        return orders
    
    def get(self, order_id):
        conn = get_db_connection()
        order_data = conn.execute('SELECT * FROM order_table WHERE id = ?', (order_id,)).fetchone()
        conn.close()
        
        if order_data:
            order = Order()
            order.id = order_data['id']
            order.customer_name = order_data['customer_name']
            order.customer_email = order_data['customer_email']
            order.customer_phone = order_data['customer_phone']
            order.customer_address = order_data['customer_address']
            order.total_amount = order_data['total_amount']
            order.order_date = order_data['order_date']
            return order
        return None
    
    def get_or_404(self, order_id):
        order = self.get(order_id)
        if order is None:
            from flask import abort
            abort(404)
        return order
    
    def order_by(self, field):
        self.order_field = field
        return self
    
    def filter(self, condition=None):
        return self

#класс для запросов к элементам заказа
class OrderItemQuery:
    def filter_by(self, **kwargs):
        self.filter_args = kwargs
        return self
    
    def all(self):
        conn = get_db_connection()
        
        if hasattr(self, 'filter_args') and 'order_id' in self.filter_args:
            items_data = conn.execute(
                'SELECT * FROM order_item WHERE order_id = ?', 
                (self.filter_args['order_id'],)
            ).fetchall()
        else:
            items_data = conn.execute('SELECT * FROM order_item').fetchall()
        
        conn.close()
        
        items = []
        for row in items_data:
            item = OrderItem()
            item.id = row['id']
            item.order_id = row['order_id']
            item.product_id = row['product_id']
            item.quantity = row['quantity']
            item.unit_price = row['unit_price']
            items.append(item)
        return items

#классы моделей
class Product:
    query = ProductQuery()
    
    def __init__(self, id=None, name=None, price=None, description=None, image=None):
        self.id = id
        self.name = name
        self.price = price
        self.description = description
        self.image = image
    
    def __repr__(self):
        return f'<Product {self.name}>'
    
    def get_formatted_date(self):
        """Возвращает отформатированную дату для шаблонов"""
        try:
            if self.order_date:
                if isinstance(self.order_date, str):
                    dt = datetime.fromisoformat(self.order_date)
                else:
                    dt = self.order_date
                return dt.strftime('%d.%m.%Y %H:%M')
            return ""
        except (ValueError, AttributeError):
            return self.order_date or ""

class Order:
    query = OrderQuery()
    
    def __init__(self, id=None, customer_name=None, customer_email=None, customer_phone=None, 
                 customer_address=None, total_amount=None, order_date=None):
        self.id = id
        self.customer_name = customer_name
        self.customer_email = customer_email
        self.customer_phone = customer_phone
        self.customer_address = customer_address
        self.total_amount = total_amount
        self.order_date = order_date
    
    def __repr__(self):
        return f'<Order {self.id} - {self.customer_name}>'
    
    def get_formatted_date(self):
        """Возвращает отформатированную дату для шаблонов"""
        try:
            if self.order_date:
                if isinstance(self.order_date, str):
                    dt = datetime.fromisoformat(self.order_date)
                else:
                    dt = self.order_date
                return dt.strftime('%d.%m.%Y %H:%M')
            return ""
        except (ValueError, AttributeError):
            return self.order_date or ""

class OrderItem:
    query = OrderItemQuery()
    
    def __init__(self, id=None, order_id=None, product_id=None, quantity=None, unit_price=None):
        self.id = id
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price

#функции для работы с заказами
def create_order_in_db(customer_name, customer_email, customer_phone, customer_address, total_amount):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''INSERT INTO order_table 
        (customer_name, customer_email, customer_phone, customer_address, total_amount, order_date) 
        VALUES (?, ?, ?, ?, ?, ?)''',
        (customer_name, customer_email, customer_phone, customer_address, total_amount, datetime.now().isoformat())
    )
    order_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return order_id

def add_order_item_to_db(order_id, product_id, quantity, unit_price):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO order_item (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)',
        (order_id, product_id, quantity, unit_price)
    )
    item_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return item_id

#класс для обратной совместимости с db
class Database:
    def init_app(self, app):
        pass
    
    def session(self):
        return DBSession()
    
    def create_all(self):
        init_db()

class DBSession:
    def add(self, obj):
        pass
    
    def flush(self):
        pass
    
    def commit(self):
        pass
    
    def rollback(self):
        pass

db = Database()