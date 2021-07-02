from flask import Flask, render_template, url_for, request, session, redirect
from flask.helpers import flash
from flask_socketio import SocketIO, emit
import sqlite3


class DBModels:
    def __init__(self):
        self.con = sqlite3.connect("small_projects/flask_projects/todo_app/data.db", check_same_thread=False)
        self.cur = self.con.cursor()
        
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users (
            username text not null,
            password text not null
        )""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS tasks (
            user text not null,
            content text not null,
            task_id integer primary key autoincrement
        )""")
    
    def create_user(self, username, password):
        self.cur.execute("INSERT INTO users VALUES (?, ?)", (username, password))
        self.con.commit()
    
    def successful_login(self, username, password):
        self.cur.execute("SELECT * FROM users WHERE username = (?) AND password = (?)", (username, password))
        return len(self.cur.fetchall()) == 1
    
    def username_available(self, username):
        self.cur.execute("SELECT * FROM users WHERE username = (?)", (username,))
        return len(self.cur.fetchall()) == 0
    
    def create_task(self, user, content):
        self.cur.execute("INSERT INTO tasks VALUES (?, ?, ?)", (user, content, None))
        self.con.commit()

    def delete_task(self, task_id):
        self.cur.execute("DELETE FROM tasks WHERE task_id = (?)", (task_id,))
        self.con.commit()
    
    def fetch_user_tasks(self, user):
        self.cur.execute("SELECT * FROM tasks WHERE user = (?)", (user,))
        tasks = self.cur.fetchall()
        return tasks
    
    def user_owns_task(self, user, task_id):
        self.cur.execute("SELECT * FROM tasks WHERE user = (?) AND task_id = (?)", (user, task_id))
        return len(self.cur.fetchall()) == 1


app = Flask(__name__)
app.config["SECRET_KEY"] = b'Y\xbe\xbf7\xd7\x16\xcf\xee2z$\xae1\xca\x84\x890\x84=~@\xae\xabP'

socketio = SocketIO(app)

models_instance = DBModels()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            username = request.form["username"]
            password = request.form["password"]
            confirm = request.form["confirm"]
            if models_instance.username_available(username):
                if password == confirm:
                    models_instance.create_user(username, password)
                    flash("Account created. You can now login.")
                    return render_template("index.html")

                flash("Make sure to confirm password.")
                return render_template("index.html")

            flash("Username not available")
            return render_template("index.html")
        except:
            username = request.form["login_username"]
            password = request.form["login_password"]

            if models_instance.successful_login(username, password):
                session["user"] = username
                return redirect(url_for("tasks"))
            
            flash("Account not found.")
            return render_template("index.html")

    return render_template("index.html")


@app.route("/tasks")
def tasks():
    if "user" in session:
        user_tasks = models_instance.fetch_user_tasks(session["user"])
        return render_template("tasks.html", tasks=user_tasks)
    return redirect(url_for("index"))


@socketio.on('new_task')
def new_task(msg):
    if "user" in session:
        content = msg['content']
        if content != "" and not content.isspace():
            models_instance.create_task(session["user"], content)
            emit('new_task_response', {'success': True}, room=request.sid)
        else:
            emit('new_task_response', {'success': False}, room=request.sid)

@socketio.on('delete_task')
def delete_task(msg):
    if "user" in session:
        id = msg['id']
        print(models_instance.user_owns_task(session["user"], id))
        if models_instance.user_owns_task(session["user"], id):
            models_instance.delete_task(id)
            emit('reload_page', room=request.sid)


if __name__ == "__main__":
    socketio.run(app, debug=True)
