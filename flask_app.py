from flask import Flask,render_template,request,session,redirect,url_for,flash
from dbconnection.datamanipulation import *

from werkzeug.utils import secure_filename
import os
app=Flask(__name__)
upload_folder='./static'
app.config['UPLOAD_FOLDER']=upload_folder
app.config['MAX_CONTENT_LENGTH']=16*1024*1024
ALLOWED_EXTENSIONS={'jpg','png','PNG'}
def is_allowed(filename):
    return '.' in filename and filename.rsplit('.',1)[1]in ALLOWED_EXTENSIONS
    

app.secret_key="supersecret"




@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/registerAction",methods=['POST'])
def registerAction():
    name=request.form['name']
    address=request.form['address']
    gender=request.form['gender']
    dob=request.form['dob']
    phone=request.form['phone']
    username=request.form['username']
    password=request.form['password']
    user=sql_edit_insert("insert into register_tb values(NULL,?,?,?,?,?,?,?)",(name,address,gender,dob,phone,username,password))
    if user>0:
        msg="registration successfull"
    else:
        msg="registration failed"
    return render_template("register.html",msg=msg)

@app.route("/login") 
def login():
    return render_template('login.html')

@app.route("/loginAction",methods=['POST'])
def loginAction():
    username=request.form['username']
    password=request.form['password']
    user=sql_query2("select * from register_tb where username=? and password=?",(username,password))
    if len(user)>0:
        session['id']=user[0][0]
        return render_template('home.html')
    else:
        msg="login failed"
        return render_template('login.html',msg=msg)

@app.route("/viewregisteredusers")
def viewregisteredusers():
    user=sql_query("select * from register_tb")
    return render_template('viewregisteredusers.html',user=user)

@app.route("/delete")
def delete():
    sid=request.args.get('uid')
    user=sql_edit_insert("delete from register_tb where id=?",[sid])
    return redirect(url_for ('viewregisteredusers'))

@app.route("/edit")
def edit():
    rid=request.args.get('uid')
    user=sql_query2("select * from register_tb where id=?",[rid])
    return render_template("edit.html",user=user)

@app.route("/editAction",methods=["post"])
def editAction():
    id=request.form['id']
    name=request.form['name']
    address=request.form['address']
    gender=request.form['gender']
    dob=request.form['dob']
    phone=request.form['phone']
    username=request.form['username']
    password=request.form['password']
    user=sql_edit_insert("update register_tb set name=?,address=?,gender=?,dob=?,phone=?,username=?,password=? where id=?",(name,address,gender,dob,phone,username,password,id))
    flash("updated successfully")
    return redirect(url_for ("viewregisteredusers"))

@app.route("/dropdownbindig")
def dropdownbinding():
    country=sql_query("select * from country_tb" )
    return render_template("dropdownbinding.html",country=country)

@app.route("/getstate")
def getstate():
    sid=request.args.get('countryid')
    print(sid)
    state=sql_query2("select * from state_tb where countryid=?",[sid])
    print(state)
    return render_template("getstate.html",state=state)

@app.route("/imageupload")
def imageupload():
    return render_template("imageupload.html")

@app.route('/imageuploadAction',methods=["post"])
def imageuploadAction():
    if request.method == "POST":
        if len(request.files)>0:
            file=request.files['file']
        if file and is_allowed(file.filename):
            filename=secure_filename(file.filename)
            r=sql_edit_insert("insert into image_tb values(NULL,?,?)",(filename,request.form['name']))
            if r>0:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                flash("uploaded successfully")
                return render_template('imageupload.html')
            return redirect(url_for('imageupload'))
        
            













if __name__=="__main__":
    app.run(debug=True)
