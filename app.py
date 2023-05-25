from flask import Flask, request, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret here lol'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///writer_database.db'
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

import routes
from models import User

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

if __name__ == '__main__':
    db.create_all()
    print('after db.create_all()')