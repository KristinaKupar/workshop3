from model.Task import User
from datetime import date

class UsersDao(object):
    def delete_user(self, connection, id):
        result = connection.query(User).get(id)
        connection.delete(result)
        connection.commit()
    def create_user(self, connection, request):
        user = User(user_name=request.form["user_name"], user_email=request.form["user_email"], user_registration=date.today())
        connection.add(user)
        connection.commit()