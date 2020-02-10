import os
from os import path
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from flask_s3 import FlaskS3
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
from __main__ import app
from __main__ import mongo


@app.route('/add_ingredient')
def add_ingredient():
    return render_template("ingredient/ingredient_add.html",
                           ingredients=mongo.db.ingredients.find())


@app.route('/insert_ingredient', methods=['POST'])
def insert_ingredient():
    recipe_doc = {
        'name': request.form.get('name')
        }
    mongo.db.ingredients.insert_one(recipe_doc)
    return redirect(url_for('manage_ingredients'))


@app.route('/manage_ingredients')
def manage_ingredients():
    return render_template("ingredient/ingredient_manage.html",
                           ingredients=mongo.db.ingredients.find())


@app.route('/delete_ingredient/<ingredient_id>')
def delete_ingredient(ingredient_id):
    mongo.db.ingredients.remove({'_id': ObjectId(ingredient_id)})
    return redirect(url_for('manage_ingredients'))


@app.route('/edit_ingredient/<ingredient_id>')
def edit_ingredient(ingredient_id):
    the_ingredient = mongo.db.ingredients.find_one({'_id': ObjectId(ingredient_id)})
    return render_template("ingredient/ingredient_edit.html",
                           ingredient=the_ingredient)


@app.route('/update_ingredient/<ingredient_id>', methods=['POST'])
def update_ingredient(ingredient_id):
    ingredients = mongo.db.ingredients
    ingredients.update({'_id': ObjectId(ingredient_id)},
                       {
                           'name': request.form.get('name')
                       })
    return redirect(url_for('manage_ingredients'))
