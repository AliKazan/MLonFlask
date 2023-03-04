from flask import redirect, render_template, request, send_file, session, url_for
#from typing_extensions import self
from flask import Flask, jsonify,request
from flask_cors import CORS
from os import path
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, \
                               unset_jwt_cookies, jwt_required, JWTManager

from flask import send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from sqlalchemy.sql import func

app = Flask(__name__,template_folder='./templates')
bcrypt = Bcrypt(app)
cors = CORS(app, resources={r"*": {"origins": "*"}})
app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
app.config["JWT_SECRET_KEY"] = "99999999999999999999"
jwt = JWTManager(app)

#DB
db = SQLAlchemy()
DB_NAME = "database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)
#login_manager = LoginManager()


class User(db.Model,UserMixin):
    _id = db.Column(db.Integer, primary_key=True)
    _email = db.Column(db.String(150), unique=True)
    _password = db.Column(db.String(150), default='1234223')
    _date=db.Column(db.DateTime(timezone=True), default=func.now())
    def get_id(self):
        return self._id
    def get_email(self):
        return self._email
    def get_passsword(self):
        return self._password
#initialize          
#login_manager.init_app(app)
def create_database(app):
    if not path.exists(DB_NAME):
       # db.create_all(app=app)  old
       with app.app_context():
        db.create_all()
        print('Created Database!')
 
create_database(app)


#routes
@app.route('/')
def attributes():
    print("Connected")
    return jsonify("connected!, try routes: /Dtree /knn /logREg")

#return PDF
@app.route('/report')
def report():
    try:
        return send_file('Report.pdf', download_name='Report.pdf')
    except Exception as e:
        return str(e)

#DB routes
@app.route('/login', methods=["POST"])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    query_email_exists = db.session.query(User).filter(User._email == email)
    query_password = db.session.query(User).filter(User._email == email).first()
    print(db.session.query(query_email_exists.exists()).scalar()) 
    emailExists=db.session.query(query_email_exists.exists()).scalar()
    if not emailExists:
        return {"msg": "email does not exist"}, 401
    if emailExists and query_password._password==password:
        access_token = create_access_token(identity=email)
        response = {"access_token":access_token}, 200
        print(response)
        return response
    else:
        return {"msg": "password is not correct"}, 402

@app.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logged out successfully"})
    unset_jwt_cookies(response)
    print(response)
    return response 
#get All users in the Database
@app.route("/users",methods=["GET"])
def getAccounts():
    #allUsers = User.query.all()
    allUsers= db.session.query(User).all()
    my_dict = {"_email":[],"_date":[],"_id":[]}
    for u in allUsers:
        my_dict["_email"].append(u.__dict__["_email"])
        my_dict["_id"].append(u.__dict__["_id"])
        my_dict["_date"].append(u.__dict__["_date"])
    response=jsonify(my_dict)
    return response

#create a user and add it to the Database
@app.route('/signup',methods=['POST'])
def signup():
    #method edit to be post
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    new_userr = User(_email=email,_password=password)
    query_email_exists = db.session.query(User).filter(User._email == email)
    emailExists=db.session.query(query_email_exists.exists()).scalar()
    if emailExists:
        return {"msg": "You already Have an account"}, 401
    else:
        db.session.add(new_userr)
        db.session.commit()
        print('@@@@@@@@@@NEW user added to db @@@@@@@@@@@')
        return {"msg": "Account created"}, 200    

#render template with passed attribute
@app.route('/template',methods=["GET"])
def template():
    return render_template('template.html', utc_dt=datetime.utcnow())
    
#Handle Error then redirect
@app.errorhandler(404)
def errHandler(e):
    return redirect("template.html", code=404)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        return render_template('contact.html')
    elif request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # do something with the form data
        return 'Thanks for your message!'


if __name__=="__main__":
    app.run(port=5001)
   

   