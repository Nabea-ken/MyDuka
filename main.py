#Imports
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for,flash,session
from database import get_products,get_sales,insert_products,insert_sales,available_stock,fetch_stock,add_stock,check_user_exists,insert_users
from flask_bcrypt import Bcrypt

#Flask instance
app = Flask(__name__)

# Object instance of Bcrypt()
bcrypt = Bcrypt(app)

# Secret key - signs session data
app.secret_key = 'qwertyuioplkjhgfdsazxcvbnm'

# index route
@app.route("/")
def home():
    return render_template("index.html")

def login_required(f):
    @wraps(f)
    def protected(*args,**kwargs):
        if 'email' not in session:
            return redirect(url_for('login'))
        return f(*args,**kwargs)
    return protected

# Getting products
@app.route('/products')
@login_required
def fetch_products():
    products = get_products()

    return render_template("products.html",products=products)


# Inserting products
@app.route('/add_products',methods=['GET','POST'])
def add_products():
    product_name = request.form["product_name"]
    buying_price = request.form["buying_price"]
    selling_price = request.form["selling_price"]

    new_product = (product_name,buying_price,selling_price)
    insert_products(new_product)
    flash("Product added successfully",'success')

    return redirect(url_for('fetch_products'))

# the psql create table sales query, created_at is default
# the primary key is always serialized
""" 
CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    pid INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
); """

# Getting sales
@app.route('/sales')
def fetch_sales():
    sales = get_sales()
    products = get_products()

    return render_template("sales.html",sales=sales,products=products)


# Posting sales
@app.route('/add_sales',methods=['GET','POST'])
def add_sales():
    pid = request.form["pid"]
    quantity = int(request.form["quantity"])

    check_stock = available_stock(pid)

    if check_stock < quantity:
        flash("Insufficient stock!",'danger')
        return redirect(url_for('fetch_sales'))
    
    new_sale = (pid,quantity)
    insert_sales(new_sale)
    flash("Sale made successfully",'success')

    return redirect(url_for('fetch_sales'))


# Stock route
@app.route('/stock')
def get_stock():
    stock = fetch_stock()
    products = get_products()

    return render_template("stock.html",stock = stock,products = products)


# Adding stock
@app.route('/add_stock',methods=['GET','POST'])
def insert_stock():
    pid = request.form["pid"]
    s_quantity = int(request.form["s_quantity"])

    new_stock = (pid,s_quantity)
    add_stock(new_stock)

    print("Stock added")
    return redirect(url_for('get_stock'))

# User dashboard
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

# User Login
@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        registered_user = check_user_exists(email)
        if not registered_user:
            flash("User with this email doesnt exist, Register",'danger')
        else:
            if bcrypt.check_password_hash(registered_user[-1],password):
                flash("Login successfull",'success')
                session['email'] = email
                return redirect(url_for('dashboard'))
            else:
                flash("Password incorrect!",'danger')

    return render_template("login.html") 

# User create account
@app.route("/register",methods=['GET','POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone']
        password = request.form['password']

        existing_user = check_user_exists(email)
        if not existing_user:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = (full_name,email,phone_number,hashed_password)
            insert_users(new_user)
            flash("User registered successfully",'success')
            return redirect(url_for('login'))
        else:
            flash("Email already exists!",'danger')

    return render_template("register.html")

# Starts flask dev server and auto reload on code changes(remove debug=true when ready for production)
app.run(debug=True)

