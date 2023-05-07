from atitube import db, login_manager
from datetime import datetime
from flask_login import UserMixin
import base64
from base64 import b64encode, b64decode

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    Email = db.Column(db.String(130), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    videos = db.relationship('Video', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.Email}')"


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    video_file = db.Column(db.LargeBinary, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Video('{self.name}', '{self.description}')"



