from model.Task import Task, State, User

def search_tasks(connection, request):
    query = connection.query(Task)
    # Match by name as like filter if present in the form request
    if "task_name" in request.form and request.form["task_name"] is not u'':
        query = query.filter(Task.task_name.like(request.form["task_name"] + "%"))
    # Match by state name as equality filter if present in the form request
    if "state" in request.form and request.form["state"] is not u'':
        query = query.join(Task.active_state).filter(Task.active_state.has(state_name=request.form["state"]))
    result = query.all()
    return result

def delete_task_by_id(connection, id):
    result = connection.query(Task).get(id)
    connection.delete(result)
    connection.commit()

def change_task_state_by_id(connection, state_id, task_id):
    task = connection.query(Task).get(task_id)
    state = connection.query(State).get(state_id)
    task.active_state = state
    connection.commit()

def create_task_for_params(connection, name, state_id, user_id):
    state = connection.query(State).get(state_id)
    user = connection.query(User).get(user_id)
    task = Task(task_name=name, active_state=state, user=user)
    connection.add(task)
    connection.commit()
    
