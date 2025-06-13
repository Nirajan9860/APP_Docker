from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, ToDo
from config import Config
 
app = Flask(__name__)
app.config.from_object(Config)
 
# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
CORS(app, resources={r"/*": {"origins": "*"}}) # Allow any origin, method, and header
 
@app.route("/todos", methods=["GET"])
def get_todos():
    todos = ToDo.query.all()
    return jsonify([{"id": t.id, "title": t.title, "is_completed": t.is_completed} for t in todos])
 
@app.route("/todos/<int:id>", methods=["GET"])
def get_todo(id):
    todo = ToDo.query.get(id)
    if todo is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"id": todo.id, "title": todo.title, "is_completed": todo.is_completed})
 
@app.route("/todos", methods=["POST"])
def create_todo():
    data = request.get_json()
    todo = ToDo(title=data["title"], is_completed=data.get("is_completed", False))
    db.session.add(todo)
    db.session.commit()
    return jsonify({"id": todo.id, "title": todo.title, "is_completed": todo.is_completed}), 201
 
@app.route("/todos/<int:id>", methods=["PUT"])
def update_todo(id):
    todo = ToDo.query.get(id)
    if todo is None:
        return jsonify({"error": "Not found"}), 404
 
    data = request.get_json()
    todo.title = data.get("title", todo.title)
    todo.is_completed = data.get("is_completed", todo.is_completed)
    db.session.commit()
    return jsonify({"id": todo.id, "title": todo.title, "is_completed": todo.is_completed})
 
@app.route("/todos/<int:id>", methods=["DELETE"])
def delete_todo(id):
    todo = ToDo.query.get(id)
    if todo is None:
        return jsonify({"error": "Not found"}), 404
    db.session.delete(todo)
    db.session.commit()
    return '', 204
 
if __name__ == "__main__":
    app.run(host="192.168.56.11", port=5000, debug=True) 