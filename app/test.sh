
# Get all the transactions 
curl https://sage-task.nw.r.appspot.com/v1/api/transactions/


# Get transaction by symbol
curl --header "Content-Type: application/json" \
     --request POST \
     --data '{}'  \
     https://sage-task.nw.r.appspot.com/v1/api/transactions/get/symbol/VCRA


# Get transaction by name
curl --header "Content-Type: application/json" \ 
     --request POST \
     --data '{}' \
     https://sage-task.nw.r.appspot.com/v1/api/transactions/get/name/Vocera%20Communications,%20Inc.


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
        







