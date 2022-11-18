import os
import ibm_db
from werkzeug.utils import secure_filename
from flask import Flask, render_template , request , redirect, session

app = Flask(__name__, static_url_path='/static')
UPLOAD_FOLDER = './static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'any'

conn_str='DATABASE=bludb;HOSTNAME=9938aec0-8105-433e-8bf9-0fbb7e483086.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32459;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;uid=bbf86602;pwd=iAjizpHEzfYvlS6v'
conn = ibm_db.connect(conn_str,'','')


# @app.route("/db",methods=['GET'])
# def db():
#    sql = "create table products (id integer not null GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),name varchar(500),rate int,stock int,img varchar(500),desc varchar(500),cat varchar(125),PRIMARY KEY (id));"
#    sql = "create table orders (id integer not null GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),userid varchar(200),productid varchar(250),data varchar(225),payment varchar(125),PRIMARY KEY (id));"
#    sql = "create table users (id integer not null GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),name varchar(500),email varchar(500),password varchar(225),mob varchar(125),address varchar(500),PRIMARY KEY (id));"
#    stmt = ibm_db.exec_immediate(conn, sql)
#    return "ok"

# Without Account
@app.route("/",methods=["GET"])
def index():
   data = []
   sql = "SELECT * FROM products WHERE cat = 'WOMEN' ORDER BY id"
   stmt = ibm_db.exec_immediate(conn, sql)
   dictionary = ibm_db.fetch_both(stmt)
   while dictionary != False:
      data.append(dictionary)
      dictionary = ibm_db.fetch_both(stmt)

   newdata = []
   sql = "SELECT * FROM products WHERE cat = 'WOMEN' ORDER BY id desc LIMIT 4"
   stmt = ibm_db.exec_immediate(conn, sql)
   dictionar = ibm_db.fetch_both(stmt)
   while dictionar != False:
      newdata.append(dictionar)
      dictionar = ibm_db.fetch_both(stmt)

   return render_template("index.html",data = data , newdata = newdata)

@app.route("/men",methods=["GET"])
def index_men():
   data = []
   sql = "SELECT * FROM products WHERE cat = 'MEN' ORDER BY id"
   stmt = ibm_db.exec_immediate(conn, sql)
   dictionary = ibm_db.fetch_both(stmt)
   while dictionary != False:
      data.append(dictionary)
      dictionary = ibm_db.fetch_both(stmt)

   newdata = []
   sql = "SELECT * FROM products WHERE cat = 'MEN' ORDER BY id desc LIMIT 4"
   stmt = ibm_db.exec_immediate(conn, sql)
   dictionar = ibm_db.fetch_both(stmt)
   while dictionar != False:
      newdata.append(dictionar)
      dictionar = ibm_db.fetch_both(stmt)

   return render_template("men.html",data = data , newdata = newdata)

@app.route("/kids",methods=["GET"])
def index_kids():
   data = []
   sql = "SELECT * FROM products WHERE cat = 'KIDS' ORDER BY id"
   stmt = ibm_db.exec_immediate(conn, sql)
   dictionary = ibm_db.fetch_both(stmt)
   while dictionary != False:
      data.append(dictionary)
      dictionary = ibm_db.fetch_both(stmt)

   newdata = []
   sql = "SELECT * FROM products WHERE cat = 'KIDS' ORDER BY id desc  LIMIT 4"
   stmt = ibm_db.exec_immediate(conn, sql)
   dictionar = ibm_db.fetch_both(stmt)
   while dictionar != False:
      newdata.append(dictionar)
      dictionar = ibm_db.fetch_both(stmt)

   return render_template("kids.html",data = data , newdata = newdata)


@app.route("/product/<id>",methods=["GET"])
def product(id):
   data = []
   sql = "SELECT * FROM products WHERE id="+id+""
   stmt = ibm_db.exec_immediate(conn, sql)
   dictionary = ibm_db.fetch_both(stmt)
   while dictionary != False:
      data.append(dictionary)
      dictionary = ibm_db.fetch_both(stmt)

   newdata = []
   sql = "SELECT * FROM products ORDER BY id desc  LIMIT 4"
   stmt = ibm_db.exec_immediate(conn, sql)
   dictionar = ibm_db.fetch_both(stmt)
   while dictionar != False:
      newdata.append(dictionar)
      dictionar = ibm_db.fetch_both(stmt)
   if(data):
      return render_template("product.html",data = data[0] , newdata = newdata)
   else:
      return redirect("/")

@app.route("/search",methods=["POST"])
def search():
   data = []
   sql = "SELECT * FROM products WHERE UPPER(name) LIKE '"+request.form["search"].upper()+"'"
   stmt = ibm_db.exec_immediate(conn, sql)
   dictionary = ibm_db.fetch_both(stmt)
   while dictionary != False:
      data.append(dictionary)
      dictionary = ibm_db.fetch_both(stmt)

   newdata = []
   sql = "SELECT * FROM products ORDER BY id desc  LIMIT 4"
   stmt = ibm_db.exec_immediate(conn, sql)
   dictionar = ibm_db.fetch_both(stmt)
   while dictionar != False:
      newdata.append(dictionar)
      dictionar = ibm_db.fetch_both(stmt)
   if(data):
      return render_template("search.html",data = data , newdata = newdata)
   else:
      return redirect("/")


@app.route("/login",methods=["GET"])
def login():
   return render_template("login.html")

@app.route("/signin",methods=["POST"])
def signin():
   sql = "select * from users where email='"+request.form["email"]+"'"
   stmt = ibm_db.exec_immediate(conn, sql)
   data = []
   dictionary = ibm_db.fetch_both(stmt)
   while dictionary != False:
      data.append(dictionary)
      dictionary = ibm_db.fetch_both(stmt)
   if(data):
      if(data[0]["PASSWORD"]==request.form["password"]):
         session["user"]=data[0]["ID"]
         session["name"]=data[0]["NAME"]
         session["mob"]=data[0]["MOB"]
         session["email"]=data[0]["EMAIL"]
         return redirect("/user")
      else:
         return redirect("/login?data=Username or password is wrong")
   else:
      return redirect("/login?data=Username or password is wrong")

@app.route("/register",methods=["GET"])
def register():
   return render_template("signup.html")

@app.route("/signup",methods=["POST"])
def signup():
   sql = "INSERT INTO users (name , email , password , mob , address)values('"+request.form["name"]+"','"+request.form["email"]+"','"+request.form["password"]+"','"+request.form["mob"]+"','"+request.form["address"]+"')"
   stmt = ibm_db.exec_immediate(conn, sql)
   return redirect("/login?data=Registered Successfully!")



# USER

@app.route("/user",methods=["GET"])
def user_index():
   data = []
   sql = "SELECT * FROM products WHERE cat = 'WOMEN' ORDER BY id"
   stmt = ibm_db.exec_immediate(conn, sql)
   dictionary = ibm_db.fetch_both(stmt)
   while dictionary != False:
      data.append(dictionary)
      dictionary = ibm_db.fetch_both(stmt)

   newdata = []
   sql = "SELECT * FROM products WHERE cat = 'WOMEN' ORDER BY id desc LIMIT 4"
   stmt = ibm_db.exec_immediate(conn, sql)
   dictionar = ibm_db.fetch_both(stmt)
   while dictionar != False:
      newdata.append(dictionar)
      dictionar = ibm_db.fetch_both(stmt)

   if(session["user"]):
      return render_template("user/index.html",data = data , newdata = newdata)
   else:
      return redirect("/")

@app.route("/user/men",methods=["GET"])
def user_men():
   data = []
   sql = "SELECT * FROM products WHERE cat = 'MEN' ORDER BY id"
   stmt = ibm_db.exec_immediate(conn, sql)
   dictionary = ibm_db.fetch_both(stmt)
   while dictionary != False:
      data.append(dictionary)
      dictionary = ibm_db.fetch_both(stmt)

   newdata = []
   sql = "SELECT * FROM products WHERE cat = 'MEN' ORDER BY id desc LIMIT 4"
   stmt = ibm_db.exec_immediate(conn, sql)
   dictionar = ibm_db.fetch_both(stmt)
   while dictionar != False:
      newdata.append(dictionar)
      dictionar = ibm_db.fetch_both(stmt)

   if(session["user"]):
      return render_template("user/men.html",data = data , newdata = newdata)
   else:
      return redirect("/")

@app.route("/user/kids",methods=["GET"])
def user_kids():
   data = []
   sql = "SELECT * FROM products WHERE cat = 'KIDS' ORDER BY id"
   stmt = ibm_db.exec_immediate(conn, sql)
   dictionary = ibm_db.fetch_both(stmt)
   while dictionary != False:
      data.append(dictionary)
      dictionary = ibm_db.fetch_both(stmt)

   newdata = []
   sql = "SELECT * FROM products WHERE cat = 'KIDS' ORDER BY id desc  LIMIT 4"
   stmt = ibm_db.exec_immediate(conn, sql)
   dictionar = ibm_db.fetch_both(stmt)
   while dictionar != False:
      newdata.append(dictionar)
      dictionar = ibm_db.fetch_both(stmt)

   if(session["user"]):
      return render_template("user/kids.html",data = data , newdata = newdata)
   else:
      return redirect("/")


@app.route("/user/product/<id>",methods=["GET"])
def user_product(id):
   data = []
   sql = "SELECT * FROM products WHERE id="+id+""
   stmt = ibm_db.exec_immediate(conn, sql)
   dictionary = ibm_db.fetch_both(stmt)
   while dictionary != False:
      data.append(dictionary)
      dictionary = ibm_db.fetch_both(stmt)

   newdata = []
   sql = "SELECT * FROM products ORDER BY id desc  LIMIT 4"
   stmt = ibm_db.exec_immediate(conn, sql)
   dictionar = ibm_db.fetch_both(stmt)
   while dictionar != False:
      newdata.append(dictionar)
      dictionar = ibm_db.fetch_both(stmt)

   if(data and session["user"]):
      return render_template("user/product.html",data = data[0] , newdata = newdata)
   else:
      return redirect("/")

@app.route("/user/search",methods=["POST"])
def user_search():
   data = []
   sql = "SELECT * FROM products WHERE UPPER(name) LIKE '"+request.form["search"].upper()+"'"
   stmt = ibm_db.exec_immediate(conn, sql)
   dictionary = ibm_db.fetch_both(stmt)
   while dictionary != False:
      data.append(dictionary)
      dictionary = ibm_db.fetch_both(stmt)

   newdata = []
   sql = "SELECT * FROM products ORDER BY id desc  LIMIT 4"
   stmt = ibm_db.exec_immediate(conn, sql)
   dictionar = ibm_db.fetch_both(stmt)
   while dictionar != False:
      newdata.append(dictionar)
      dictionar = ibm_db.fetch_both(stmt)
   if(data and session["user"]):
      return render_template("user/search.html",data = data , newdata = newdata)
   else:
      return redirect("/")

@app.route("/user/order/<userid>/<productid>",methods=["GET"])
def user_order_add(userid,productid):
   sql = "INSERT INTO orders(userid,productid,data,payment) values('"+userid+"','"+productid+"','Your order is in waiting list','Not Paid')"
   stmt = ibm_db.exec_immediate(conn, sql)
   if(session["user"]):
      return redirect("/user/orders")
   else:
      return redirect("/")

@app.route("/user/orders",methods=["GET"])
def user_order():
   data = []
   sql = "SELECT * FROM orders WHERE userid='"+session['email']+"'"
   stmt = ibm_db.exec_immediate(conn, sql)
   dictionary = ibm_db.fetch_both(stmt)
   while dictionary != False:
      data.append(dictionary)
      dictionary = ibm_db.fetch_both(stmt)

   if(session["user"]):
      return render_template("user/orders.html" , data = data)
   else:
      return redirect("/")


@app.route("/user/logout",methods=["GET"])
def user_logout():
   if(session["user"]):
      return redirect("/")
   else:
      return redirect("/")

# Admin
@app.route("/admin",methods = ['POST', 'GET'])
def admin():
   if request.method == 'POST':
      if(request.form['email']=="admin@vshow.com"):
         if(request.form["password"]=="admin"):
            session['username'] = 'admin'
            return redirect("/admin/dashboard")
         else:
            return "<h3 style='text-align:center'>Password is wrong<br><br><a href='/admin'>click to login</a><h3>"
      else:
         return "<h3 style='text-align:center'>Username is wrong<br><br><a href='/admin'>click to login</a><h3>"
   if request.method == 'GET':
      return render_template("admin/index.html")

# Admin Dashboard
@app.route("/admin/dashboard",methods = ['GET'])
def dashboard():
   if(session['username']=='admin'):
      data=[]
      sql = "SELECT * FROM orders"
      stmt = ibm_db.exec_immediate(conn, sql)
      dictionary = ibm_db.fetch_both(stmt)
      while dictionary != False:
         data.append(dictionary)
         dictionary = ibm_db.fetch_both(stmt)
      return render_template("admin/orders/index.html" ,data =data )
   else:
      return redirect("/admin")

@app.route("/admin/order",methods = ['POST'])
def order_update():
   if(session['username']=='admin'):
      data=[]
      sql = "UPDATE orders SET data='"+request.form['data']+"' , payment='"+request.form['payment']+"' where id ="+request.form["id"]
      stmt = ibm_db.exec_immediate(conn, sql)
      return redirect("/admin/dashboard")
   else:
      return redirect("/admin")

# Admin Products
@app.route("/admin/products",methods = ['GET'])
def products():
   data = []
   sql = "SELECT * FROM products"
   stmt = ibm_db.exec_immediate(conn, sql)
   dictionary = ibm_db.fetch_both(stmt)
   while dictionary != False:
      data.append(dictionary)
      dictionary = ibm_db.fetch_both(stmt)
   if(session['username']=='admin'):
      return render_template("admin/products/index.html" , data = data)
   else:
      return redirect("/admin")
   

@app.route("/admin/products/add",methods = ['POST'])
def product_add():
   f = request.files['file']
   print(request.form["cat"])
   sql = "insert into products(name , desc , rate , stock , img , cat) values ('"+request.form["name"]+"','"+request.form["desc"]+"',"+request.form["rate"]+","+request.form["stock"]+",'"+request.form["name"]+"','"+request.form["cat"]+"')"
   stmt = ibm_db.exec_immediate(conn, sql)
   f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(request.form["name"]+".png")))
   if(session['username']=='admin'):
      return redirect("/admin/products")
   else:
      return redirect("/admin")
   

@app.route("/admin/products/delete",methods = ['POST'])
def product_delete():
   sql = "delete from products where id="+request.form["id"]
   stmt = ibm_db.exec_immediate(conn, sql)
   if(session['username']=='admin'):
      return redirect("/admin/products")
   else:
      return redirect("/admin")
   

# Admin users
@app.route("/admin/users",methods = ['GET'])
def users():
   data = []
   sql = "SELECT * FROM users"
   stmt = ibm_db.exec_immediate(conn, sql)
   dictionary = ibm_db.fetch_both(stmt)
   while dictionary != False:
      data.append(dictionary)
      dictionary = ibm_db.fetch_both(stmt)
   if(session['username']=='admin'):
      return render_template("admin/users/index.html" , data=data)
   else:
      return redirect("/admin")
   

@app.route("/admin/users/delete",methods = ['POST'])
def user_delete():
   sql = "delete from users where id="+request.form["id"]
   stmt = ibm_db.exec_immediate(conn, sql)
   if(session['username']=='admin'):
      return redirect("/admin/users")
   else:
      return redirect("/admin")
   

@app.route("/admin/logout",methods = ['GET'])
def admin_logout():
   session['username']=""
   return redirect("/admin")
   

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=80)
