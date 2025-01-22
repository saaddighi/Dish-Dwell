from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import current_user, login_required
import httpx

Grecipe = Blueprint('Grecipe', __name__)


def get_id(ing):
    """search recipes from the ingredients"""
    try:
        url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ing}&apiKey=eea22b03760641f1bba4b51c6b75b5b8"
        with httpx.Client(timeout=10.0) as client:    
            response = client.get(url)
            data = response.json()
            recipies = []
            for recipe in data:
                idd = recipe['id']
                recipies.append(idd)
            return recipies
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {exc.request.url!r}.")
        return []

def get_recipe(id):
    try:
        url = f"https://api.spoonacular.com/recipes/{id}/information?apiKey=eea22b03760641f1bba4b51c6b75b5b8"
        with httpx.Client(timeout=10.0) as client:    
            response = client.get(url)
            data = response.json()   
            recipie_data = {
                    'id': data['id'],
                    'title': data['title'],
                    'image': data.get('image', ''),
                    'readyInMinutes': data['readyInMinutes'],
                    'servings': data['servings'],
                    'summary': data['summary'],
                    'instructions': data.get('instructions', 'not available'),
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


           


@Grecipe.route('/generate_recipe', methods=['GET', 'POST'])
@login_required
def generate():
    """displays the search results"""
    ids = []
    if request.method == 'POST':
        ingr = request.form.getlist('ingredient_name[]')
        if ingr:
            ids = get_id(ingr)
            recipes = [get_recipe(j) for j in ids]
            return render_template('display.html', user=current_user, recipes=recipes)
    else:
        return render_template('Grecipie.html', user=current_user)
