from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    recipies = db.relationship('Recipes')

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
class Recipes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    image = db.Column(db.String(255))
    prep_time = db.Column(db.Integer)
    servings = db.Column(db.Integer)
    instructions = db.Column(db.Text)
    ingredients = db.Column(db.JSON)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))