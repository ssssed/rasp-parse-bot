from peewee import Model, BigIntegerField, CharField
from db import pg_db

db = pg_db.db


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    class Meta:
        db_table = 'users'

    chat_id = BigIntegerField()
    group_name = CharField(max_length=50)


if __name__ == '__main__':
    db.create_tables([User])
