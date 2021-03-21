# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import datetime
import logging
import json
import os


from flask import Flask, render_template, request, Response, jsonify, current_app 

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields, validate

#from database import init_connection_engine
from modules import Transaction 



# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

drivername= "postgresql+pg8000"
db_user = os.environ["DB_USER"]
db_pass = os.environ["DB_PASS"]
db_name = os.environ["DB_NAME"]
cloud_sql_connection_name = os.environ["CLOUD_SQL_CONNECTION_NAME"]

if 'DB_SOCKET_DIR' in os.environ:
    db_socket_dir = os.environ["DB_SOCKET_DIR"]
else:
    db_socket_dir = '/cloudsql'


database_url = '{}://{}:{}@/{}?unix_sock={}/{}/.s.PGSQL.5432'.format(drivername,db_user,db_pass,db_name,db_socket_dir,cloud_sql_connection_name)
#'postgresql+pg8000://postgres:root@/sagetransactions?unix_sock=/Users/mihai/Desktop/sage_task/cloudsql/sage-task:europe-west2:sage-transactions/.s.PGSQL.5432'

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)


logger = logging.getLogger()

    
#use marshmallow for deserializing the api data 
class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("name", "symbol", "currency", "amount", "date")

    name = fields.Str(required=True, validate=[validate.Length(min=1, max=200)])
    symbol = fields.Str(required=True, validate=[validate.Length(min=1, max=200)])
    currency = fields.Str(required=True, validate=[validate.Length(min=1, max=200)])
    amount = fields.Float(required=True)
    date = fields.Integer(required=True)

       
user_schema = UserSchema()
users_schema = UserSchema(many=True)


#main page for testing 
@app.route('/', methods=['GET'])
def homepage():
     return 'This is Sage Task Api'



#get all transactions 
@app.route('/v1/api/transactions/', methods=['GET'])
def all_transactions():
    
    
    transactions = db.session.query(Transaction).all() 
    db.session.close()
    return jsonify(users_schema.dump(transactions)), 200


#get a page of all transactions
@app.route('/v1/api/transactions/page_num/<int:page_num>', methods=['GET'])
def page_transactions(page_num):
    
    trans_per_page = 50  
    transactions = db.session.query(Transaction).paginate(per_page = trans_per_page, page = page_num)
    db.session.close()
    return jsonify(users_schema.dump(transactions.items)), 200    


#get transaction by symbol
@app.route("/v1/api/transactions/get/symbol/<symbol>", methods=['GET'])
def transaction_get_by_symbol(symbol):

    transaction = db.session.query(Transaction).filter(Transaction.symbol == symbol).all()
    db.session.close()  
    return jsonify(users_schema.dump(transaction)), 200 



#get transaction by name
@app.route("/v1/api/transactions/get/name/<name>", methods=['GET'])
def transaction_get_by_name(name):

    transaction = db.session.query(Transaction).filter(Transaction.name == name).all()
    db.session.close()  
    return jsonify(users_schema.dump(transaction)), 200        



#post another transaction
@app.route("/v1/api/transactions/add", methods=['POST'])
def transaction_add():

    request_data = request.get_json() 
    user_schema.validate(request_data)
    
    new_transaction = Transaction(    
    name      = request_data['name'],
    symbol    = request_data['symbol'],
    currency  = request_data['currency'],
    amount    = request_data['amount'],
    date      = request_data['date'],
    )

    try:
        db.session.add(new_transaction)
        db.session.commit()
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()

  
    return jsonify(request_data), 201



#delete a transaction by symbol 
@app.route("/v1/api/transactions/delete/symbol/<symbol>", methods=['DELETE'])
def transactions_delete_symbol(symbol):

    try:
        querry = db.session.query(Transaction).filter(Transaction.symbol == symbol)
        transactions = querry.all()
        number_of_transactions = querry.delete()
        db.session.commit()
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()

    if number_of_transactions > 0: 
        return jsonify(users_schema.dump(transactions)),  200

    return jsonify([]), 200   


#delete a transaction by name
@app.route("/v1/api/transactions/delete/name/<name>", methods=['DELETE'])
def transactions_delete_name(name):

    try:
        transactions = db.session.query(Transaction).filter(Transaction.name == name).all()
        number_of_transactions = db.session.query(Transaction).filter(Transaction.name == name).delete()
        db.session.commit()
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()

    if number_of_transactions > 0: 
        return jsonify(users_schema.dump(transactions)),  200

    return jsonify([]), 200        


#update  another transaction
@app.route("/v1/api/transactions/update/<symbol>/<currency>", methods=['PUT'])
def transaction_update(symbol, currency):
      
    request_data = request.get_json()
    user_schema.validate(request_data)

    new_name      = request_data['name'],
    new_symbol    = request_data['symbol'],
    new_currency  = request_data['currency'],
    new_amount    = request_data['amount'],
    new_date      = request_data['date']

    try:
        transaction = db.session.query(Transaction).filter(Transaction.symbol == symbol).filter(Transaction.currency == currency).one()
        transaction.name = new_name[0]
        transaction.symbol = new_symbol[0]
        transaction.currency = new_currency[0]
        transaction.amount = new_amount[0]
        transaction.date = new_date
   
    except:
        db.session.rollback()
        return jsonify([])
    finally:
        db.session.close()

  
    return jsonify(user_schema.dump(transaction)), 201



if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python3_app]
# [END gae_python38_app]
