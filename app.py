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
    return redirect(url_for('add_recipe'))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=os.environ.get('PORT'),
    debug=True)