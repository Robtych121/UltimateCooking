import os
from os import path
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
from __main__ import app
from __main__ import mongo

@app.route('/add_recipe')
def add_recipe():
    return render_template("recipe_add.html",
    cuisines=mongo.db.cuisines.find(),
    ingredients=mongo.db.ingredients.find(),
    tools=mongo.db.tools.find())

@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    f = request.files['file']
    f.save(os.path.join(app.config['UPLOAD_FOLDER_RECIPE'], f.filename))
    url = f.filename
    keys = request.form.getlist('ingredients')
    values = list(filter(None,request.form.getlist('quantity')))
    ingred_qtys = dict(zip(keys, values))
    recipe_doc = {
        'name': request.form.get('name'),
        'description': request.form.get('description'),
        'picture': url,
        'instructions': list(filter(None,request.form.getlist('instructions'))),
        'complexity': request.form.get('complexity'),
        'cookingTime': request.form.get('cookingTime'),
        'prepTime': request.form.get('prepTime'),
        'servings': request.form.get('servings'),
        'tools': request.form.getlist('tools'),
        'ingredients': ingred_qtys,
        'calories': request.form.get('calories'),
        'fat': request.form.get('fat'),
        'saturates': request.form.get('saturates'),
        'carbs': request.form.get('carbs'),
        'sugars': request.form.get('sugars'),
        'fibre': request.form.get('fibre'),
        'protein': request.form.get('protein'),
        'salt': request.form.get('salt'),
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
    ingredients=mongo.db.ingredients.find(), tools=mongo.db.tools.find(), instructions=the_recipe['instructions'], imagePath=app.config['UPLOAD_FOLDER_RECIPE'])

@app.route('/edit_recipe_picture/<recipe_id>')
def edit_recipe_picture(recipe_id):
    the_recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    return render_template("recipe_pic_edit.html", recipe=the_recipe, imagePath=app.config['UPLOAD_FOLDER_RECIPE'])

@app.route('/update_recipe_picture/<recipe_id>', methods=['POST'])
def update_recipe_picture(recipe_id):
    f = request.files['file']
    f.save(os.path.join(app.config['UPLOAD_FOLDER_RECIPE'], f.filename))
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
            'cookingTime': recipe['cookingTime'],
            'prepTime': recipe['prepTime'],
            'servings': recipe['servings'],
            'tools': recipe['tools'],
            'ingredients': recipe['ingredients'],
            'calories': recipe['calories'],
            'fat': recipe['fat'],
            'saturates': recipe['saturates'],
            'carbs': recipe['carbs'],
            'sugars': recipe['sugars'],
            'fibre': recipe['fibre'],
            'protein': recipe['protein'],
            'salt': recipe['salt'],
            'cuisine': recipe['cuisine']
        })
    return redirect(url_for('manage_recipes'))

@app.route('/update_recipe/<recipe_id>', methods=['POST'])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    pictures = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)}, {'picture':1,'_id':0})
    keys = request.form.getlist('ingredients')
    values = list(filter(None,request.form.getlist('quantity')))
    ingred_qtys = dict(zip(keys, values))
    recipes.update({'_id': ObjectId(recipe_id)},
        {
            'name': request.form.get('name'),
            'description': request.form.get('description'),
            'picture': pictures['picture'],
            'instructions': list(filter(None,request.form.getlist('instructions'))),
            'complexity': request.form.get('complexity'),
            'cookingTime': request.form.get('cookingTime'),
            'prepTime': request.form.get('prepTime'),
            'servings': request.form.get('servings'),
            'tools': request.form.getlist('tools'),
            'ingredients': ingred_qtys,
            'calories': request.form.get('calories'),
            'fat': request.form.get('fat'),
            'saturates': request.form.get('saturates'),
            'carbs': request.form.get('carbs'),
            'sugars': request.form.get('sugars'),
            'fibre': request.form.get('fibre'),
            'protein': request.form.get('protein'),
            'salt': request.form.get('salt'),
            'cuisine': request.form.get('cuisine')
        })
    return redirect(url_for('manage_recipes'))

@app.route('/view_recipe/<recipe_id>')
def view_recipe(recipe_id):
    the_recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    return render_template("recipe_view.html", recipe=the_recipe, instructions=the_recipe['instructions'],tools=the_recipe['tools'], ingredients=the_recipe['ingredients'], imagePath=app.config['UPLOAD_FOLDER_RECIPE'])

@app.route('/view_recipes_grid')
def view_recipes_grid():
    return render_template("recipe_view_grid.html",
    recipes=mongo.db.recipes.find(),imagePath=app.config['UPLOAD_FOLDER_RECIPE'],cuisines=mongo.db.cuisines.find(),ingredients=mongo.db.ingredients.find(),tools=mongo.db.tools.find())
