from peewee import *

user = 'root'
password = 'Onepiece345'
db_name = 'P2'

conn = MySQLDatabase(
    db_name, user=user,
    password=password,
    host='localhost'
)

# def get_connection():
#     return conn