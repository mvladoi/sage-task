

# Desing Procedures: 


### 1. Download the Sample Data csv file and uploaded to Google Cloud Storage 
[GCS Uploading objects](https://cloud.google.com/storage/docs/uploading-objects)


### 2. Create a Google Cloud SQL instance (PostgreSQL), create the database, create the table 
[Quickstart for Cloud SQL for PostgreSQL](https://cloud.google.com/sql/docs/postgres/quickstart)

instance name = sage-transactions
database = sagetransactions
table = transactions


```
CREATE TABLE transactions (id SERIAL PRIMARY KEY,name VARCHAR(255), symbol VARCHAR(255), currency VARCHAR(255), amount NUMERIC(5,2), date int8);
ALTER SEQUENCE transactions_id_seq RESTART WITH 10000
```


### 3. Importing data from CSV files into Cloud SQL
Prepare the Sample Data csv file to be imported with Pandas because it does not have the right format

[Importing data into Cloud SQL](https://cloud.google.com/sql/docs/postgres/import-export/importing)


### 4. Set up the Google Cloud SQL proxy in order to connect to the SQL instance from local computer. This is needed for development and testing before deploying the application to the cloud.
[Connecting using the Cloud SQL Proxy](https://cloud.google.com/sql/docs/postgres/connect-admin-proxy)

instance connection name = sage-task:europe-west2:sage-transactions

a.start the proxy

```./cloud_sql_proxy -dir=/cloudsql -instances=sage-task:europe-west2:sage-transactions -credential_file=key.json &```

b.connect to the proxy

```psql "sslmode=disable host=/cloudsql/sage-task:europe-west2:sage-transactions user=postgres"```


### 5.Start with Quickstart for Python 3 in the App Engine Standard Environment for creating a microservice 
[Quickstart for Python 3 in the App Engine Standard Environment](https://cloud.google.com/appengine/docs/standard/python3/quickstart)

```
python3 -m venv env
source env/bin/activate
gcloud app deploy

```


### 6. Connect to Cloud SQL instance from local machine using the Cloud SQL proxy

a. set the env variables 

```
export GOOGLE_APPLICATION_CREDENTIALS=/Users/mihai/Desktop/sage_task/key.json

export DB_SOCKET_DIR=/Users/mihai/Desktop/sage_task/cloudsql

export CLOUD_SQL_CONNECTION_NAME='sage-task:europe-west2:sage-transactions'

export DB_USER='postgres'

export DB_PASS='xxxx'

export DB_NAME='sagetransactions'
```

### 7. Api to be implemented : 

- **a.**\
Action	     HTTP \
Verb         GET\
URL Path     /v1/api/transactions/  
> Description  Defines a unique URL to retrieve all the transactions

- **b.**\
Action	     HTTP \
Verb         GET\
URL Path     /v1/api/transactions/page_num/<page_num>
> Description  Defines a unique URL to retrieve a page of all the transactions


- **c.**\
Action	     HTTP \
Verb         GET\
URL Path     /v1/api/transactions/get/symbol/<symbol> 
> Description  Defines a unique URL to retrieve all transaction with a specific symbol

- **d.**\
Action	     HTTP \
Verb         GET\
URL Path     v1/api/transactions/get/name/<name>
> Description  Defines a unique URL to retrieve all transaction with a specific name

- **e.**\
Action	     HTTP \
Verb         POST\
URL Path     /v1/api/transactions/add/
> Description  Defines a unique URL to add a new transaction

- **f.**\
Action	     HTTP \ 
Verb         DELETE \

URL Path     v1/api/transactions/delete/symbol/<symbol>
> Description  Defines a unique URL to delete all transactions with a specif symbol

- **g.**\
Action	     HTTP \
Verb         DELETE\
URL Path     v1/api/transactions/delete/name/<name>
> Description  Defines a unique URL to delete all transactions with a specif name


- **h.** \
Action	     HTTP \
Verb         PUT \
URL Path     v1/api/transactions/update/<symbol>/<currency>
> Description  Defines a unique URL to delete all transactions with a specif symbol and currency



### 8. Create some simple test cases using curl. 

To do:\
Automate the test cases and make a trigger to deploy the application to 
Google Cloud App Engine once a commit is pushed to Version Control 


### 9. Write the code:

- a. Flask back end microservice hosted on Google Cloud App Engine
- b. Use SQLAlchemy (is the Python SQL toolkit and Object Relational Mapper that 
gives application developers the full power and flexibility of SQL)
     - connect to Google Cloud SQL instance
- c. Use Marshmallow (is an ORM/ODM/framework-agnostic library for converting 
complex datatypes, such as objects, to and from native Python datatypes)
     - add user validation 


### 10. Implement pagination for the api which retrieve all the transactions
> transactions per page = 50  


### 11. Set up API Gateway to manage and secure an App Engine backend service.
[Getting started with API Gateway and App Engine](https://cloud.google.com/api-gateway/docs/get-started-app-engine)

- a. create config
```
gcloud api-gateway api-configs create sage-config \
  --api=sage-api --openapi-spec=openapi2-appengine.yaml \
  --project=sage-task --backend-auth-service-account=sage-gateway@sage-task.iam.gserviceaccount.

gcloud api-gateway api-configs describe sage-config \
  --api=sage-api --project=sage-task
  ```

- b. create gateway
```
  gcloud api-gateway gateways create sage-gateway \
  --api=sage-api --api-config=sage-config-new \
  --location=europe-west2 --project=sage-task

  gcloud api-gateway gateways describe sage-gateway \
  --location=europe-west2 --project=sage-task
```
defaultHostname: sage-gateway-3hbojviu.nw.gateway.dev = sage-gateway-3hbojviu.nw.gateway.dev

```curl https://sage-gateway-3hbojviu.nw.gateway.dev/```

- c. write the yaml config file 


### 12. Securing access by using an API key
[Quickstart: Deploy an API on API Gateway using the Cloud Console](https://cloud.google.com/api-gateway/docs/quickstart-console)

sage-api.apigateway.sage-task.cloud.goog

api-key = AIzaSyCdy-L8R_r-jv8gsB17aWJxPN7pV7BggCo

https://sage-gateway-3hbojviu.nw.gateway.dev/?key=AIzaSyCdy-L8R_r-jv8gsB17aWJxPN7pV7BggCo



