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
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler


app = Flask(__name__)
bcrypt = Bcrypt(app)
cors = CORS(app, resources={r"*": {"origins": "*"}})
app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
app.config["JWT_SECRET_KEY"] = "99999999999999999999"
jwt = JWTManager(app)


#routes
@app.route('/')
def attributes():
    print("Connected")
    return jsonify("connected!, try routes: /Dtree /knn /logREg")

@app.route('/french')
def french():
    try:
        return send_file('C:/Users/Lenovo/Desktop/thesis/doc+src/ML/Report.pdf', download_name='Report.pdf')
    except Exception as e:
        return str(e)




if __name__=="__main__":
    app.run()
   

   