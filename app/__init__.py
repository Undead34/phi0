from flask import Flask
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
from flask_mailman import Mail
from werkzeug.middleware.proxy_fix import ProxyFix
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY')
    app.wsgi_app = ProxyFix(app.wsgi_app)

    app.config.from_object('app.config.Config')
    
    Session(app)
    CSRFProtect(app)
    Mail(app)

    from app.services.firebase import init_firebase
    init_firebase(app)

    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.email import email_bp
    from app.routes.dashboard import dashboard_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(email_bp)
    app.register_blueprint(dashboard_bp)

    return app
