from flask import Flask, render_template , request , redirect
import ibm_db
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=9938aec0-8105-433e-8bf9-0fbb7e483086.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32459;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;PROTOCOL=TCPIP;UID=bbf86602;PWD=iAjizpHEzfYvlS6v", '', '')

app = Flask(__name__)

@app.route("/",methods = ['POST', 'GET'])
def index():
   if request.method == 'POST':
      user_email = request.form['email']
      user_password = request.form['password']
      user_rollno = request.form['rollno']
      user_username = request.form['username']
      stmt = ibm_db.exec_immediate(conn, "insert into users (username , email , rollno , password) values ('"+user_email+"','"+user_email+"','"+user_rollno+"','"+user_password+")")
      return redirect("/signin")

   return render_template("index.html")



@app.route("/signin",methods = ['POST', 'GET'])
def signin():
   if request.method == 'POST':
      user_email = request.form['email']
      user_password = request.form['password']
      stmt = ibm_db.exec_immediate(conn, "select * from users where username="+user_email+" and password="+user_password)
      user= ibm_db.fetch_assoc(stmt)
      if(user){
         return redirect("/user")
      }else{
         return render_template("signin.html")
      }
      
   return render_template("signin.html")


@app.route("/user")
def user():
   return render_template("home.html")


if __name__ == '__main__':
   app.run(debug = True)