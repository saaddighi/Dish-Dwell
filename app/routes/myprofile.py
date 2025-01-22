from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import Recipes
import json
from app import db


myprofile = Blueprint('myprofile', __name__)


@myprofile.route('/myprofile')
@login_required
def mprofile():
    """displays saved and created recipes on /myprofile"""   
    created_recipes = Recipes.query.filter_by(user_id=current_user.id).all()
    if created_recipes:    
        for recipe in created_recipes:
            data = json.loads(recipe.ingredients)
    else:
        data = ""
    return render_template('myprofile.html', created_recipes=created_recipes, user=current_user, data=data)

@myprofile.route('/delete/<int:recipe_id>', methods=['POST'])
@login_required
def delt(recipe_id):
    """deletes recipes from the database"""
    recipe_to_del = Recipes.query.get_or_404(recipe_id)
    print('ok')
    if recipe_to_del.user_id != current_user.id:
        print('You are not authorized to delete this recipe.', 'danger')
        return redirect(url_for('myprofile.mprofile'))

    db.session.delete(recipe_to_del)
    db.session.commit()
    flash('Recipe deleted successfully!', 'success')
    return redirect(url_for('myprofile.mprofile'))
