# app/__init__.py
'''App Initialisation'''
from flask import Flask
from .routes import main


def create_app():
    '''Create app function'''
    app = Flask(__name__)
    app.register_blueprint(main)

    return app
