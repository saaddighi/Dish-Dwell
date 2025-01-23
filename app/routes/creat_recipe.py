from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.models import Recipes
from app import db
import json
import os
from werkzeug.utils import secure_filename

Crecipie = Blueprint('Crecipie', __name__)

UPLOAD_FOLDER = r'app\static\uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@Crecipie.route('/creat_recipie',methods=['GET', 'POST'])
@login_required
def create_recipe():
    """save the recipe that the user created"""
    if request.method == 'POST':
        title = request.form.get('title')
        image = request.files.get('image')
        prep_time = request.form.get('prep_time')
        servings = request.form.get('servings')
        instructions = request.form.get('instructions')

        ingredients = []
        names = request.form.getlist('ingredient_name[]')
        amounts = request.form.getlist('ingredient_amount[]')
        units = request.form.getlist('ingredient_unit[]')

        for name, amount, unit in zip(names, amounts, units):
            if name and amount and unit:
                ingredients.append({"name": name, "amount": amount, "unit": unit})
        
        image_filename = None
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            image.save(image_path)
            image_filename = os.path.join('uploads', filename).replace("\\", "/")
            
        print("Image saved to:", image_path)
        print("Image URL path:", image_filename)
        

        new_recipe = Recipes(
            title=title,
            image=image_filename,
            prep_time=prep_time,
            servings=servings,
            instructions=instructions,
            ingredients=json.dumps(ingredients),
            user_id=current_user.id
        )
        db.session.add(new_recipe)
        db.session.commit()
        flash('Recipe created successfully!', 'success')
        return redirect(url_for('home.home'))

    return render_template('Crecipie.html', user=current_user)
