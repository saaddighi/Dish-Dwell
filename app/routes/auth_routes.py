from flask import Blueprint, render_template, redirect, flash, url_for
from app.forms import RegistrationForm, loginForm
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import login_user, logout_user, current_user, login_required

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def authh():
    form = loginForm()
    
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
    
    if form.validate_on_submit():
        user = User.query.filter_by(email= form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            flash('Log in succesful', "sucsess")
            return redirect(url_for('home.home'))
    else:
        flash("log in unsecsessful, password or email incorrect", "danger")
    return render_template('login.html', user=current_user, form=form)


@auth.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
    
    if form.validate_on_submit():
        first_name = form.Firstname.data
        last_name = form.Lastname.data
        email = form.email.data
        password = form.password.data
        new_user = User(first_name=first_name, last_name=last_name, email=email, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        login_user(user, remember=True)
        flash(f"Account created for {form.Firstname.data} {form.Lastname.data}!", category="success")
        return f"Account created for {form.Firstname.data} {form.Lastname.data}!"
    return render_template('sign_up.html', form=form)


@auth.route('logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.authh'))