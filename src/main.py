"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Todo
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/todos', methods=['GET'])
def get_todo():
   # get all the people
    query = Todo.query.all()

    # map the results and your list of people  inside of the all_people variable
    all_todos = list(map(lambda x: x.serialize(), query))

    return jsonify(all_todos), 200

@app.route('/addtodo', methods=['POST'])
def add_task():

    body = request.get_json()
    # en celeste campos de base de datos // y entre "" los datos que se envían
    newTodo = Todo(task=body["task"], is_done=body["is_done"])
    db.session.add(newTodo)
    db.session.commit()
    return "To do task has been inluded", 200

@app.route('/deltodo/<int:Todo_id>', methods=['DELETE'])
def handle_delete_todo(Todo_id):
    task = Todo.query.get(Todo_id)
    if task is None:
        raise APIException('Todo not found', status_code=404)
    db.session.delete(task)
    db.session.commit()
    return jsonify('Todo eliminado de forma correcta.' ,task.task), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
