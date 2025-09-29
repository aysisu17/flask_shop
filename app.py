from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from models import db, Product, Order, OrderItem
import re
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'

db.init_app(app)

# Валидация данных
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_phone(phone):
    pattern = r'^(\+7|8)?[\s\-]?\(?[0-9]{3}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$'
    return re.match(pattern, phone) is not None

# Главная страница
@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

# Корзина
@app.route('/cart')
def cart():
    cart_items = []
    total = 0
    
    if 'cart' in session:
        for product_id, quantity in session['cart'].items():
            product = Product.query.get_or_404(int(product_id))
            item_total = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total
            })
            total += item_total
    
    return render_template('cart.html', cart_items=cart_items, total=total)

# Добавление в корзину
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = {}
    
    cart = session['cart']
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session['cart'] = cart
    session.modified = True
    
    flash('Товар добавлен в корзину!', 'success')
    return redirect(url_for('index'))

# Обновление корзины
@app.route('/update_cart', methods=['POST'])
def update_cart():
    if 'cart' not in session:
        session['cart'] = {}
    
    cart = session['cart']
    
    for key, value in request.form.items():
        if key.startswith('quantity_'):
            product_id = key.replace('quantity_', '')
            quantity = int(value)
            
            if quantity > 0:
                cart[product_id] = quantity
            else:
                cart.pop(product_id, None)
    
    session['cart'] = cart
    session.modified = True
    
    flash('Корзина обновлена!', 'success')
    return redirect(url_for('cart'))

# Удаление из корзины
@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    if 'cart' in session:
        cart = session['cart']
        cart.pop(str(product_id), None)
        session['cart'] = cart
        session.modified = True
        
        flash('Товар удален из корзины!', 'success')
    
    return redirect(url_for('cart'))

# Оформление заказа
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'cart' not in session or not session['cart']:
        flash('Корзина пуста!', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        # Валидация данных
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()
        
        errors = []
        
        if not name:
            errors.append('Имя обязательно для заполнения')
        if not email:
            errors.append('Email обязателен для заполнения')
        elif not is_valid_email(email):
            errors.append('Неверный формат email')
        if not phone:
            errors.append('Телефон обязателен для заполнения')
        elif not is_valid_phone(phone):
            errors.append('Неверный формат телефона')
        if not address:
            errors.append('Адрес обязателен для заполнения')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('checkout.html')
        
        # Создание заказа
        try:
            total = 0
            for product_id, quantity in session['cart'].items():
                product = Product.query.get(int(product_id))
                total += product.price * quantity
            
            order = Order(
                customer_name=name,
                customer_email=email,
                customer_phone=phone,
                customer_address=address,
                total_amount=total,
                order_date=datetime.utcnow()
            )
            
            db.session.add(order)
            db.session.flush()  # Получаем ID заказа
            
            for product_id, quantity in session['cart'].items():
                product = Product.query.get(int(product_id))
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=quantity,
                    unit_price=product.price
                )
                db.session.add(order_item)
            
            db.session.commit()
            
            # Очищаем корзину
            session.pop('cart', None)
            
            return redirect(url_for('order_confirmation', order_id=order.id))
            
        except Exception as e:
            db.session.rollback()
            flash('Произошла ошибка при создании заказа. Попробуйте еще раз.', 'error')
            return render_template('checkout.html')
    
    return render_template('checkout.html')

# Страница подтверждения заказа
@app.route('/order_confirmation/<int:order_id>')
def order_confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('order_confirmation.html', order=order)

# Административная панель
@app.route('/admin')
def admin():
    orders = Order.query.order_by(Order.order_date.desc()).all()
    
    # Фильтрация по дате
    date_filter = request.args.get('date')
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d')
            orders = Order.query.filter(
                db.func.date(Order.order_date) == filter_date.date()
            ).order_by(Order.order_date.desc()).all()
        except ValueError:
            pass
    
    # Поиск по email
    email_search = request.args.get('email')
    if email_search:
        orders = Order.query.filter(
            Order.customer_email.ilike(f'%{email_search}%')
        ).order_by(Order.order_date.desc()).all()
    
    return render_template('admin.html', orders=orders)

# Обработчики ошибок
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)