from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'usr'

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(20), nullable=False)
    user_email = Column(String(40), unique=True)
    user_registration = Column(Date, nullable=False)

class State(Base):
    __tablename__ = 'state'
    state_id = Column(Integer, primary_key=True)
    state_name = Column(String(20), nullable=False)


class Task(Base):
    __tablename__ = 'task'

    task_id = Column(Integer, primary_key=True)
    task_name = Column(String(20), nullable=False)

    user_id = Column(Integer, ForeignKey('usr.user_id'))
    user = relationship('User')

    active_state_id = Column(Integer, ForeignKey('state.state_id'))
    active_state = relationship("State")