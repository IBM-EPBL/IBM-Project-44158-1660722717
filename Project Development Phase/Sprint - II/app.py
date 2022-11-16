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


@app.route("/db",methods=['GET'])
def db():
   # sql = "create table products (id integer not null GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),name varchar(500),rate int,stock int,img varchar(500),desc varchar(500),cat varchar(125),PRIMARY KEY (id));"
   sql = "create table orders (id integer not null GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),userid varchar(200),productid varchar(250),data varchar(225),payment varchar(125),PRIMARY KEY (id));"
   # sql = "create table users (id integer not null GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),name varchar(500),email varchar(500),password varchar(225),mob varchar(125),address varchar(500),PRIMARY KEY (id));"
   stmt = ibm_db.exec_immediate(conn, sql)
   return "ok"

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
   app.run()