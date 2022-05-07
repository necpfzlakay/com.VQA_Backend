#from black import err
import flask
from flask import Flask, flash, request, redirect, url_for, redirect, url_for, session, send_file
from werkzeug.utils import secure_filename
import os
from transformers import ViltProcessor, ViltForQuestionAnswering
import base64
from PIL import Image
import torch
from io import BytesIO

from AuthModel import *
from history import *


app = flask.Flask(__name__)
app.config["DEBUG"] = True

UPLOAD_FOLDER = '/images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



# def upload_filee():
#     if request.method == 'POST':
#         # check if the post request   has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         print("filemiz", file)
#         # if user does not select file, browser also
#         # submit a empty part without filename
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


@app.route('/file', methods=['POST'])
def file():
    try:
        print("Files --->", request.files, "\n")
        print("filename --->", request.files, "\n")
        uploaded_file = request.files['photo']
        uploaded_file.save("images/"+uploaded_file.filename)
        return uploaded_file.filename

    except:
        print("ERROR")
        return "No Such a File. Error!"

    # file = str(request.files)
    return redirect(url_for('response'))
    # uploaded_file.save("./Server/images/"+uploaded_file.filename+".jpg")


@app.route('/', methods=['GET', 'POST'])
def home():
    stri = '<h1>Visual Question Answering</h1> <p>Taner Arsan, \n Hüseyin Fuat Alsan, \n\n Necip Fazil Akay, \n Toygar Simsek, \n Merve Cilengir, \n Cem Kirmizigedik</p> '
    return stri


@app.route('/sendimage', methods=['POST', "GET"])
def image():
    print(request.get_json())
    return "<h1>send Page</h1><p>This site is a prototype</p>"


@app.route('/response')
def response():
    return "<h1>Success</h1><p>Photo uploaded</p>"


@app.route('/image')
def send_image():
    img = request.args.get("image")
    print("IMG -->", img)
    return send_file('images/'+str(img), mimetype='image/gif')
    # return "<h1>Success</h1><p>Photo uploaded</p>"


""" USER LOGIN REGISTER PART"""


@app.route('/login')
def login_user():
    return Login(request.args.get("username"),request.args.get("password"))


@app.route('/register')
def register_user(): 
    return Register(request.args.get("username"),
                 request.args.get("email"),
                 request.args.get("password"))



@app.route('/history')
def history_user():
    return history(request.args.get("username"))



@app.route('/question', methods=['POST', "GET"])
def ask_question():
    try:
        qstn = request.args.get("question")
        username = request.args.get("username")
        answer = "Not Completed Yet"
        photoName = request.args.get("photoName")


        addHistory(username, qstn,answer, photoName)
    except:
        qstn = " Null"
    return "Question: " + str(qstn)





"""
AFTER THIS LINE, VILT WILL BE LAUNCH
"""

"""
""" 

processor = ViltProcessor.from_pretrained("processor")
model = ViltForQuestionAnswering.from_pretrained("model")

def answer_question(image, text):
    encoding = processor(image, text, return_tensors="pt")

    # forward pass
    with torch.no_grad():
        outputs = model(**encoding)
     
    logits = outputs.logits
    idx = logits.argmax(-1).item()
    predicted_answer = model.config.id2label[idx]
   
    return predicted_answer

@app.route('/vilt', methods=['POST'])
def main():
    print("image, ",request.get_json()["image"][:50])
    #Base64 to Bytes to ImageFile to PIL
    image_b64 = request.get_json()["image"]
    image_bytes = base64.b64decode(image_b64)
    image_file = BytesIO(image_bytes)
    image = Image.open(image_file)
    question = request.get_json()["question"]
    answer = answer_question(image, question)
    print('answer', answer)
    return {'answer': answer}

app.run(debug=True, host='10.1.7.10', port=80)