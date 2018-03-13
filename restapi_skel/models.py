from datetime import datetime
from sqlalchemy import desc
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from restapi_skel import db


# User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    email = db.Column(db.String(254), unique=True)
    password_hash = db.Column(db.String(64))

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_token(self, expiration=600):
        s = Serializer(b'\x15\x01\xf7\x1b]\xce\xf1I\xc3\xc8\xb5^\x05\x9f\xc2\xe6\xd8,-\x06\xe7Z\xb7\xe0',
                       expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_token(token):
        s = Serializer(b'\x15\x01\xf7\x1b]\xce\xf1I\xc3\xc8\xb5^\x05\x9f\xc2\xe6\xd8,-\x06\xe7Z\xb7\xe0')
        try:
            data = s.loads(token)
        except SignatureExpired:
            # valid token but expired
            return None
        except BadSignature:
            # invalid token
            return None
        user = User.query.get(data['id'])
        return user

    @staticmethod
    def get_by_id(id):
        return User.query.filter_by(id=id)

    # remove?
    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()


# Tasks
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    done = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def serialize(self):
        task = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'date': self.date,
            'due_date': self.due_date,
            'done': self.done,
            'user_id': self.user_id
        }
        return task

    @staticmethod
    def newest(num):
        return Task.query.order_by(desc(Task.date)).limit(num)
