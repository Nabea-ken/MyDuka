import psycopg2

conn = psycopg2.connect(host='localhost',port='5433',user='postgres',password='postgres',dbname='myduka_db')

cur = conn.cursor()

""" cur.execute("select * from products")
products = cur.fetchall()
# print(products) """

def get_products():
    cur.execute("select * from products")
    products = cur.fetchall()
    return products

products = get_products()
print(products)


""" cur.execute("insert into products(name,buying_price,selling_price)values('samsung',15000,20000)")
conn.commit()
print(products) """

def insert_products(values):
    cur.execute(f"insert into products(name,buying_price,selling_price)values{values}")
    conn.commit()

product1 = ('iphone',100000,120000)
product2 = ('hp',50000,60000)
insert_products(product1)
insert_products(product2)

#2  with tasks

def insert_sales(values):
    cur.execute(f"insert into sales(pid,quantity)values{values}")
    conn.commit()

sales1=(0,20)
sales2=(1,25)
insert_sales(sales1)
insert_sales(sales2)

def get_sales():
    cur.execute("select * from sales")
    sales = cur.fetchall()
    return sales

sales = get_sales()
print(sales)

#secure from sql injection
def insert_sales_2(values):
    cur.execute("insert into sales(pid,quantity)values(%s,%s)",(values))
    conn.commit

sale1 = (9,20)
insert_sales(sale1)

def available_stock(pid):
    cur.execute("select sum(stock_quantity) from stock where pid = %s", (pid,))
    total_stock = cur.fetchone() or 0

    # cur.execute(f'select sum(quantity) from sales where pid = {pid}')
    cur.execute("select sum(quantity) from sales where pid = %s", (pid,))

    total_sales = cur.fetchone() or 0

    return total_stock - total_sales

def fetch_stock():
    cur.execute("select * from stock")
    stock = cur.fetchall()
    return stock

def add_stock(values):
    cur.execute(f"insert into stock(pid,stock_quantity)values{values}")
    conn.commit()

# Insert Users
def insert_user(users):
    cur.execute(f"insert into users(full_name,email,phone_number,password)values{users}")
    conn.commit()

# sales_per_product
def sales_per_product():
    cur.execute(
        select products.name as p_name, sum(sales.quantity * products.selling_price) as total_sales
        from products inner join sales on products.id = sales.pid group by(p_name);
    )

    product_sales = cur.fetchall()
    return product_sales

# sales_per_day
        
# profit_per_product
def profit_per_product():
    cur.execute(
    select products.name as p_name ,sum((products.selling_price - products.buying_price) * sales.quantity) as profit from
    sales inner join products on sales.pid = products.id group by(p_name);
    )

    product_profit = cur.fetchall()
    return product_profit
    
# profit_per_day



