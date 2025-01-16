from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

login_manager = LoginManager()

db = SQLAlchemy()
DB_NAME = "database.db"


def creat_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "ghazkgazhlkgfvoha"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    
    from app.routes.auth_routes import auth
    from app.routes.home import homep
    from app.routes.creat_recipe import Crecipie
    from app.routes.myprofile import myprofile
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(homep, url_prefix='/')
    app.register_blueprint(Crecipie, url_prefix='/')
    app.register_blueprint(myprofile, url_prefix='/')
    
    from .models import User, Recipes
    creat_database(app)
    
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    return app


def creat_database(app):
    if not path.exists('/app' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('database created!')