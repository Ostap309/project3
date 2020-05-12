import sqlalchemy
from flask_login import UserMixin
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True)
    password = sqlalchemy.Column(sqlalchemy.String)

    surname = sqlalchemy.Column(sqlalchemy.String)

    name = sqlalchemy.Column(sqlalchemy.String)

    middle_name = sqlalchemy.Column(sqlalchemy.String)

    city = sqlalchemy.Column(sqlalchemy.String)

    date = sqlalchemy.Column(sqlalchemy.String)

    gender = sqlalchemy.Column(sqlalchemy.String)

    age = sqlalchemy.Column(sqlalchemy.Integer)

    phone_number = sqlalchemy.Column(sqlalchemy.String)

    temperament = sqlalchemy.Column(sqlalchemy.String)

    music = sqlalchemy.Column(sqlalchemy.String)

    books = sqlalchemy.Column(sqlalchemy.String)
