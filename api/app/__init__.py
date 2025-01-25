from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from config import SECRET_KEY

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
    app.config["SECRET_KEY"] = SECRET_KEY
    
    from .models.user_model import User
    from .routes.callback import callback_bp
    from .routes.users import users_bp

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(callback_bp)
    app.register_blueprint(users_bp)

    @app.before_request
    def validate_secret_key():
        if not request.path in ["/callback", "/"]:
            key = request.headers.get("X-Secret-Key")
            if key is None or key != SECRET_KEY:
                return jsonify(success=False, message="Missing or invalid secret key")

    @app.get("/")
    def home():
        return jsonify(
            status="ok",
            version="1.0.0",
            author="packslasher"
        )
    
    return app
