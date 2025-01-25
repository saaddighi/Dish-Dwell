from flask import Blueprint, render_template
from flask_login import current_user, login_required
from app.models import URecipes
import json


Urecipe = Blueprint('Urecipe', __name__)


@Urecipe.route('/user_recipes', methods=['GET', 'POST'])
@login_required
def u_recipe():
    recipes = URecipes.query.all()
    recipes_data = []
    if recipes:    
        for recipe in recipes:
            data = json.loads(recipe.ingredients)
            recipe_data = {
                'recipe': recipe,
                'ingredients': data
            }
            recipes_data.append(recipe_data)
            
    else:
        recipe_data = ''
    
    return render_template('Urecepies.html', user=current_user, recipes=recipes, data=recipe_data)