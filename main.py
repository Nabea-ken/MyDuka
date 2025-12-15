from flask import Flask, render_template, request, redirect, url_for
from database import get_products,get_sales,insert_products,insert_sales,available_stock,fetch_stock,add_stock


#Flask instance
app = Flask(__name__)

# index route
@app.route("/")
def home():
    return render_template("index.html")

# Getting products
@app.route('/products')
def fetch_products():
    products = get_products()
    return render_template("products.html",products=products)

# Posting products
@app.route('/add_products',methods=['GET','POST'])
def add_products():
    product_name = request.form["product_name"]
    buying_price = request.form["buying_price"]
    selling_price = request.form["selling_price"]
    new_product = (product_name,buying_price,selling_price)
    insert_products(new_product)
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
        print("Insufficient stock!")
        return redirect(url_for('fetch_sales'))
    
    new_sale = (pid,quantity)
    insert_sales(new_sale)

    return redirect(url_for('fetch_sales'))


# Stock route
@app.route('/stock')
def get_stock():
    stock = fetch_stock()
    products = get_products()
    return render_template("stock.html",stock = stock,products = products)

# Adding stock
@app.route('/add_stock',methods=['GET','POST'])
def stock():
    pid = request.form["pid"]
    stock = int(request.form["stock"])

    new_stock = (pid,stock)
    add_stock(new_stock)

    print("Stock added")
    return redirect(url_for('stock'))


@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


@app.route("/login")
def login():
    return render_template("login.html") 


@app.route("/register")
def register():
    return render_template("register.html")


app.run(debug=True)

