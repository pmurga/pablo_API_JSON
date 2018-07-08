# Instructions
By: Pablo Murga - pablomurga94@gmail.com

Source:
- https://ianlondon.github.io/blog/deploy-flask-docker-nginx/
- https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

- POST

id must be integer

Example:

- Wrong

curl -u $APIUSER:$APIPASS -i -H "Content-Type: application/json" -X POST -d "{"id":"4"}" $APIURL/json

- Correct

curl -u $APIUSER:$APIPASS -i -H "Content-Type: application/json" -X POST -d '{"id":4}' $APIURL/json

- GET 

To see all the files in db

curl -u $APIUSER:$APIPASS -i $API1/json

To see a file from id (3 being id in example)

curl -u $APIUSER:$APIPASS -i $API1/json/3

- PUT 

Must include title, description and done status in JSON body and id in URL (1 being id in example)

curl -u $APIUSER:$APIPASS -i -H "Content-Type: application/json" -X PUT -d '{"title":"Estudiar","done":true,"description":"Salve la materia"}' $APIURL/1

- DELETE

Must include id in url(3 being id in example)

curl -u $APIUSER:$APIPASS -i -H "Content-Type: application/json" -X DELETE $APIURL/json/3
