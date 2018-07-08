# Instructions
By: Pablo Murga - pablomurga94@gmail.com

Source:
- https://ianlondon.github.io/blog/deploy-flask-docker-nginx/
- https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

Hacer Request al server especificando URL/json. El mismo puede ser:

- POST 
curl -u $APIUSER:$APIPASS -i -H "Content-Type: application/json" -X POST -d "{"""id""":"""4"""}" $API1/json
curl -u $APIUSER:$APIPASS -i -H "Content-Type: application/json" -X POST -d '{"id":"4"}' $API1/json

- GET 
curl -u $APIUSER:$APIPASS -i $API1/json
- PUT 

curl -i -H "Content-Type: application/json" -X PUT -d '{"done":true}' $API1/json/3
curl -u $APIUSER:$APIPASS -i 10.0.1.27/json
curl -u $APIUSER:$APIPASS -i localhost/json

- DELETE
