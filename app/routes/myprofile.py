from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import Recipes, URecipes
import json
from app import db
import os


myprofile = Blueprint('myprofile', __name__)


@myprofile.route('/myprofile', methods=['GET','POST'])
@login_required
def mprofile():
    """displays saved and created recipes on /myprofile"""   
    created_recipes = Recipes.query.filter_by(user_id=current_user.id).all()
    other_recipes = URecipes.query.filter_by(user_id=current_user.id).all()
    if created_recipes:    
        for recipe in created_recipes:
            data = json.loads(recipe.ingredients)
    else:
        data = ""
    recipes_data = []
    if other_recipes:    
        for recipe in other_recipes:
            data = json.loads(recipe.ingredients)
            recipe_data = {
                'recipe': recipe,
                'ingredients': data
            }
            recipes_data.append(recipe_data)
            
    else:
        recipe_data = ''
    return render_template('myprofile.html', created_recipes=created_recipes, user=current_user, data=data, other_recipes=other_recipes, data1=recipe_data)

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

@myprofile.route('/delet/<recipe_id>', methods=['POST'])
@login_required
def delte(recipe_id):
    recipe_todel = URecipes.query.get_or_404(recipe_id)
    
    try:
        os.remove('app/static/'+recipe_todel.image)
    except:
        pass
    db.session.delete(recipe_todel)
    db.session.commit()
    flash('Recipe deleted successfully!', 'success')
    return redirect(url_for('myprofile.mprofile'))
