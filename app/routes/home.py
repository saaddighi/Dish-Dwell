from flask import render_template, Blueprint, flash, request, redirect, url_for
import httpx
from flask_login import login_required, current_user
import json
from app import db
from app.models import Recipes

homep = Blueprint('home', __name__)

def get_renadom_recipes(number=25):
    """gets 25 recipes from the api"""
    url = f"https://api.spoonacular.com/recipes/random?apiKey=eea22b03760641f1bba4b51c6b75b5b8&number={number}"
    try:
        with httpx.Client(timeout=10.0) as client:    
            response = client.get(url)
            data = response.json()
            recipies = []
            for recipe in data['recipes']:    
                recipie_data = {
                    'id': recipe['id'],
                    'title': recipe['title'],
                    'image': recipe.get('image', ''),
                    'readyInMinutes': recipe.get('readyInMinutes', 0),
                    'servings': recipe.get('servings', 0),
                    'summary': recipe.get('summary', ''),
                    'instructions': recipe.get('instructions', ''),
                    'ingredients': [
                        {
                            'name': ingredient['name'],
                            'amount': ingredient['amount'],
                            'unit': ingredient['unit']
                        }
                        for ingredient in recipe.get('extendedIngredients', [])
                    ]
                }
                recipies.append(recipie_data)
            
            return recipies
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {exc.request.url!r}.")
        return []

def get_recipe(id):
    """gets a recipe from its id"""
    try:
        url = f"https://api.spoonacular.com/recipes/{id}/information?apiKey=eea22b03760641f1bba4b51c6b75b5b8"
        with httpx.Client(timeout=10.0) as client:    
            response = client.get(url)
            data = response.json()   
            recipie_data = {
                    'id': str(id),
                    'title': data['title'],
                    'image': data.get('image', ''),
                    'readyInMinutes': data['readyInMinutes'],
                    'servings': data['servings'],
                    'summary': data['summary'],
                    'instructions': data['instructions'],
                    'ingredients': [
                        {
                            'name': ingredient['name'],
                            'amount': ingredient['amount'],
                            'unit': ingredient['unit']
                        }
                        for ingredient in data['extendedIngredients']
                    ]
                }
        return recipie_data
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {exc.request.url!r}.")
        return []
         

@homep.route('/')
@login_required
def home():
    """displays 25 recipes"""
    recipes = get_renadom_recipes(25)
    return render_template('home.html', user=current_user, recipes=recipes)

@homep.route('/save/<int:recipe_id>', methods=['GET','POST'])
@login_required
def save(recipe_id):
    """saves recipe when user click save recipe"""
    recipe_to_save = get_recipe(recipe_id)
    ingr = json.dumps(recipe_to_save['ingredients'])
    nw_recipe = Recipes(title=recipe_to_save['title'], image=recipe_to_save['image'],
                        prep_time=recipe_to_save['readyInMinutes'], servings=recipe_to_save['servings'],
                        instructions=recipe_to_save['instructions'], ingredients=ingr,
                        user_id=current_user.id)
    db.session.add(nw_recipe)
    db.session.commit()
    
    
    return redirect(url_for('myprofile.mprofile'))
