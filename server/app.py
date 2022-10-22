from flask import Flask           # import flask
from fastai.vision import *
import os
import shutil
import re
from PIL import Image
import json
from flask import request
from flask import jsonify
import numpy as np

app = Flask(__name__)             # create an app instance

@app.route("/")                   # at the end point /
def hello():                      # call method hello
    return "Hello World!"         # which returns "hello world"
@app.route('/test', methods=['GET', 'POST'])
def test():
    img = Image.open(request.files['image'])
    filename = request.form['filename']
    img.save("test.jpg")
    data=""
    return data

@app.route('/classify', methods=['GET', 'POST'])
def classify():
    img = Image.open(request.files['image'])
    filename = request.form['filename']
    
    new_image = img.resize((512, 384))
    if os.path.isdir(filename[0:filename.index(".")])==False:
        os.mkdir(filename[0:filename.index(".")])
    new_image.save(filename[0:filename.index(".")]+"/"+filename)
    
    classes=['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']
    
    deployed_path="./model"
    learn = load_learner(deployed_path, test=ImageList.from_folder(filename[0:filename.index(".")]))
    
    test_preds_probs, _ = learn.get_preds(DatasetType.Test)
    arr = np.array(test_preds_probs)
    ind=np.argmax(arr, axis=1)
    
    indx=[]

    shutil.rmtree(filename[0:filename.index(".")]) 
    for i in ind:
        indx.append(classes[int(i)])
    data = {'label': indx[0]}
    return data

@app.route('/classify_prob', methods=['GET', 'POST'])
def classify_prob():
    img = Image.open(request.files['image'])
    filename = request.form['filename']
    
    new_image = img.resize((512, 384))
    if os.path.isdir(filename[0:filename.index(".")])==False:
        os.mkdir(filename[0:filename.index(".")])
    new_image.save(filename[0:filename.index(".")]+"/"+filename)
    
    classes=['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']
    
    deployed_path="./model"
    learn = load_learner(deployed_path, test=ImageList.from_folder(filename[0:filename.index(".")]))
    
    test_preds_probs, _ = learn.get_preds(DatasetType.Test)
    arr = np.array(test_preds_probs)
    json1=dict()
    for i in range(len(arr[0])):
        print(classes[i])
        print(str(arr[0][i]))
        json1[classes[i]]=str(arr[0][i])
    return  json.dumps(json1)
if __name__ == "__main__":        # on running python app.py
    app.run(host='0.0.0.0', port=5001)                     # run the flask app