

#From APP ENGINE backend 

# Get the homepage, testing purposed 
curl https://sage-task.nw.r.appspot.com

# Get all the transactions 
curl https://sage-task.nw.r.appspot.com/v1/api/transactions/

# Get a pge of the transactions (50 rows)
curl https://sage-task.nw.r.appspot.com/v1/api/transactions/page_num/5


# Get transaction by symbol
curl https://sage-task.nw.r.appspot.com/v1/api/transactions/get/symbol/VCRA


# Get transaction by name
curl https://sage-task.nw.r.appspot.com/v1/api/transactions/get/name/Vocera%20Communications,%20Inc.


# Post transaction 
curl --header "Content-Type: application/json" \
     --request POST \
     --data '{"amount":-0.845,"currency":"JKY","date":1604933435000,"name":"Vocera Task","symbol":"VCRLL"}' \
     https://sage-task.nw.r.appspot.com/v1/api/transactions/add/


# Delete transaction by symbol 
curl --header "Content-Type: application/json" \
     --request DELETE \
     --data '{}' \
     https://sage-task.nw.r.appspot.com/v1/api/transactions/delete/symbol/VCRLL


# Post transaction 
curl --header "Content-Type: application/json" \
     --request POST \
     --data '{"amount":-0.845,"currency":"JKY","date":1604933435000,"name":"Vocera Task","symbol":"VCRLL"}' \
     https://sage-task.nw.r.appspot.com/v1/api/transactions/add/  


# Delete transaction by name 
curl --header "Content-Type: application/json" \
     --request DELETE \
     --data '{}' \
     https://sage-task.nw.r.appspot.com/v1/api/transactions/delete/name/Vocera%20Task   

# Post transaction 
curl --header "Content-Type: application/json" \
     --request POST \
     --data '{"amount":-0.845,"currency":"JKY","date":1604933435000,"name":"Vocera Task","symbol":"VCRLL"}' \
     https://sage-task.nw.r.appspot.com/v1/api/transactions/add/ 


# Update transaction 
curl --header "Content-Type: application/json" \
     --request PUT \
     --data '{"amount":-0.000,"currency":"JKY","date":1604939999999,"name":"Vocera Task Updated","symbol":"VCRLL"}' \
     https://sage-task.nw.r.appspot.com/v1/api/transactions/update/VCRLL/JKY
        



#From API Gateway 

# Get the homepage, testing purposed 
curl https://sage-gateway-3hbojviu.nw.gateway.dev/?key=AIzaSyCdy-L8R_r-jv8gsB17aWJxPN7pV7BggCo

# Get all the transactions 
curl https://sage-gateway-3hbojviu.nw.gateway.dev/v1/api/transactions/?key=AIzaSyCdy-L8R_r-jv8gsB17aWJxPN7pV7BggCo

# Get a pge of the transactions (50 rows)
curl  https://sage-gateway-3hbojviu.nw.gateway.dev/v1/api/transactions/page_num/8?key=AIzaSyCdy-L8R_r-jv8gsB17aWJxPN7pV7BggCo

# Get transactions by name 
curl https://sage-gateway-3hbojviu.nw.gateway.dev/v1/api/transactions/get/name/Vocera%20Communications,%20Inc.?key=AIzaSyCdy-L8R_r-jv8gsB17aWJxPN7pV7BggCo

# Get transactions by symbol 
curl https://sage-gateway-3hbojviu.nw.gateway.dev/v1/api/transactions/get/symbol/HHHH?key=AIzaSyCdy-L8R_r-jv8gsB17aWJxPN7pV7BggCo


# Post transaction 
curl --header "Content-Type: application/json" \
     --request POST \
     --data '{"amount":-0.845,"currency":"JKY","date":1604933435000,"name":"Just Another Test","symbol":"HHHH"}' \
     https://sage-gateway-3hbojviu.nw.gateway.dev/v1/api/transactions/add?key=AIzaSyCdy-L8R_r-jv8gsB17aWJxPN7pV7BggCo

# Delete transactions by name 
curl --header "Content-Type: application/json" \
     --request DELETE \
     --data '{}' \
     https://sage-gateway-3hbojviu.nw.gateway.dev/v1/api/transactions/delete/name/Just%20Another%20Test?key=AIzaSyCdy-L8R_r-jv8gsB17aWJxPN7pV7BggCo 


# Delete transactions by symbol
curl --header "Content-Type: application/json" \
     --request DELETE \
     --data '{}' \
     https://sage-gateway-3hbojviu.nw.gateway.dev/v1/api/transactions/delete/symbol/HHHH?key=AIzaSyCdy-L8R_r-jv8gsB17aWJxPN7pV7BggCo 

# Update transaction 
curl --header "Content-Type: application/json" \
     --request PUT \
     --data '{"amount":-0.000,"currency":"JKY","date":1604939999999,"name":"Vocera Task Updated","symbol":"VCRLL"}' \
     https://sage-gateway-3hbojviu.nw.gateway.dev/v1/api/transactions/update/HHHH/JKY?key=AIzaSyCdy-L8R_r-jv8gsB17aWJxPN7pV7BggCo
