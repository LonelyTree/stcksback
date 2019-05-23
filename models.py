import datetime

# peewee is orm
# this will give our model the power to talk to postgres sql
# peewee is kinda mongoose
# orm object relational mapper

from peewee import *

DATABASE = SqliteDatabase('dogs.sqlite')


class Dog(Model):
    name = CharField()
    owner = CharField()
    breed = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        # instructions on what database to connect too, in our current case sqlite
        database = DATABASE




def initialize():
    DATABASE.connect() #opening a connection to the db
    DATABASE.create_tables([Dog], safe=True)#the array takes our models and will create tables that match them
    DATABASE.close()
