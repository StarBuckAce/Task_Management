from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

TASK_FILE = 'tasks.json'

def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, 'r') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASK_FILE,'w') as f:
        json.dump(tasks, f, indent=4)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = load_tasks()
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def create_task():
    data= request.get_json()
    task = {
        'id':len(load_tasks())+1,
        'title': data.get('title'),
        'description': data.get('description'),
        'done':False
        }
    tasks= load_tasks()
    tasks.append(task)
    save_tasks(tasks)
    return jsonify(task), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    tasks = load_tasks()
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        task['title'] = data.get('title', task['title'])
        task['description'] = data.get('description', task['description'])
        task['done'] = data.get('done', task['done'])
        save_tasks(tasks)
        return jsonify(task)
    else:
        return jsonify({'message':'Task not found'}), 404

if __name__=='__main__':
    app.run(debug=True)
    
    
