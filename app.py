from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

with app.app_context():
    db.create_all()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting the task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error updating the task.'

    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)


# from flask import Flask, render_template, request, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
# db = SQLAlchemy(app)

# class Product(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.String(500))
#     price = db.Column(db.Float, nullable=False)
#     image = db.Column(db.String(200))
#     category = db.Column(db.String(50))

# class Order(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(100), nullable=False)
#     address = db.Column(db.String(500), nullable=False)
#     city = db.Column(db.String(100), nullable=False)
#     state = db.Column(db.String(100), nullable=False)
#     zip_code = db.Column(db.String(10), nullable=False)
#     products = db.relationship('Product', secondary='order_product', backref=db.backref('orders', lazy=True))

# order_product = db.Table('order_product',
#     db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
#     db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
# )

# @app.route('/')
# def index():
#     products = Product.query.all()
#     return render_template('index.html', products=products)

# @app.route('/product/<int:id>')
# def product(id):
#     product = Product.query.filter_by(id=id).first()
#     return render_template('product.html', product=product)

# @app.route('/cart')
# def cart():
#     cart = request.cookies.get('cart')
#     if cart:
#         cart_items = []
#         total_price = 0
#         cart_list = cart.split(',')
#         for item in cart_list:
#             product_id, quantity = item.split(':')
#             product = Product.query.filter_by(id=product_id).first()
#             if product:
#                 cart_items.append((product, int(quantity)))
#                 total_price += product.price * int(quantity)
#         return render_template('cart.html', cart_items=cart_items, total_price=total_price)
#     else:
#         return render_template('cart.html', cart_items=[], total_price=0)

# @app.route('/add-to-cart', methods=['POST'])
# def add_to_cart():
#     product_id = request.form['product_id']
#     quantity = request.form['quantity']
#     cart = request.cookies.get('cart')
#     if cart:
#         cart += ',' + product_id + ':' + quantity
#     else:
#         cart = product_id + ':' + quantity
#     response = make_response(redirect(url_for('cart')))
#     response.set_cookie('cart', cart)
#     return response

# @app.route('/checkout', methods=['GET', 'POST'])
# def checkout():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         address = request.form['address']
#         city = request.form['city']
#         state = request.form['state']
#         zip_code = request.form['zip_code']
#         cart = request.cookies.get('cart')
#         if cart:
#             cart_list = cart.split(',')
#             products = []
#             for item in cart_list:
#                 product_id, quantity
