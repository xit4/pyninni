import sqlite3
from db import db


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(80), unique=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    last_login = db.Column(db.DateTime())
    creation_date = db.Column(db.DateTime())

    def __init__(self, username, password, email, creation_date, first_name, last_name, last_login=None):
        self.username = username
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.last_login = last_login
        self.creation_date = creation_date

    def json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "last_login": self.last_login.isoformat() if self.last_login else '',
            "creation_date": self.creation_date.isoformat() if self.creation_date else ''
        }

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def patch(self, username, email, first_name, last_name):
        self.username = username if username else self.username
        self.email = email if email else self.email
        self.first_name = first_name if first_name else self.first_name
        self.last_name = last_name if last_name else self.last_name

    def update_last_login(self, last_login):
        self.last_login = last_login if last_login else self.last_login

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
