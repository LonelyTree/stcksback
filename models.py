import datetime

# peewee is orm
# this will give our model the power to talk to postgres sql
# peewee is kinda mongoose
from peewee import *

DATABASE = SqliteDatabase('dogs.sqlite')


class Dog(Model):
    name = CharField()
    owner = CharField()
    breed = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        # instructions on what database to connect too
        database = DATABASE




def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Dog], safe=True)
    DATABASE.close()
