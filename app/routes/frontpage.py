from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

fpage = Blueprint('fpage', __name__)


@fpage.route('/front_page', methods=['GET', 'POST'])
def fp():
    """front page route"""
    user = current_user
    if user.is_authenticated:
        return redirect(url_for('home.home'))
    else:
        return render_template('fpage.html', user=user)