import cx_Oracle
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_connection():
    username = 'user'
    password = 'root'
    host = 'localhost'
    port = '1521'
    database = 'xe'

    connection = cx_Oracle.connect(username, password, 'localhost:1521/xe')
    cursor = connection.cursor()

    print("New connection to {} created".format(db_version[0]))

    oracle_connection_string = 'oracle+cx_oracle://{username}:{password}@{hostname}:{port}/{database}'

    engine = create_engine(
        oracle_connection_string.format(
            username=username,
            password=password,
            hostname=host,
            port=port,
            database=service,
        )
    )

    Session = sessionmaker(bind=engine)
    session = Session()
    return session