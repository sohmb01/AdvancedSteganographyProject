from flask import Blueprint, redirect, render_template, request, flash, jsonify, url_for
from flask_login import login_required, current_user
from .models import Note, Upload
from . import db
import json
import os
from werkzeug.utils import secure_filename
from website.steganography import encode,decode_file
import cv2

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
def home():
    encoded_images = os.listdir("./website/static/uploads/updatedFiles/")
    return render_template("home.html", user=current_user, encoded_images = encoded_images)

@views.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST': 
        start = request.form.get('start')
        skip = request.form.get('skip')
        carrier = request.files['carrier']
        message = request.files['message']
        if not (message and carrier and skip and start):
            flash('Please enter values for all fields!', category='error') 
        else:
            carrierName = secure_filename(carrier.filename)
            carrier.save(os.path.join('./website/static/uploads/carriers/', carrierName))
            messageName = secure_filename(message.filename)
            message.save(os.path.join('./website/static/uploads/messages/', messageName))
            updatedFile = encode('./website/static/uploads/carriers/' + carrierName ,'./website/static/uploads/messages/' + messageName)
            print("./website/static/uploads/carriers/' + carrierName") 
            name, extension = carrierName.split(".")
            output_image = os.path.join('./website/static/uploads/updatedFiles/', f"{name}_encoded.{extension}")
            cv2.imwrite(output_image, updatedFile)
            
            flash('Data uploaded!', category='success')
            return render_template("encoded_image.html", fileName = "./static/uploads/updatedFiles/" + f"{name}_encoded.{extension}", name = carrierName,  user=current_user)

    return render_template("upload.html", user=current_user)

@views.route('/decode', methods=['GET', 'POST'])
@login_required
def decode():
    if request.method == 'POST': 
        fileName = request.form.get('originalFile')
        name , extension = fileName.split(".")
        if not fileName :
            flash('Please enter Filename', category='error') 
        else:
            filePath = './website/static/uploads/updatedFiles/' + fileName
            originalFile = decode_file(filePath)
            decodedFileName = fileName.split("_encoded")[0] + ".png"
            with open("./website/static/uploads/decodedFiles/" + decodedFileName, "wb") as f:
                f.write(originalFile)
            print("./website/static/uploads/decodedFiles/" + decodedFileName)
            return render_template("dashboard.html",fileName = "/static/uploads/carriers/" + decodedFileName,user=current_user)
            
    encoded_images = os.listdir("./website/static/uploads/updatedFiles/")
    return render_template("decode.html", user=current_user, encoded_images = encoded_images)

@views.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)
