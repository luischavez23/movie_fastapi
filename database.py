from peewee import *
from datetime import datetime
import hashlib 

db_postgres = PostgresqlDatabase('fastapi', user='postgres', password='admin',
                                 host='localhost', port=5432)

class User(Model):
    username = CharField(max_length=50, unique=True)
    password = CharField(max_length=50)
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db_postgres
        table_name= 'users'
    
    @classmethod
    def encrypted_password(cls, password):
        h = hashlib.md5()
        h.update(password.encode('utf-8'))
        return h.hexdigest()

class Movie(Model):
    title = CharField(max_length=50, unique=True)
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db_postgres
        table_name= 'movies'

class Review(Model):
    user_id = ForeignKeyField(User, backref='reviews')
    movie_id = ForeignKeyField(Movie, backref='reviews')
    description= TextField()
    rating = IntegerField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db_postgres
        table_name= 'reviews'
