from flask import Flask, render_template , request , redirect
import ibm_db

# conn_str='DATABASE=bludb;HOSTNAME=9938aec0-8105-433e-8bf9-0fbb7e483086.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32459;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;uid=bbf86602;pwd=iAjizpHEzfYvlS6v'
# conn = ibm_db.connect(conn_str,'','')


app = Flask(__name__, static_url_path='/static')

# Admin
@app.route("/admin",methods = ['POST', 'GET'])
def admin():
   if request.method == 'POST':
      if(request.form['email']=="admin@vshow.com"):
         if(request.form["password"]=="admin"):
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
   return render_template("admin/orders/index.html")

# Admin Products
@app.route("/admin/products",methods = ['GET'])
def products():
   return render_template("admin/products/index.html")

# Admin users
@app.route("/admin/users",methods = ['GET'])
def users():
   return render_template("admin/users/index.html")


if __name__ == '__main__':
   app.run(debug = True)