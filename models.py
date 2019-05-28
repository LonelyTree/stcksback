import datetime

from peewee import *
from flask_bcrypt import generate_password_hash
from flask_login import UserMixin

DATABASE = PostgresqlDatabase('chopsticks', user="reeduser", password='password')

class User(UserMixin, Model):
    username = CharField()
    email    = CharField()
    password = CharField()

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, email, password, **kwargs):

        email = email.lower()
        try:
            cls.select().where(
                (cls.email==email)
            ).get()
        except cls.DoesNotExist:
            user = cls(username=username, email=email)
            user.password = generate_password_hash(password)
            user.save()
            return user
        else:
            return "user with that email already existis"









class chopsticks(Model):
    length = CharField()
    width = CharField()
    color = CharField()
    message = CharField()
    owner = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect() 
    DATABASE.create_tables([User, chopsticks], safe=True)
    DATABASE.close()
