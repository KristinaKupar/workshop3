from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker
from model.User import User
from model.Task import Task, State
from dao.tasks_dao import search_tasks, delete_task_by_id, change_task_state_by_id, create_task_for_params
from dao.users_dao import UsersDao
from db.connector import get_connection

import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import json

users_dao = UsersDao()

connection = get_connection()

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Hello, world"

@app.route('/users', methods=["GET"])
def get_users():
    result = connection.query(User).all()
    return render_template("users.html", users=result)

@app.route('/users', methods=["POST"])
def create_user():
    users_dao.create_user(connection, request)
    return redirect(url_for('get_users'))

@app.route('/users/delete', methods=["POST"])
def delete_user():
    users_dao.delete_user(connection, request.form["id"])
    return redirect(url_for('get_users'))

# contains dynamical filter
@app.route('/tasks', methods=["GET", "POST"])
def get_tasks():
    result = search_tasks(connection, request)
    states = connection.query(State).all() 
    users = connection.query(User).all()

    tasksPerStateData = connection.query(State.state_name, func.count(Task.task_id)) \
                .join(Task.active_state) \
                .group_by(State.state_id).all()

    tasksPerUser = connection.query(User.user_name, func.count(Task.task_id)) \
                .group_by(User.user_id).all()

    print(tasksPerUser)

    state_names, tasks_count_for_state = zip(*tasksPerStateData)
    tasks_stats_bar = [go.Bar(
        x = state_names,
        y = tasks_count_for_state
    )]
    user_names, tasks_count = zip(*tasksPerUser)
    tasks_per_user_pie= [go.Pie(
        labels=user_names,
        values=tasks_count
    )]

    tasks_per_state_json = json.dumps(tasks_stats_bar, cls=plotly.utils.PlotlyJSONEncoder)
    tasks_per_user_json = json.dumps(tasks_per_user_pie, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("tasks.html", tasks=result, states=states, tasksPerStateJson=tasks_per_state_json, tasksPerUserJson=tasks_per_user_json, users=users)

@app.route('/tasks/states', methods=["POST"])
def change_state():
    change_task_state_by_id(connection, request.form["state"], request.form["task"])
    return redirect(url_for('get_tasks'))

@app.route('/tasks/create', methods=["POST"])
def create_task():
    create_task_for_params(connection, request.form["task_name"], request.form["state"], request.form["user"])
    return redirect(url_for('get_tasks'))


@app.route('/tasks/delete', methods=["POST"])
def delete_task():
    delete_task_by_id(connection, request.form["id"])
    return redirect(url_for('get_tasks'))
