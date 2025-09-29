from app import app, db, Product

def init_database():
    with app.app_context():
        # Создаем таблицы
        db.create_all()
        
        # Добавляем тестовые товары
        if not Product.query.first():
            products = [
                Product(name='iPhone 14', price=999, description='Новый iPhone 14 с улучшенной камерой'),
                Product(name='MacBook Pro', price=1999, description='Мощный ноутбук для профессионалов'),
                Product(name='AirPods Pro', price=249, description='Беспроводные наушники с шумоподавлением'),
                Product(name='iPad Air', price=599, description='Универсальный планшет'),
                Product(name='Apple Watch', price=399, description='Умные часы для активного образа жизни')
            ]
            
            for product in products:
                db.session.add(product)
            
            db.session.commit()
            print('База данных инициализирована с тестовыми данными!')

if __name__ == '__main__':
    init_database()