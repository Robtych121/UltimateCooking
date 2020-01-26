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
app.config['UPLOAD_FOLDER_RECIPE'] = 'static/image/uploads/recipes'
app.config['UPLOAD_FOLDER_TOOL'] = 'static/image/uploads/tools'
app.config['UPLOAD_FOLDER_CUISINE'] = 'static/image/uploads/cuisines'

mongo = PyMongo(app)

@app.route('/')
def home():
    return render_template("homepage.html")

@app.route('/manage')
def manage():
    return render_template("manage.html")

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
    f.save(os.path.join(app.config['UPLOAD_FOLDER_RECIPE'], f.filename))
    url = f.filename
    keys = request.form.getlist('ingredients')
    values = request.form.getlist('quantity')
    ingred_qtys = dict(zip(keys, values))
    recipe_doc = {
        'name': request.form.get('name'),
        'description': request.form.get('description'),
        'picture': url,
        'instructions': request.form.get('instructions'),
        'complexity': request.form.get('complexity'),
        'tools': request.form.getlist('tools'),
        'ingredients': ingred_qtys,
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
    ingredients=mongo.db.ingredients.find(), tools=mongo.db.tools.find(), imagePath=app.config['UPLOAD_FOLDER_RECIPE'])

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
            'tools': recipe['tools'],
            'ingredients': recipe['ingredients'],
            'cuisine': recipe['cuisine']
        })
    return redirect(url_for('manage_recipes'))

@app.route('/update_recipe/<recipe_id>', methods=['POST'])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    pictures = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)}, {'picture':1,'_id':0})
    keys = request.form.getlist('ingredients')
    values = request.form.getlist('quantity')
    ingred_qtys = dict(zip(keys, values))
    recipes.update({'_id': ObjectId(recipe_id)},
        {
            'name': request.form.get('name'),
            'description': request.form.get('description'),
            'picture': pictures['picture'],
            'instructions': request.form.get('instructions'),
            'complexity': request.form.get('complexity'),
            'tools': request.form.getlist('tools'),
            'ingredients': ingred_qtys,
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

# Tools Routes
@app.route('/manage_tools')
def manage_tools():
    return render_template("tool_manage.html",
    tools=mongo.db.tools.find())

@app.route('/add_tool')
def add_tool():
    return render_template("tool_add.html")

@app.route('/insert_tool', methods=['POST'])
def insert_tool():
    f = request.files['file']
    f.save(os.path.join(app.config['UPLOAD_FOLDER_TOOL'], f.filename))
    url = f.filename
    tool_doc = {
        'name': request.form.get('name'),
        'description': request.form.get('description'),
        'picture': url,
        'brand': request.form.get('brand'),
        'price': request.form.get('price')
        }
    mongo.db.tools.insert_one(tool_doc)
    return redirect(url_for('manage_tools'))

@app.route('/edit_tool/<tool_id>')
def edit_tool(tool_id):
    the_tool = mongo.db.tools.find_one({'_id': ObjectId(tool_id)})
    return render_template("tool_edit.html", tool=the_tool, imagePath=app.config['UPLOAD_FOLDER_TOOL'])

@app.route('/update_tool/<tool_id>', methods=['POST'])
def update_tool(tool_id):
    tools = mongo.db.tools
    pictures = mongo.db.tools.find_one({'_id': ObjectId(tool_id)}, {'picture':1,'_id':0})
    tools.update({'_id': ObjectId(tool_id)},
        {
            'name': request.form.get('name'),
            'description': request.form.get('description'),
            'picture': pictures['picture'],
            'brand': request.form.get('brand'),
            'price': request.form.get('price')
        })
    return redirect(url_for('manage_tools'))

@app.route('/delete_tool/<tool_id>')
def delete_tool(tool_id):
    mongo.db.tools.remove({'_id': ObjectId(tool_id)})
    return redirect(url_for('manage_tools'))

@app.route('/edit_tool_picture/<tool_id>')
def edit_tool_picture(tool_id):
    the_tool = mongo.db.tools.find_one({'_id': ObjectId(tool_id)})
    return render_template("tool_pic_edit.html", tool=the_tool, imagePath=app.config['UPLOAD_FOLDER_TOOL'])

@app.route('/update_tool_picture/<tool_id>', methods=['POST'])
def update_tool_picture(tool_id):
    f = request.files['file']
    f.save(os.path.join(app.config['UPLOAD_FOLDER_TOOL'], f.filename))
    url = f.filename
    tools = mongo.db.tools
    tool = mongo.db.tools.find_one({'_id': ObjectId(tool_id)})
    tools.update({'_id': ObjectId(tool_id)},
        {
            'name': tool['name'],
            'description': tool['description'],
            'picture': url,
            'brand': tool['brand'],
            'price': tool['price']
        })
    return redirect(url_for('manage_tools'))

# Cuisine Routes
@app.route('/manage_cuisines')
def manage_cuisines():
    return render_template("cuisine_manage.html",
    cuisines=mongo.db.cuisines.find())

@app.route('/add_cuisine')
def add_cuisine():
    return render_template("cuisine_add.html")

@app.route('/insert_cuisine', methods=['POST'])
def insert_cuisine():
    f = request.files['file']
    f.save(os.path.join(app.config['UPLOAD_FOLDER_CUISINE'], f.filename))
    url = f.filename
    cuisine_doc = {
        'name': request.form.get('name'),
        'description': request.form.get('description'),
        'picture': url
        }
    mongo.db.cuisines.insert_one(cuisine_doc)
    return redirect(url_for('manage_cuisines'))

@app.route('/edit_cuisine/<cuisine_id>')
def edit_cuisine(cuisine_id):
    the_cuisine = mongo.db.cuisines.find_one({'_id': ObjectId(cuisine_id)})
    return render_template("cuisine_edit.html", cuisine=the_cuisine, imagePath=app.config['UPLOAD_FOLDER_CUISINE'])

@app.route('/update_cuisine/<cuisine_id>', methods=['POST'])
def update_cuisine(cuisine_id):
    cuisines = mongo.db.cuisines
    pictures = mongo.db.cuisines.find_one({'_id': ObjectId(cuisine_id)}, {'picture':1,'_id':0})
    cuisines.update({'_id': ObjectId(cuisine_id)},
        {
            'name': request.form.get('name'),
            'description': request.form.get('description'),
            'picture': pictures['picture']
        })
    return redirect(url_for('manage_cuisines'))

@app.route('/delete_cuisine/<cuisine_id>')
def delete_cuisine(cuisine_id):
    mongo.db.cuisines.remove({'_id': ObjectId(cuisine_id)})
    return redirect(url_for('manage_cuisines'))

@app.route('/edit_cuisine_picture/<cuisine_id>')
def edit_cuisine_picture(cuisine_id):
    the_cuisine = mongo.db.cuisines.find_one({'_id': ObjectId(cuisine_id)})
    return render_template("cuisine_pic_edit.html", cuisine=the_cuisine, imagePath=app.config['UPLOAD_FOLDER_CUISINE'])

@app.route('/update_cuisine_picture/<cuisine_id>', methods=['POST'])
def update_cuisine_picture(cuisine_id):
    f = request.files['file']
    f.save(os.path.join(app.config['UPLOAD_FOLDER_CUISINE'], f.filename))
    url = f.filename
    cuisines = mongo.db.cuisines
    cuisine = mongo.db.cuisines.find_one({'_id': ObjectId(cuisine_id)})
    cuisines.update({'_id': ObjectId(cuisine_id)},
        {
            'name': cuisine['name'],
            'description': cuisine['description'],
            'picture': url
        })
    return redirect(url_for('manage_cuisines'))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=os.environ.get('PORT'),
    debug=True)