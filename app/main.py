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

# [START gae_python38_app]
# [START gae_python3_app]
import datetime
import logging
import json
import decimal


from flask import Flask, render_template, request, Response, jsonify, current_app 
from sqlalchemy.orm import sessionmaker
from flask_marshmallow import Marshmallow

from database import *
from modules import *


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)
ma = Marshmallow(app)


logger = logging.getLogger()


# This global variable is declared with a value of `None`, instead of calling
# `init_connection_engine()` immediately, to simplify testing. In general, it
# is safe to initialize your database connection pool when your script starts
# -- there is no need to wait for the first request.
db = None


# initialize the connection to Cloud Postgresql database
@app.before_first_request
def create_connection():
    global db
    db = init_connection_engine()
    

#create the SQLAlchemy session 
def create_session():
    Session = sessionmaker(bind=db)
    session = Session() 
    return session 

    
#use marshmallow for deserializing the api data 
class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("name", "symbol", "currency", "amount", "date")

       
user_schema = UserSchema()
users_schema = UserSchema(many=True)



#get all transactions 
@app.route('/v1/api/transactions/', methods=['GET'])
def all_transactions():
    
    session = create_session()
    transactions = session.query(Transaction).all()  
    session.close()
    return jsonify(users_schema.dump(transactions)), 200


#get transaction by symbol
@app.route("/v1/api/transactions/get/symbol/<symbol>", methods=['POST'])
def transaction_get_by_symbol(symbol):

    session = create_session()
    transaction = session.query(Transaction).filter(Transaction.symbol == symbol).all()
    session.close()  
    return jsonify(users_schema.dump(transaction)), 200 



#get transaction by name
@app.route("/v1/api/transactions/get/name/<name>", methods=['POST'])
def transaction_get_by_name(name):

    session = create_session()
    transaction = session.query(Transaction).filter(Transaction.name == name).all()
    session.close()  
    return jsonify(users_schema.dump(transaction)), 200        



#post another transaction
@app.route("/v1/api/transactions/add", methods=['POST'])
def transaction_add():
     
    request_data = request.get_json() 
    session = create_session()

    new_transaction = Transaction(    
    name      = request_data['name'],
    symbol    = request_data['symbol'],
    currency  = request_data['currency'],
    amount    = request_data['amount'],
    date      = request_data['date'],
    )

    try:
        session.add(new_transaction)
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

  
    return jsonify(request_data), 201



#delete a transaction by symbol 
@app.route("/v1/api/transactions/delete/symbol/<symbol>", methods=['DELETE'])
def transactions_delete_symbol(symbol):
     
    session = create_session()

    try:
        querry = session.query(Transaction).filter(Transaction.symbol == symbol)
        transactions = querry.all()
        number_of_transactions = querry.delete()
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

    if number_of_transactions > 0: 
        return jsonify(users_schema.dump(transactions)),  200

    return jsonify([]), 200   


#delete a transaction by name
@app.route("/v1/api/transactions/delete/name/<name>", methods=['DELETE'])
def transactions_delete_name(name):
     
    session = create_session()

    try:
        transactions = session.query(Transaction).filter(Transaction.name == name).all()
        number_of_transactions = session.query(Transaction).filter(Transaction.name == name).delete()
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

    if number_of_transactions > 0: 
        return jsonify(users_schema.dump(transactions)),  200

    return jsonify([]), 200        


#update  another transaction
@app.route("/v1/api/transactions/update/<symbol>/<currency>", methods=['PUT'])
def transaction_update(symbol, currency):
      
    
    session = create_session()
    request_data = request.get_json() 

    new_name      = request_data['name'],
    new_symbol    = request_data['symbol'],
    new_currency  = request_data['currency'],
    new_amount    = request_data['amount'],
    new_date      = request_data['date']

    try:
        transaction = session.query(Transaction).filter(Transaction.symbol == symbol).filter(Transaction.currency == currency).one()
        transaction.name = new_name[0]
        transaction.symbol = new_symbol[0]
        transaction.currency = new_currency[0]
        transaction.amount = new_amount[0]
        transaction.date = new_date
   
    except:
        session.rollback()
        raise
    finally:
        session.close()

  
    return jsonify(user_schema.dump(transaction)), 201



if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python3_app]
# [END gae_python38_app]
