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

preprocessor = ViltProcessor.from_pretrained('dandelin/vilt-b32-finetuned-vqa')
saved_dict = torch.load('vilt_VG_finetuned.pth')

model = saved_dict['model']
id2answer = saved_dict['id2answer']

print('Model loaded successfully!')

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



"""
Our model is working below
"""
def answer_question(image, text):
    encoding = preprocessor(image, text, return_tensors='pt')
    
    model.eval()

    with torch.no_grad():
        outputs = model(**encoding)
     
    logits = outputs.logits
    idx = logits.argmax(-1).item()
    predicted_answer = id2answer[idx]
    
    return predicted_answer
    
def predict_answer(image_path, question_str):
    image_raw = Image.open(image_path).convert('RGB')

    predicted_answer = answer_question(image_raw, question_str)

    # BU KISMI ISTERSENIZ SILEBILIRSINIZ
    #plt.yticks([])
    #plt.tight_layout()
    #plt.title(f'{question_str}\n{predicted_answer}')
    #plt.imshow(image_raw)
    
    print(f'Answer for the image {image_path} is: {predicted_answer}')
    
    # BU KISMI API UZERINDEN UYGULAMAYA GERI GONDERIN
    return predicted_answer

@app.route('/question', methods=['POST', "GET"])
def ask_question():
    try:
        qstn = request.args.get("question")
        question = request.args.get("question")
        username = request.args.get("username") 
        photoName = request.args.get("photoName")
        photoUrl = './images/'+ photoName
        image_raw = Image.open(photoUrl).convert('RGB')

        predicted_answer = answer_question(image_raw, qstn)
 
        print(f'Answer for the image {photoUrl} is: {predicted_answer}') 

        qstn = predicted_answer
        addHistory(username, question, predicted_answer, photoName)
        # return predicted_answer

    except:
        qstn = " Null"
    return "Answer: " + str(qstn)





"""
AFTER THIS LINE, VILT WILL BE LAUNCH
"""

"""
""" 
#https://cdn-lfs.huggingface.co/dandelin/vilt-b32-finetuned-vqa/4d5f3409947b0369487ece7c5868f0040ceb67d25735dbb4ac5e99e03bab3a19
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
