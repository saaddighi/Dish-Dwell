from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from wtforms.fields import FieldList, FormField
class RegistrationForm(FlaskForm):
    Firstname = StringField('First name', validators=[DataRequired(), Length(min=3, max=20)])
    Lastname = StringField('Last name', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

class loginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')
    
class IngridientsF(FlaskForm):
    name = StringField('Ingredient Name', validators=[DataRequired()])
    amount = IntegerField('Amount', validators=[DataRequired()])
    unit = StringField('Unit', validators=[DataRequired()])


class RecipesF(FlaskForm):
    title = StringField('Recipe title', validators=[DataRequired(), Length(min=2, max=150)])
    image = StringField('Image URL', validators=[DataRequired(), Length(min=8, max=255)])
    prep_time = IntegerField('Preparation time(in minutes)', validators=[DataRequired()])
    servings = IntegerField('Servings', validators=[DataRequired()])
    instructions = TextAreaField('Instructions', validators=[DataRequired()])
    ingredients = FieldList(FormField(IngridientsF), min_entries=1)
    submit = SubmitField('Creat recipe')