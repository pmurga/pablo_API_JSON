#!flask/bin/python
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Hacer las compras',
        'description': u'Arroz, Queso, Pizza, Frutas, Verduras',
        'done': False
    },
    {
        'id': 2,
        'title': u'Estudiar',
        'description': u'Necesito salvar la materia',
        'done': False
    }
]

@app.errorhandler(405)
def id_exists(error):
    return make_response(jsonify({'error': 'Existing ID - Use a different one'}), 405)


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
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@app.route('/json', methods=['POST'])
@auth.login_required
def create_task():

    for task2 in tasks:
        if task2['id'] == request.json['id']:
            abort(405)

    if not request.json or not 'id' in request.json:
        abort(400)

    task = {
#        'id': tasks[-1]['id'] + 1,
        'id': request.json['id'],
        'title': request.json.get('title', ""),
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

@app.route('/json/<int:task_id>', methods=['PUT'])
@auth.login_required
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

@app.route('/json/<int:task_id>', methods=['DELETE'])
@auth.login_required
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task

@app.route('/json', methods=['GET'])
@auth.login_required
def get_tasks():
    return jsonify({'tasks': [make_public_task(task) for task in tasks]})


if __name__ == '__main__':
    app.run(debug=False)
