#!flask/bin/python
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for
from flask_httpauth import HTTPBasicAuth
import os.path
import json
from pprint import pprint


app = Flask(__name__)
path = '/tmp/jsons/'

@app.errorhandler(405)
def id_exists(error):
    return make_response(jsonify({'error': 'Existing ID - Use a different one'}), 405)

@app.errorhandler(406)
def req_fields(error):
    return make_response(jsonify({'error': 'Lacking required fields in JSON body'}), 406)

@app.errorhandler(408)
def req_fields(error):
    return make_response(jsonify({'error': 'id must be integer'}), 408)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

auth = HTTPBasicAuth()

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403) #en vez de 401 (para evitar popup browser)

@auth.get_password
def get_password(username):
    if username == 'pablo':
        return 'tucuman'
    return None

@app.route('/json/<int:task_id>', methods=['GET'])
@auth.login_required
def get_task(task_id):
    if len(os.listdir(path)) == 0:
        abort(404)

    for file in os.listdir(path):
        if file == str(task_id) + '.json':
            filepath = path + str(task_id) + '.json'
            return jsonify({'task': readJSONfile(filepath)})

    return jsonify({'error': "File does not exist"})

def readJSONfile(file):

    f = open(file)
    try:
        data = json.load(f)
        return data

    finally:
        f.close()

@app.route('/json', methods=['POST'])
@auth.login_required
def create_task():

    if not request.json or not 'id' in request.json:
        abort(406)
    if type(request.json['id']) != int:
        abort(408)

    _str_ = str(request.json['id'])
    if os.path.isfile(path + _str_ + '.json'):
        abort(405)
    task = {
#        'id': tasks[-1]['id'] + 1,
        'id': request.json['id'],
        'title': request.json.get('title', ""),
        'description': request.json.get('description', ""),
        'done': False
    }
    #tasks.append(task)
    writeToJSONFile(path, _str_ , task)
    return jsonify({'task': task}), 201

def writeToJSONFile(path, fileName, data):
    filePathNameWExt = path + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)


@app.route('/json/<int:task_id>', methods=['PUT'])
@auth.login_required
def update_task(task_id):

    _str_ = str(task_id)
    file = _str_ + '.json'

    if not os.path.isfile(path + file):
        abort(404)
    if len(os.listdir(path)) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if not 'title' in request.json or type(request.json['title']) != unicode:
        abort(406)
    if not 'description' in request.json or type(request.json['description']) is not unicode:
        abort(406)
    if not 'done' in request.json or type(request.json['done']) is not bool:
        abort(406)

    data = readJSONfile(path + file)

    task = {
    'id': data['id'],
    'title': request.json['title'],
    'description': request.json['description'],
    'done': request.json['done']
    }
    writeToJSONFile(path,_str_,task)

    return jsonify({'task': readJSONfile(path + file)})

@app.route('/json/<int:task_id>', methods=['DELETE'])
@auth.login_required
def delete_task(task_id):
    #task = [task for task in tasks if task['id'] == task_id]
    if len(os.listdir(path)) == 0:
        abort(404)

    file = str(task_id) + '.json'

    if not os.path.isfile(path + file):
        abort(404)

    if os.path.isfile(path + file):
        os.remove(path + file)
    else:
        return jsonify({'result': False})

    return jsonify({'result': True})

@app.route('/json', methods=['GET'])
@auth.login_required
def get_tasks():
   return jsonify({'tasks': os.listdir(path)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)
