import unittest

from flask import Flask, jsonify, request
import datetime
import time  # Simulate some work
import threading

app = Flask(__name__)

tasks = [
    {'id': 1, 'title': 'Grocery Shopping', 'completed': False, 'due_date': '2024-03-15'},
    {'id': 2, 'title': 'Pay Bills', 'completed': False, 'due_date': '2024-03-20'},
]
next_task_id = 3 # For assigning new task IDs

def send_notification(*args):
    print(datetime.datetime.now())
    time.sleep(2)

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def create_task():
    global next_task_id
    data = request.get_json()
    new_task = {
        'id': next_task_id,
        'title': data['title'],
        'completed': False,
        'due_date': data.get('due_date') or datetime.date.today().strftime("%Y-%m-%d")
    }
    next_task_id+=1
    tasks.append(new_task)
    return jsonify(new_task), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    for task in tasks:
        if task['id'] == task_id:
            task.update(data)  # Update task attributes
            # Simulate sending a notification (this is currently synchronous)
            # It is also possible to implement some timeout, but it must be checked how the counting of time impacts
            # the performance
            notification_thread = threading.Thread(target=send_notification)
            notification_thread.start() # Simulate some work (e.g., sending email)
            print(f"Notification sent for task {task_id}")
            return jsonify(task), 200
    return jsonify({'error': 'Task not found'}), 404

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    for i, task in enumerate(tasks):
        if task['id'] == task_id:
            del tasks[i]
            return jsonify({'message': 'Task deleted'}), 204
    return jsonify({'error': 'Task not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
