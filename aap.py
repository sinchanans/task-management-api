from flask import Flask, request, jsonify
from db import init_db, mysql

app = Flask(__name__)
init_db(app)

# CREATE TASK
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO tasks(title, description, status) VALUES (%s,%s,%s)",
                (data['title'], data['description'], data['status']))
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "Task created"}), 201

# GET ALL TASKS
@app.route('/tasks', methods=['GET'])
def get_tasks():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    cur.close()
    return jsonify(tasks)

# UPDATE TASK
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.json
    cur = mysql.connection.cursor()
    cur.execute("UPDATE tasks SET title=%s, description=%s, status=%s WHERE id=%s",
                (data['title'], data['description'], data['status'], id))
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "Task updated"})

# DELETE TASK
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tasks WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "Task deleted"})

if __name__ == '__main__':
    app.run(debug=True)