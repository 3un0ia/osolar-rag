from flask import Flask
from api.routes import bp as api_bp

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("../config.py")
    app.register_blueprint(api_bp, url_prefix="/api")
    return app
