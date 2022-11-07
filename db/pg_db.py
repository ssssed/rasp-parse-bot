from peewee import *
from utils.config import database, user, password, host

db = PostgresqlDatabase(database, user=user, password=password, host=host, port=5432)