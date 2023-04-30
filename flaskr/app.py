from flask import Flask, render_template, request,  flash, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required,current_user
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.security import generate_password_hash,check_password_hash
import os
from wtforms.validators import InputRequired
from flask_mysqldb import MySQL
import mysql.connector
import MySQLdb.cursors
from datetime import datetime
import requests

#function to translate a string to other language
def translate(s,o,i):
    url = "https://microsoft-translator-text.p.rapidapi.com/translate"

    querystring = {"to[0]":i,"api-version":"3.0","from":o,"profanityAction":"NoAction","textType":"plain"}

    payload = [{ "Text": s}]
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "7e614f520bmsh1c97a2bc5ec852cp1f6cc7jsned56cc8e2fd2",
        "X-RapidAPI-Host": "microsoft-translator-text.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers, params=querystring)
    return response.text[27:-15]



app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = "achyut"
app.config['MYSQL_HOST'] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "achyut"
app.config["MYSQL_DB"] = "salesquaredb"
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'
mysql = MySQL(app)

# Stuff for Security of the User

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Functions to add images in static Folder

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class UploadFileForm(FlaskForm):
    file1 = FileField('File 1', validators=[InputRequired()])
    file2 = FileField('File 2', validators=[InputRequired()])
    file3 = FileField('File 3', validators=[InputRequired()])
    file4 = FileField('File 4', validators=[InputRequired()])
    submit = SubmitField('Submit')
     
@app.route('/addimage', methods=['GET',"POST"])
def addimage():
    userid = request.args.get('userid')
    productid = request.args.get('productid')
    form = UploadFileForm()
    if form.validate_on_submit():
        file1 = form.file1.data
        file2 = form.file2.data
        file3 = form.file3.data
        file4 = form.file4.data

        filename1 = f"{productid}@1.jpg"
        filename2 = f"{productid}@2.jpg"
        filename3 = f"{productid}@3.jpg"
        filename4 = f"{productid}@4.jpg"

        file1.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],filename1))
        file2.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],filename2))
        file3.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],filename3))
        file4.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],filename4))
        return redirect(url_for('my_products'))
    return render_template('addimage.html', form=form)

# Render Security page

@app.route('/security')
@login_required
def security():
    userid = current_user.id
    return render_template('security.html',userid=userid)

# Render contact page

@app.route('/contact')
@login_required
def contact():
    userid = current_user.id
    return render_template('contact.html',userid=userid)

# Render Return Policy page

@app.route('/returnPolicy')
@login_required
def returnPolicy():
    userid = current_user.id
    return render_template('returnPolicy.html',userid=userid)

#this function returns index page of website

@app.route('/', methods = ['GET', 'POST'])
def index():
    # Fetch data from 'users' table
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM electronics LIMIT 4")
    elec = cursor.fetchall()
    cursor.execute("SELECT * FROM beauty LIMIT 4")
    beau = cursor.fetchall()
    cursor.execute("SELECT * FROM fashion LIMIT 4")
    fas = cursor.fetchall()
    cursor.close()
    return render_template('index.html',elec=elec,beau=beau,fas=fas)

#this is home page after logging in
 
@app.route('/home', methods = ['GET', 'POST'])
@login_required
def home(): 
    userid = current_user.id
    if request.method == 'POST':
        return redirect(url_for(search ))
    cursor = mysql.connection.cursor()
    cursor.execute(f"SELECT * FROM electronics LIMIT 4")
    elec = cursor.fetchall()
    cursor.execute(f"SELECT * FROM beauty LIMIT 4")
    beau = cursor.fetchall()
    cursor.execute(f"SELECT * FROM fashion LIMIT 4")
    fas = cursor.fetchall()
    cursor.close()
    return render_template('home.html',elec=elec,beau=beau,fas=fas, userid = userid)

#this to show signup page after logging in 

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        em = email.split("@")[0]
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if len(password) < 8:
            flash('Password strength is too low!' , 'error')
            return redirect(url_for('signup'))
        elif user:
            flash('Email already exists, please use a different email address.', 'error')
            return redirect(url_for('signup'))
        elif password != confirm_password:
            flash('Passwords do not match, please try again.', 'error')
            return redirect(url_for('signup'),)
        else:
            k = email.split("@")
            supplierid = k[0]
            password = generate_password_hash(password, method='sha256')
            cursor.execute("INSERT INTO users (name, email, password,supplierid) VALUES (%s, %s, %s, %s)", (name, email, password, supplierid))
            mysql.connection.commit()
            cursor.close()
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("USE cart")
            cursor.execute("CREATE TABLE {} LIKE sample".format(em))
            cursor.execute("USE orders")
            cursor.execute("CREATE TABLE {} LIKE sample".format(em))
            cursor.execute("USE supplies")
            cursor.execute("CREATE TABLE {} LIKE sample".format(em))
            cursor.execute("USE address")
            cursor.execute("CREATE TABLE {} LIKE sample".format(em))
            cursor.execute("USE salesquaredb")
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('login'))
    return render_template('signup.html')

# this function to show login and enter the user in current session in the device

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("show databases")
        email = request.form.get('email')
        password = request.form.get('password')
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        mysql.connection.commit()
        cursor.close()
        if user!=None:
            if not check_password_hash(user[2], password):
                flash("wrong password", 'error')
                return redirect(url_for('login'))
            else:
                mysql.connection.commit()
                cursor.close()
                k = email.split("@")
                userid = k[0]
                user = User(userid)
                login_user(user)
                return redirect(url_for('home'))
        else:
            flash("email doesn't exist, please signup.", 'error')
    return render_template('login.html')

# Function to remove user from current Session of the device

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Render Team Page

@app.route('/team.html')
@login_required
def team():
    userid = current_user.id
    return render_template('team.html',userid=userid )

# Show sell categories on the site

@app.route('/sellcategory')
@login_required
def sell():
    userid = current_user.id
    return render_template('categories_sell.html',userid=userid)

# show buy categories on the site 

@app.route('/buycategory')
@login_required
def buy():
    userid = current_user.id
    return render_template('categories_buy.html',userid=userid)

# Forms to add Products

@app.route('/formelectronics', methods = ['GET','POST'])
@login_required
def add_electronics():
    userid = current_user.id
    if request.method == 'POST':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("show databases")
        name_product = request.form.get('name_product')
        price = request.form.get('price')
        desc = request.form.get('desc')
        category = "electronics"
        now = datetime.now()
        productid = now.strftime("%Y%m%d%H%M%S")
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO electronics (productname,unit_price,description,productid,supplierid) VALUES (%s, %s, %s, %s,%s)",(name_product,price,desc,productid,userid))
        cursor.execute("INSERT INTO products (productname,unit_price,description,category,productid,supplierid) VALUES (%s, %s, %s, %s, %s ,%s)",(name_product,price,desc,category,productid,userid))       
        mysql.connection.commit()
        cursor.close()
        # flash('Product Added Successfully', 'success')
        return redirect(url_for('addimage',productid=productid))
    return render_template('formelectronics.html',userid=userid )

@app.route('/formbeauty', methods = ['GET','POST'])
@login_required
def add_beauty():
    userid = current_user.id
    if request.method == 'POST':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("show databases")
        name_product = request.form.get('name_product')
        price = request.form.get('price')
        desc = request.form.get('desc')
        category = "beauty"
        now = datetime.now()
        productid = now.strftime("%Y%m%d%H%M%S")
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO beauty (productname,unit_price,description,productid,supplierid) VALUES (%s, %s, %s, %s,%s)",(name_product,price,desc,productid,userid))
        cursor.execute("INSERT INTO products (productname,unit_price,description,category,productid,supplierid) VALUES (%s, %s, %s, %s, %s ,%s)",(name_product,price,desc,category,productid,userid))        
        mysql.connection.commit()
        cursor.close()
        # flash('Product Added Successfully', 'success')
        return redirect(url_for('addimage', productid=productid))
    return render_template('formbeauty.html',userid = userid)

@app.route('/formfashion', methods = ['GET','POST'])
@login_required
def add_fashion():
    userid = current_user.id
    if request.method == 'POST':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("show databases")
        name_product = request.form.get('name_product')
        price = request.form.get('price')
        desc = request.form.get('desc')
        category = "fashion"
        now = datetime.now()
        productid = now.strftime("%Y%m%d%H%M%S")
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO fashion (productname,unit_price,description,productid,supplierid) VALUES (%s, %s, %s, %s,%s)",(name_product,price,desc,productid,userid))
        cursor.execute("INSERT INTO products (productname,unit_price,description,category,productid,supplierid) VALUES (%s, %s, %s, %s, %s ,%s)",(name_product,price,desc,category,productid,userid))         
        mysql.connection.commit()
        cursor.close()
        # flash('Product Added Successfully', 'success')
        return redirect(url_for('addimage', productid=productid))
    return render_template('formfashion.html',userid=userid)

@app.route('/formhome', methods = ['GET','POST'])
@login_required
def add_home():
    userid = current_user.id
    if request.method == 'POST':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("show databases")
        name_product = request.form.get('name_product')
        price = request.form.get('price')
        desc = request.form.get('desc')
        category = "homeandkitchen"
        now = datetime.now()
        productid = now.strftime("%Y%m%d%H%M%S")
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO homeandkitchen (productname,unit_price,description,productid,supplierid) VALUES (%s, %s, %s, %s, %s)",(name_product,price,desc,productid,userid))
        cursor.execute("INSERT INTO products (productname,unit_price,description,category,productid,supplierid) VALUES (%s, %s, %s, %s, %s, %s)",(name_product,price,desc,category,productid,userid))       
        mysql.connection.commit()
        cursor.close()
        # flash('Product Added Successfully', 'success')
        return redirect(url_for('addimage', productid=productid))
    return render_template('formhome.html',userid=userid)

@app.route('/formsports', methods = ['GET','POST'])
@login_required
def add_sports():
    userid = current_user.id
    if request.method == 'POST':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("show databases")
        name_product = request.form.get('name_product')
        price = request.form.get('price')
        desc = request.form.get('desc')
        category = "sports"
        now = datetime.now()
        productid = now.strftime("%Y%m%d%H%M%S")
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO sports (productname,unit_price,description,productid,supplierid) VALUES (%s, %s, %s, %s , %s)",(name_product,price,desc,productid,userid))
        cursor.execute("INSERT INTO products (productname,unit_price,description,category,productid,supplierid) VALUES (%s, %s, %s, %s, %s, %s)",(name_product,price,desc,category,productid,userid))       
        mysql.connection.commit()
        cursor.close()
        # flash('Product Added Successfully', 'success')
        return redirect(url_for('addimage', productid=productid))
    return render_template('formsports.html',userid=userid)

@app.route('/formbooks', methods = ['GET','POST'])
@login_required
def add_books():
    userid = current_user.id
    if request.method == 'POST':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("show databases")
        name_product = request.form.get('name_product')
        price = request.form.get('price')
        desc = request.form.get('desc')
        category = "books"
        now = datetime.now()
        productid = now.strftime("%Y%m%d%H%M%S")
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO books (productname,unit_price,description,productid,supplierid) VALUES (%s, %s, %s, %s, %s)",(name_product,price,desc,productid,userid))
        cursor.execute("INSERT INTO products (productname,unit_price,description,category,productid,supplierid) VALUES (%s, %s, %s, %s, %s, %s)",(name_product,price,desc,category,productid,userid))       
        mysql.connection.commit()
        cursor.close()
        # flash('Product Added Successfully', 'success')
        return redirect(url_for('addimage', productid=productid))
    return render_template('formbooks.html',userid=userid)

# show product description 

@app.route('/product', methods =['GET','POST'] )
@login_required
def product():
    userid = current_user.id
    productid = request.args.get('productid')
    cursor = mysql.connection.cursor()
    cursor.execute("use salesquaredb")
    cursor.execute("SELECT * FROM products WHERE productid = %s",(productid,))
    product = cursor.fetchone()
    info=product[3]
    info_list = info.split(".")
    if request.method=='POST':
        lang_o=request.form.get("lang")
        if lang_o=="hindi":
            info = ""
            for sent in info_list:
                x=translate(str(sent),'en','hi')
                info = info + x + "."
    cursor.close()
    return render_template("product.html",product=product,userid=userid,info=info)

# add a product to cart

@app.route('/addedtocart', methods =['GET','POST'] )
@login_required
def addtocart_productpage():
    userid = current_user.id
    productid = request.args.get("productid")
    cursor = mysql.connection.cursor()
    cursor.execute("USE cart")
    cursor.execute(f"SELECT * FROM {userid} WHERE productid = {productid}")
    item = cursor.fetchone()
    if item==None:
        quantity = 1
        cursor.execute(f"INSERT INTO {userid} (productid,quantity) VALUES ({productid}, {quantity})")
    else:
        quantity = item[1]
        quantity += 1
        cursor.execute(f"UPDATE {userid} SET productid = {productid}, quantity = {quantity} WHERE productid={productid}")
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('product',productid=productid))

@app.route('/myOrders')
@login_required
def myOrders():
    userid = current_user.id
    cursor = mysql.connection.cursor()
    cursor.execute("USE orders")
    cursor.execute(f"SELECT * FROM {userid}")
    orderids = cursor.fetchall()
    products=[]
    for item in orderids:
        cursor.execute("USE orderinfo")
        cursor.execute(f"SELECT * FROM {item[0]}")
        pro = cursor.fetchall()
        for item in pro:
            products.append(item)
    ducts = []
    cursor.execute("USE salesquaredb")
    for item in products:
        cursor.execute("SELECT * FROM products WHERE productid=%s",(item[0],))
        po = cursor.fetchone()
        l = [po,item]
        ducts.append(l)
    mysql.connection.commit()
    cursor.close()
    return render_template('myOrders.html',userid=userid,ducts=ducts,products=products)

# add order in database

@app.route('/addorders', methods =['GET','POST'])
@login_required
def add_orders():
    userid = current_user.id
    addressid = request.form.get('addressid')
    status = "Out for Delivery"
    cursor = mysql.connection.cursor()
    cursor.execute("USE cart")
    cursor.execute(f"SELECT * from {userid}")
    products = cursor.fetchall()
    cursor.execute(f"delete from {userid}")
    now = datetime.now()
    orderid = "o"+now.strftime("%d%m%Y%H%M%S")
    cursor.execute('USE orders')
    cursor.execute(f"INSERT INTO {userid} (orderid) VALUES ('{orderid}')")
    cursor.execute("use salesquaredb")
    sellers = []
    for item in products:
        cursor.execute(f"SELECT supplierid FROM products WHERE productid='{item[0]}'")
        seller = cursor.fetchone()
        sellers.append(seller[0])
    cursor.execute("USE orderinfo")
    cursor.execute(f"CREATE TABLE {orderid} LIKE sample")
    for item in range(len(products)):
        cursor.execute(f"INSERT INTO {orderid} (productid,quantity,seller,buyer,status) VALUES ('{products[item][0]}',{products[item][1]},'{sellers[item]}','{userid}','{status}')")
    cursor.execute("use supplies")
    sellers_refined = set(sellers)
    for seller in sellers_refined:
        cursor.execute(f"Insert into {seller} (orderid,addressid) VALUES ('{orderid}','{addressid}')")
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('cart'))

@app.route('/mySupplies',methods=['GET','POST'])
@login_required
def mySupplies():
    userid = current_user.id
    cursor = mysql.connection.cursor()
    cursor.execute(" USE supplies")
    cursor.execute(f"SELECT * FROM {userid}")
    supplies = cursor.fetchall()
    supp=[]
    for item in supplies:
        orderid = item[0]
        adid = item[1]
        cursor.execute("USE salesquaredb")
        cursor.execute("SELECT * from address WHERE addressid=%s",(adid,))
        add = cursor.fetchone()
        cursor.execute("use orderinfo")
        cursor.execute(f"select status from {orderid} where seller='{userid}'")
        status = cursor.fetchone()
        supp.append([item,add, status[0]])
    supp.reverse()
    return render_template('mySupplies.html',supp=supp,userid=userid)

# select a address for the for order

@app.route('/checkout', methods=['GET','POST']) 
@login_required
def checkout():
    userid = current_user.id
    if request.method=="POST":
        return redirect(url_for('add_orders'))
    cursor = mysql.connection.cursor()
    cursor.execute("USE address")
    cursor.execute(f"SELECT * FROM {userid}")
    address = cursor.fetchall()
    cursor.execute(" USE cart ")
    cursor.execute(f"SELECT * FROM {userid}")
    orders = cursor.fetchall()
    cursor.execute("USE salesquaredb")
    products = []
    for item in orders:
        i_d = item[0]
        quantity = item[1]
        cursor.execute("SELECT * from products WHERE productid = %s ",(i_d,))
        pro = cursor.fetchone()
        pro = pro + tuple([quantity])
        products.append(pro)
    total = 50
    for item in products:
        total=total + item[2]*item[-1]
    cursor.execute("USE salesquaredb")
    cursor.execute("SELECT * FROM users WHERE supplierid = %s",(userid,))
    user = cursor.fetchone()
    return render_template("checkout.html",user=user,userid=userid,products=products,address=address,total=total)
    
# show all products in cart

@app.route('/cart')
@login_required
def cart():
    userid = current_user.id
    cursor = mysql.connection.cursor()
    cursor.execute("USE cart")
    cursor.execute(f"SELECT * FROM {userid}")
    cart = cursor.fetchall()
    cursor.execute("USE salesquaredb")
    products = []
    for item in cart:
        i_d = item[0]
        quantity = item[1]
        cursor.execute("SELECT * from products WHERE productid = %s ",(i_d,))
        pro = cursor.fetchone()
        pro = pro + tuple([quantity])
        products.append(pro)
    total = 50
    for item in products:
        total=total + item[2]*item[-1]
    mysql.connection.commit()
    cursor.close()
    return render_template("cart.html",products=products,userid=userid,total=total)

# if cart is empty redirect it back to cart

@app.route('/is_Empty')
@login_required
def is_cart_empty():
    userid = current_user.id
    cursor = mysql.connection.cursor()
    cursor.execute("USE cart")
    cursor.execute(f"SELECT * FROM {userid}")
    cart = cursor.fetchall()
    if len(cart)==0:
        flash("CART is empty")
        return redirect(url_for('cart'))
    else:
        return redirect(url_for('checkout'))

@app.route('/edit_status', methods=['GET','POST']) 
@login_required
def edit_status():
    userid = current_user.id
    status = request.form.get('status')
    orderid = request.args.get('orderid')
    cursor = mysql.connection.cursor()
    cursor.execute("USE orderinfo")
    cursor.execute(f"UPDATE {orderid} SET status='{status}' WHERE seller = %s",(userid,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('mySupplies'))

# add a new address to user

@app.route('/add_address', methods = ['GET','POST'])
@login_required
def add_address():
    userid = current_user.id
    if request.method == 'POST':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("USE address")
        appartment = request.form.get('appartment')
        street = request.form.get('street')
        landmark = request.form.get('landmark')
        town = request.form.get('town')
        state = request.form.get('state')
        pincode = request.form.get('pincode')
        now = datetime.now()
        addressid = now.strftime("%Y%m%d%H%M%S")
        cursor = mysql.connection.cursor()
        cursor.execute(f"INSERT INTO {userid} (addressid,appartment,street,landmark,town,state,pincode) VALUES ('{addressid}','{appartment}','{street}','{landmark}','{town}','{state}',{pincode})") 
        cursor.execute("USE salesquaredb")
        cursor.execute(f"INSERT INTO address (addressid,appartment,street,landmark,town,state,pincode) VALUES ('{addressid}','{appartment}','{street}','{landmark}','{town}','{state}',{pincode})") 
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('show_personal'))
    return render_template('formaddress.html',userid=userid )    

@app.route('/products',methods=['GET','POST'])
@login_required
def products():
    userid = current_user.id
    cat=request.args.get('category')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("USE salesquaredb")
    cursor.execute(f"SELECT * FROM {cat} WHERE supplierid != %s",(userid,))
    prod = cursor.fetchall()
    mysql.connection.commit()
    cursor.close()
    return render_template("products.html",prod=prod,userid=userid)

@app.route('/showpersonal')
@login_required
def show_personal():
    userid = current_user.id
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE supplierid=%s",(userid,))
    user = cursor.fetchone()
    cursor.execute("USE address")
    cursor.execute(f"SELECT * FROM {userid}")
    address = cursor.fetchall()
    cursor.close()
    return render_template("profile.html",user=user,userid=userid,address=address)

# edit presonal details of user

@app.route('/editpersonal', methods = ['GET','POST'])
@login_required
def add_personal():
    userid = current_user.id
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("USE salesquaredb")
    user = cursor.execute("SELECT * FROM users where supplierid = %s",(userid,))
    if request.method == 'POST':
        cursor.execute("USE salesquaredb")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        mobile_no = request.form.get("mobile_no")
        if len(str(mobile_no))>10:
            flash("please enter a valid phone no",'error')
            return redirect(url_for('add_personal'))
        cursor.execute(f"UPDATE users SET firstname='{firstname}', lastname='{lastname}', mobile_no={mobile_no} WHERE supplierid='{userid}'")
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('show_personal'))
    return render_template('editpersonal.html',userid=userid,user=user)
        
@app.route("/del_address")
@login_required
def del_address():
    userid = current_user.id
    addressid = request.args.get('addressid')
    cursor = mysql.connection.cursor()
    cursor.execute("USE address")
    cursor.execute(f"DELETE FROM {userid} WHERE addressid={addressid}")
    cursor.execute("USE salesquaredb")
    cursor.execute(f"DELETE FROM address WHERE addressid={addressid}")
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('show_personal'))     

@app.route("/cart_plus")
@login_required
def plus():
    userid = current_user.id
    productid = request.args.get('productid')
    cursor = mysql.connection.cursor()
    cursor.execute("USE cart")
    cursor.execute(f"SELECT * from {userid} WHERE productid = {productid}")
    item = cursor.fetchone()
    quantity = item[1]+1
    cursor.execute(f"UPDATE {userid} SET productid = {productid}, quantity = {quantity} WHERE productid = {productid}")
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('cart'))

@app.route("/cart_minus")
@login_required
def minus():
    userid = current_user.id
    productid = request.args.get('productid')
    cursor = mysql.connection.cursor()
    cursor.execute("USE cart")
    cursor.execute(f"SELECT * from {userid} WHERE productid = %s",(productid,))
    item = cursor.fetchone()
    quantity = item[1]-1
    if item[1]==1:
        cursor.execute(f"DELETE FROM {userid} WHERE productid={productid}")
    else:
        cursor.execute(f"UPDATE {userid} SET productid = {productid}, quantity = {quantity} WHERE productid = {productid}")
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('cart'))

# show all the supplies of the user

@app.route("/show_supplies")
@login_required
def show_supplies():
    userid = current_user.id
    orderid = request.args.get('orderid')
    cursor = mysql.connection.cursor()
    cursor.execute('USE orderinfo')
    cursor.execute(f"SELECT * FROM {orderid} WHERE seller = %s",(userid,))
    supp_products = cursor.fetchall()
    ducts = []
    cursor.execute("USE salesquaredb")
    for item in supp_products:
        cursor.execute("SELECT * FROM products WHERE productid=%s",(item[0],))
        po = cursor.fetchone()
        l = [po,item]
        ducts.append(l)
    mysql.connection.commit()
    cursor.close()
    ducts.reverse()
    return render_template('show_supplies.html',ducts=ducts,userid=userid)

# shows all the products of user on site

@app.route("/my_products")
@login_required
def my_products():
    userid = current_user.id
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(f"SELECT * FROM products WHERE supplierid = '{userid}'")
    product = cursor.fetchall()
    return render_template('my_products.html',prod=product,userid=userid)

# delete a product from site

@app.route('/delete_prod', methods = ['GET','POST'])
@login_required
def delete_product():
    userid = current_user.id
    productid = request.args.get('productid')
    cursor = mysql.connection.cursor()
    cursor.execute(f"SELECT * FROM products where productid={productid}")
    category = cursor.fetchone()[-2]
    cursor.execute(f"DELETE FROM products WHERE productid=%s",(productid,))
    cursor.execute(f"DELETE FROM {category} WHERE productid=%s",(productid,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('my_products'))

# Search function on site

@app.route('/search', methods = ['GET','POST'])
@login_required
def search():
    userid = current_user.id
    search_con = request.form.get('search_con')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("USE salesquaredb")
    cursor.execute(f"SELECT * FROM products WHERE productname LIKE '%{search_con}%'")
    prod = cursor.fetchall()
    return render_template('products.html',prod=prod,userid=userid)

if __name__ == '__main__':
    app.run(debug=True)
    # thank you :)