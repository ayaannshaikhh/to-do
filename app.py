from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

file = "todo.db"

app = Flask(__name__)

def init_db():
    connection = sqlite3.connect(current_dir + "/todo.db")
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
    ''')
    connection.commit()
    connection.close()


def get_tasks():
    connection = sqlite3.connect(current_dir + "/todo.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    connection.close()
    return tasks

init_db()

@app.route('/')
def index():
    tasks = get_tasks()
    return render_template('index.html', tasks=tasks)

@app.route("/", methods=["POST"])
def todo():
    task = request.form["Task"]
    try:
        connection = sqlite3.connect(current_dir + "/todo.db")
        print("Connected to database")
    except:
        print("Failed to connect to database")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO tasks (title) VALUES (?)", (task,))
    connection.commit()
    connection.close()
    tasks = get_tasks()
    return render_template('index.html', tasks=tasks)

@app.route("/delete/<int:task_id>", methods=["POST"])
def del_task(task_id):
    try:
        connection = sqlite3.connect(current_dir + "/todo.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        connection.commit()
        connection.close()
        return redirect(url_for("index"))
    except:
        print("Failed to connect to database")

if __name__ == '__main__':
    app.run(debug=True)
