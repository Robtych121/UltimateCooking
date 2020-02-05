import os
from os import path
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from flask_s3 import FlaskS3
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
app.config['FLASKS3_BUCKET_NAME'] = 'ultimatecooking'

s3 = FlaskS3(app)
mongo = PyMongo(app)

import recipe_views
import ingredients_views
import tools_views
import cuisines_views

s3.init_app(app)

###############
# General Pages
###############

@app.route('/')
def home():
    recipes = mongo.db.recipes.count()
    cuisines = mongo.db.cuisines.count()
    tools = mongo.db.tools.count()

    # Finds the most common used cuisine
    favoriteCuisine = mongo.db.recipes.aggregate([
    {"$group": {"_id": "$cuisine","value": {"$sum": 1}}},{"$sort": {"value": -1}},{"$limit": 1}])

    return render_template("homepage.html", recipecount=recipes, cuisinecount=cuisines, toolcount=tools, favcuisine=list(favoriteCuisine))

@app.route('/manage')
def manage():
    return render_template("manage.html")

###############
# Search Pages
###############

@app.route('/simpleSearch/', methods=['GET','POST'])
def simpleSearch():
    simpleSearch = request.form.get('seachterm')
    recipes = list(mongo.db.recipes.find({'name':{'$regex':'.*' + simpleSearch + '.*'}}))
    return render_template("search_simple.html", search_query=simpleSearch, recipes=recipes,imagePath=app.config['UPLOAD_FOLDER_RECIPE'])

@app.route('/advancedSearch/', methods=['GET','POST'])
def advancedSearch():
    searchterm = request.form.get('searchterm').lower()
    searchfield = request.form.get('searchfield')
    recipes = list(mongo.db.recipes.find({searchfield:{'$regex':'.*' + searchterm + '.*'}}))
    return render_template("search_advanced.html", search_field=searchfield,search_query=searchterm, recipes=recipes,imagePath=app.config['UPLOAD_FOLDER_RECIPE'])

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=os.environ.get('PORT'),
    debug=True)