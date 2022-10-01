from flask import Flask, render_template , request , redirect
import ibm_db

conn_str='DATABASE=bludb;HOSTNAME=9938aec0-8105-433e-8bf9-0fbb7e483086.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32459;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;uid=bbf86602;pwd=iAjizpHEzfYvlS6v'
conn = ibm_db.connect(conn_str,'','')


app = Flask(__name__)

@app.route("/",methods = ['POST', 'GET'])
def index():
   if request.method == 'POST':
      user_email = request.form['email']
      user_password = request.form['password']
      user_rollno = request.form['rollno']
      user_username = request.form['username']
      sql = "insert into user (username , email , rollnumber , password) values ('"+user_username+"','"+user_email+"',"+user_rollno+",'"+user_password+"');"
      stmt = ibm_db.exec_immediate(conn, sql)
      return redirect("/signin")

   return render_template("index.html")



@app.route("/signin",methods = ['POST', 'GET'])
def signin():
   if request.method == 'POST':
      user_email = request.form['email']
      user_password = request.form['password']
      stmt = ibm_db.exec_immediate(conn, "select * from user where email='"+user_email+"' and password='"+user_password+"';")
      user= ibm_db.fetch_assoc(stmt)
      if(user):
         return redirect("/user")
      else:
         return render_template("signin.html")
      
   return render_template("signin.html")


@app.route("/user")
def user():
   return render_template("home.html")


if __name__ == '__main__':
   app.run(debug = True)