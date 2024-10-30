from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import SignupForm
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'af28689bef75a9ab648b001c4381a13244e71bd858d73feb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1/demo'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Setup Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirect to login if not logged in

class User(UserMixin, db.Model):
    user_id = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    middle_name = db.Column(db.String(50))
    gender = db.Column(db.String(10))
    address = db.Column(db.Text)
    date_of_birth = db.Column(db.Date)
    phone_number = db.Column(db.String(15))
    email = db.Column(db.String(100))

    def get_id(self):
        return self.user_id

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    unit_price = db.Column(db.Float)
    quantity = db.Column(db.Integer)

@app.route('/products', methods=['GET', 'POST'])
@login_required
def products():
    products = Products.query.all()  # Fetch all products from the database
    return render_template('products.html', products=products)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(
            user_id=form.user_id.data,
            password=hashed_password,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            middle_name=form.middle_name.data,
            gender=form.gender.data,
            address=form.address.data,
            date_of_birth=form.date_of_birth.data,
            phone_number=form.phone_number.data,
            email=form.email.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Signup successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        user = User.query.filter_by(user_id=user_id).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)  # Log the user in
            flash('Login successful!', 'success')
            return redirect(url_for('products'))  # Redirect to home page
        else:
            flash('Invalid User ID or Password. Please try again or sign up.', 'danger')
    return render_template('login.html')


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    # Ensure the session is being accessed correctly
    cart = session.get('cart', {})
    
    # Process the cart data (e.g., calculate totals)
    total_cost = sum(item['price'] * item['quantity'] for item in cart.values())
    
    return render_template('checkout.html', cart=cart, total_cost=total_cost)

def add_to_cart(product_id, product_name, unit_price):
    cart = session.get('cart', {})
    if product_id in cart:
        cart[product_id]['quantity'] += 1
    else:
        cart[product_id] = {'name': product_name, 'price': unit_price, 'quantity': 1}
    
    session['cart'] = cart

if __name__ == '__main__':
    db.create_all()  # Create database tables if they don't exist
    app.run(debug=True)