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
   


#dynamic route for user interaction with datasets, solvers selection
# For iris dataset
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier

# Load iris dataset
iris = load_iris()
X_iris, y_iris = iris.data, iris.target
X_iris_train, X_iris_test, y_iris_train, y_iris_test = train_test_split(X_iris, y_iris, test_size=0.2, random_state=42)

# For breast cancer dataset
from sklearn.datasets import load_breast_cancer

# Load breast cancer dataset
breast_cancer = load_breast_cancer()
X_bc, y_bc = breast_cancer.data, breast_cancer.target
X_bc_train, X_bc_test, y_bc_train, y_bc_test = train_test_split(X_bc, y_bc, test_size=0.2, random_state=42)

# For digits dataset
from sklearn.datasets import load_digits

# Load digits dataset
digits = load_digits()
X_digits, y_digits = digits.data, digits.target
X_digits_train, X_digits_test, y_digits_train, y_digits_test = train_test_split(X_digits, y_digits, test_size=0.2, random_state=42)

@app.route('/nn_classification', methods=['POST'])
def nn_classification():

    # Load data from JSON request
    #request_data = request.get_json()
    #dataset = request_data['dataset']
    #solver = request_data['solver']
    #regularization_term = float(request_data['reg_term'])
    dataset = request.form['dataset']
    solver = request.form['solver']
    regularization_term = float(request.form['alpha'])
    # Load dataset
    if dataset == 'iris':
        X_train, X_test, y_train, y_test = X_iris_train, X_iris_test, y_iris_train, y_iris_test
    elif dataset == 'breast_cancer':
        X_train, X_test, y_train, y_test = X_bc_train, X_bc_test, y_bc_train, y_bc_test
    elif dataset == 'digits':
        X_train, X_test, y_train, y_test = X_digits_train, X_digits_test, y_digits_train, y_digits_test
    else:
        return 'Invalid dataset'

   

    # Train neural network
    #hidden_layer_sizes = (layer_sizes[i] for i in range(n_layers))
    hidden_layer_sizes=[10,5]
    clf = MLPClassifier(hidden_layer_sizes=hidden_layer_sizes, max_iter=1000, alpha=regularization_term, solver=solver, verbose=10, random_state=42)
    clf.fit(X_train, y_train)

    # Evaluate accuracy
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    return jsonify({'accuracy': accuracy})

@app.route('/nnet',methods=["GET"])
def neuralNetworkFormHandler():
    return render_template('neuralNetworkForm.html')
    

if __name__=="__main__":
    app.run()
   

   