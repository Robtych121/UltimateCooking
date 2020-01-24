import os
from os import path
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename

# Import local environment settings - Local only
if path.exists("env.py"):
    import env 

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ['MONGO_DBNAME']
app.config["MONGO_URI"] = os.environ['MONGO_URI']
app.config["SECRET_KEY"] = os.environ['SECRET_KEY']
app.config['UPLOAD_FOLDER'] = 'static/image/uploads'

mongo = PyMongo(app)

@app.route('/')
def home():
    return render_template("homepage.html")

# Recipe Routes
@app.route('/add_recipe')
def add_recipe():
    return render_template("recipe_add.html",
    cuisines=mongo.db.cuisines.find(),
    ingredients=mongo.db.ingredients.find(),
    tools=mongo.db.tools.find())

@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    f = request.files['file']
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
    url = f.filename
    recipe_doc = {
        'name': request.form.get('name'),
        'description': request.form.get('description'),
        'picture': url,
        'instructions': request.form.get('instructions'),
        'complexity': request.form.get('complexity'),
        'tools': request.form.getlist('tools'),
        'ingredients': request.form.getlist('ingredients'),
        'cuisine': request.form.get('cuisine')
        }
    mongo.db.recipes.insert_one(recipe_doc)
    return redirect(url_for('manage_recipes'))

@app.route('/manage_recipes')
def manage_recipes():
    return render_template("recipe_manage.html",
    recipes=mongo.db.recipes.find())

@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('manage_recipes'))

@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    return render_template("recipe_edit.html", recipe=the_recipe, cuisines=mongo.db.cuisines.find(),
    ingredients=mongo.db.ingredients.find(), tools=mongo.db.tools.find(), imagePath=app.config['UPLOAD_FOLDER'])

@app.route('/edit_recipe_picture/<recipe_id>')
def edit_recipe_picture(recipe_id):
    the_recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    return render_template("recipe_pic_edit.html", recipe=the_recipe, imagePath=app.config['UPLOAD_FOLDER'])

@app.route('/update_recipe_picture/<recipe_id>', methods=['POST'])
def update_recipe_picture(recipe_id):
    f = request.files['file']
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
    url = f.filename
    recipes = mongo.db.recipes
    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    recipes.update({'_id': ObjectId(recipe_id)},
        {
            'name': recipe['name'],
            'description': recipe['description'],
            'picture': url,
            'instructions': recipe['instructions'],
            'complexity': recipe['complexity'],
            'tools': recipe['tools'],
            'ingredients': recipe['ingredients'],
            'cuisine': recipe['cuisine']
        })
    return redirect(url_for('manage_recipes'))

@app.route('/update_recipe/<recipe_id>', methods=['POST'])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    pictures = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)}, {'picture':1,'_id':0})
    recipes.update({'_id': ObjectId(recipe_id)},
        {
            'name': request.form.get('name'),
            'description': request.form.get('description'),
            'picture': pictures['picture'],
            'instructions': request.form.get('instructions'),
            'complexity': request.form.get('complexity'),
            'tools': request.form.getlist('tools'),
            'ingredients': request.form.getlist('ingredients'),
            'cuisine': request.form.get('cuisine')
        })
    return redirect(url_for('manage_recipes'))

# Ingredient Routes
@app.route('/add_ingredient')
def add_ingredient():
    return render_template("ingredient_add.html",
    ingredients=mongo.db.ingredients.find())

@app.route('/insert_ingredient', methods=['POST'])
def insert_ingredient():
    recipe_doc = {
        'name': request.form.get('name'),
        'unit': request.form.get('unit')
        }
    mongo.db.ingredients.insert_one(recipe_doc)
    return redirect(url_for('manage_ingredients'))

@app.route('/manage_ingredients')
def manage_ingredients():
    return render_template("ingredient_manage.html",
    ingredients=mongo.db.ingredients.find())

@app.route('/delete_ingredient/<ingredient_id>')
def delete_ingredient(ingredient_id):
    mongo.db.ingredients.remove({'_id': ObjectId(ingredient_id)})
    return redirect(url_for('manage_ingredients'))

@app.route('/edit_ingredient/<ingredient_id>')
def edit_ingredient(ingredient_id):
    the_ingredient = mongo.db.ingredients.find_one({'_id': ObjectId(ingredient_id)})
    return render_template("ingredient_edit.html", ingredient=the_ingredient)
    
@app.route('/update_ingredient/<ingredient_id>', methods=['POST'])
def update_ingredient(ingredient_id):
    ingredients = mongo.db.ingredients
    ingredients.update({'_id': ObjectId(ingredient_id)},
        {
            'name':request.form.get('name'),
            'unit':request.form.get('unit')
        })
    return redirect(url_for('manage_ingredients'))
        
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=os.environ.get('PORT'),
    debug=True)