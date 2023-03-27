import yaml

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def init_model():
    from model import User
    return User


def init():
    with open('system/config.yml', 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    global db
    app = Flask(__name__)
    with app.app_context():
        db_config = config['dbs'][config['type']]
        db_host, db_port, db_name, db_login, db_password = \
            db_config['host'], db_config['port'], db_config['name'], db_config['login'], db_config['password']
        app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_login}:{db_password}@{db_host}:{db_port}/{db_name}'
        db = SQLAlchemy(app)
        model = init_model()
        db.create_all()
    return app, db, config, model
