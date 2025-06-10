import os
os.environ["HF_HOME"] = "/tmp/hf_home"
os.environ["TRANSFORMERS_CACHE"] = "/tmp/hf_transformers"
os.environ["SENTENCE_TRANSFORMERS_CACHE"] = "/tmp/st_cache"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from flask import Flask
import awsgi
from api.routes import bp as api_bp

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    app.config["JSON_AS_ASCII"] = False
    app.register_blueprint(api_bp, url_prefix="/api")
    return app

def lambda_handler(event, context):
    app = create_app()
    return awsgi.response(app, event, context)

if __name__ == "__main__":
    # 개발용 실행
    create_app().run(host="0.0.0.0", port=8080, debug=True)