from flask import Blueprint, render_template, flash, url_for, redirect
from flask_login import current_user, login_required
import httpx

Grecipe = Blueprint('Grecipe', __name__)


def get_recipe(id):
    try:
        url = f"https://api.spoonacular.com/recipes/random?apiKey=eea22b03760641f1bba4b51c6b75b5b8"
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
            return recipie_data
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {exc.request.url!r}.")
        return []


@Grecipe.route('/generate_recipe')
@login_required
def generate():
    pass
