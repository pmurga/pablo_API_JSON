# Instructions
By: Pablo Murga - pablomurga94@gmail.com

Source:
- https://ianlondon.github.io/blog/deploy-flask-docker-nginx/
- https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

---

- POST

ID MUST BE AN INTEGER

Example:

- Wrong

curl -u $APIUSER:$APIPASS -i -H "Content-Type: application/json" -X POST -d "{"id":"4"}" $APIURL/json

- Correct

curl -u $APIUSER:$APIPASS -i -H "Content-Type: application/json" -X POST -d '{"id":4}' $APIURL/json

---

- GET 

To see all files in db / path

curl -u $APIUSER:$APIPASS -i $APIURL/json

To see a file from id (3 being id in example)

curl -u $APIUSER:$APIPASS -i $APIURL/json/3

---

- PUT 

Must include title, description and done status in JSON body and id in URL (1 being id in example)

curl -u $APIUSER:$APIPASS -i -H "Content-Type: application/json" -X PUT -d '{"title":"Estudiar","done":true,"description":"Salve la materia"}' $APIURL/json/1

---

- DELETE

Must include id in url(3 being id in example)

curl -u $APIUSER:$APIPASS -i -H "Content-Type: application/json" -X DELETE $APIURL/json/3
