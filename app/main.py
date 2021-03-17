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
import os
import json
import decimal



from flask import Flask, render_template, request, Response, jsonify, current_app
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer, BigInteger, Float
from flask_marshmallow import Marshmallow



# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)
ma = Marshmallow(app)


logger = logging.getLogger()



def init_unix_connection_engine(db_config):
    # [START cloud_sql_postgres_sqlalchemy_create_socket]
    # Remember - storing secrets in plaintext is potentially unsafe. Consider using
    # something like https://cloud.google.com/secret-manager/docs/overview to help keep
    # secrets secret.
    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]
    db_socket_dir = os.environ["DB_SOCKET_DIR"]
    cloud_sql_connection_name = os.environ["CLOUD_SQL_CONNECTION_NAME"]

    
    #pool = sqlalchemy.create_engine('postgresql+pg8000://postgres:root@/sagetransactions?unix_sock=/Users/mihai/Desktop/sage_task/cloudsql/sage-task:europe-west2:sage-transactions/.s.PGSQL.5432')
      
    pool = sqlalchemy.create_engine(

        # Equivalent URL:
        # postgres+pg8000://<db_user>:<db_pass>@/<db_name>
        #                         ?unix_sock=<socket_path>/<cloud_sql_instance_name>/.s.PGSQL.5432
        sqlalchemy.engine.url.URL(
            drivername="postgresql+pg8000",
            username=db_user,  # e.g. "my-database-user"
            password=db_pass,  # e.g. "my-database-password"
            database=db_name,  # e.g. "my-database-name"
            query={
                "unix_sock": "{}/{}/.s.PGSQL.5432".format(
                    db_socket_dir,  # e.g. "/cloudsql"
                    cloud_sql_connection_name)  # i.e "<PROJECT-NAME>:<INSTANCE-REGION>:<INSTANCE-NAME>"
            }
        ),
        **db_config
    )  
   
    # [END cloud_sql_postgres_sqlalchemy_create_socket]
    pool.dialect.description_encoding = None
    return pool


def init_connection_engine():
    db_config = {
        # [START cloud_sql_postgres_sqlalchemy_limit]
        # Pool size is the maximum number of permanent connections to keep.
        "pool_size": 5,
        # Temporarily exceeds the set pool_size if no connections are available.
        "max_overflow": 2,
        # The total number of concurrent connections for your application will be
        # a total of pool_size and max_overflow.
        # [END cloud_sql_postgres_sqlalchemy_limit]

        # [START cloud_sql_postgres_sqlalchemy_backoff]
        # SQLAlchemy automatically uses delays between failed connection attempts,
        # but provides no arguments for configuration.
        # [END cloud_sql_postgres_sqlalchemy_backoff]

        # [START cloud_sql_postgres_sqlalchemy_timeout]
        # 'pool_timeout' is the maximum number of seconds to wait when retrieving a
        # new connection from the pool. After the specified amount of time, an
        # exception will be thrown.
        "pool_timeout": 30,  # 30 seconds
        # [END cloud_sql_postgres_sqlalchemy_timeout]

        # [START cloud_sql_postgres_sqlalchemy_lifetime]
        # 'pool_recycle' is the maximum number of seconds a connection can persist.
        # Connections that live longer than the specified amount of time will be
        # reestablished
        "pool_recycle": 1800,  # 30 minutes
        # [END cloud_sql_postgres_sqlalchemy_lifetime]
    }

   
    return init_unix_connection_engine(db_config)




# This global variable is declared with a value of `None`, instead of calling
# `init_connection_engine()` immediately, to simplify testing. In general, it
# is safe to initialize your database connection pool when your script starts
# -- there is no need to wait for the first request.
db = None



@app.before_first_request
def create_connection():
    global db
    db = init_connection_engine()
   
 
    
base = declarative_base()


'''
def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError
'''



class Transaction(base):  
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    symbol = Column(String)
    currency = Column(String)
    amount = Column(Float)
    date = Column(BigInteger)

class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("name", "symbol", "currency", "amount", "date")
       

       
user_schema = UserSchema()
users_schema = UserSchema(many=True)

Session = sessionmaker(bind=db)
session = Session()


@app.route('/v1/api/users/')
def all_transactions():
    
    transactions = session.query(Transaction)  
    return jsonify(users_schema.dump(transactions))


@app.route("/v1/api/users/<symbol>")
def transaction_detail(symbol):

    Session = sessionmaker(db) 
    session = Session()
    transaction = session.query(Transaction(symbol=symbol))  
    return jsonify(users_schema.dump(transaction))   






   

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python3_app]
# [END gae_python38_app]
