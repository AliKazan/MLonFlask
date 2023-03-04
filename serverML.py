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
import pickle

app = Flask(__name__)

bcrypt = Bcrypt(app)

cors = CORS(app, resources={r"*": {"origins": "*"}})

app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'

app.config["JWT_SECRET_KEY"] = "99999999999999999999"

jwt = JWTManager(app)


#ML
#reasd DATA FILE
fruits = pd.read_table('data.txt')
#manually select the features as targets (my portion that i think they do a great input as data to my model so it learns..the DATA)
feature_names = ['mass', 'width', 'height', 'color_score']
#define X as my actual real data
X = fruits[feature_names]
#define y as the lable to that 
y = fruits['fruit_label']
#split the data into train set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
#standerdize the data using min max scalar
scaler = MinMaxScaler()
#apply the scalar to the sets
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

#routes
@app.route('/')
def attributes():
    print(fruits.head())
    print("Connected")
    return jsonify("connected!, try routes: /Dtree /knn /logREg")

@app.route('/fr')
def french():
    try:
        return send_file('C:/Users/Lenovo/Desktop/thesis/doc+src/ML/Report.pdf', download_name='Report.pdf')
    except Exception as e:
        return str(e)




@app.route('/Dtree')
def decisionTree():
    clf = DecisionTreeClassifier().fit(X_train, y_train)
    # save the model to disk
    filename = 'finalized_model.sav'
    pickle.dump(clf, open(filename, 'wb'))
    return jsonify('Accuracy of Decision Tree classifier on training set: {:.2f}'.format(clf.score(X_train, y_train)),'Accuracy of Decision Tree classifier on test set: {:.2f}'.format(clf.score(X_test, y_test)))    

@app.route('/logReg')
def logisticRegression():
    logreg = LogisticRegression()
    logreg.fit(X_train, y_train)
    return jsonify('Accuracy of Logistic regression classifier on training set: {:.2f}'.format(logreg.score(X_train, y_train)),'Accuracy of Logistic regression classifier on test set: {:.2f}'.format(logreg.score(X_test, y_test)))
    

@app.route('/knn')
def Knearestneigbor():
    knn = KNeighborsClassifier()
    knn.fit(X_train, y_train)
    return jsonify('Accuracy of K-NN classifier on training set: {:.2f}'.format(knn.score(X_train, y_train)),'Accuracy of K-NN classifier on test set: {:.2f}'.format(knn.score(X_test, y_test)))
   
@app.route('/mymodel')
def final():
    loaded_model = pickle.load(open('finalized_model.sav', 'rb'))
    return jsonify('Accuracy of FINAL classifier on TESTING set: {:.2f}'.format(loaded_model.score(X_test, y_test)))
   
     

if __name__=="__main__":
    app.run()
   

   