import datetime

# peewee is orm
# this will give our model the power to talk to postgres sql
# peewee is kinda mongoose
# orm object relational mapper

from peewee import *
from flask_bcrypt import generate_password_hash
from flask_login import UserMixin



DATABASE = PostgresqlDatabase('dogs', user="reeduser", password='password')

class User(UserMixin, Model):
    username = CharField(unique=True)
    email    = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, email, password, **kwargs):
        # making email lowercase
        # sanitize your data
        email = email.lower()
        try:
            cls.select().where(
                (cls.email==email)
            ).get()
        except cls.DoesNotExist:
            # we are instaiting an instance of the class
            user = cls(username=username, email=email)
            # hashing our password with bcrypt
            user.password = generate_password_hash(password)
            # save puts the user in the db
            user.save()
            return user
        else:
            return "user with that email already existis"









class Dog(Model):
    name = CharField()
    owner = CharField()
    breed = CharField()
    created_by = ForeignKeyField(User, related_name='dog_set')# back reference (Related name)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        # instructions on what database to connect too, in our current case sqlite
        database = DATABASE


def initialize():
    DATABASE.connect() #opening a connection to the db
    DATABASE.create_tables([User, Dog], safe=True)#the array takes our models and will create tables that match them
    DATABASE.close()
