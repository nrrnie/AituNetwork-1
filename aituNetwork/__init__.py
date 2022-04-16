from flask import Flask
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.secret_key = 'asd'

    from aituNetwork.auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    return app
