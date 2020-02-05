import os
from os import path
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from flask_s3 import FlaskS3
import boto3
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
from __main__ import app
from __main__ import mongo

def upload_file(file_name, bucket):
    """
    Function to upload a file to an S3 bucket
    """
    object_name = file_name
    s3_client = boto3.client('s3')
    response = s3_client.upload_file(file_name, bucket, object_name)

    return response

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
    upload_file(app.config['UPLOAD_FOLDER_CUISINE'] + "/" + f.filename, app.config['FLASKS3_BUCKET_NAME'])
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
    return render_template("cuisine_edit.html", cuisine=the_cuisine, imagePath=app.config['UPLOAD_FOLDER_CUISINE'], s3link=app.config['AWS_BUCKET_LINK'])

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
    return render_template("cuisine_pic_edit.html", cuisine=the_cuisine, imagePath=app.config['UPLOAD_FOLDER_CUISINE'], s3link=app.config['AWS_BUCKET_LINK'])

@app.route('/update_cuisine_picture/<cuisine_id>', methods=['POST'])
def update_cuisine_picture(cuisine_id):
    f = request.files['file']
    f.save(os.path.join(app.config['UPLOAD_FOLDER_CUISINE'], f.filename))
    upload_file(app.config['UPLOAD_FOLDER_CUISINE'] + "/" + f.filename, app.config['FLASKS3_BUCKET_NAME'])
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

@app.route('/view_cuisines_grid')
def view_cuisines_grid():
    return render_template("cuisine_view_grid.html",
    cuisines=mongo.db.cuisines.find(),imagePath=app.config['UPLOAD_FOLDER_CUISINE'], s3link=app.config['AWS_BUCKET_LINK'])