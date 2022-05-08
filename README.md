# com.VQA_Backend
Back-end Python server of the Visual Question Answering as Microservices final project


# How To Use

* Download the huggingface model via url given below:
```
https://cdn-lfs.huggingface.co/dandelin/vilt-b32-finetuned-vqa/4d5f3409947b0369487ece7c5868f0040ceb67d25735dbb4ac5e99e03bab3a19
```
* then paste it to the model folder 
* and just double click ApiService.py file
* server will run on the http://31.145.7.41/ url
* Note: Kadir Has University IBM Machine have 31.145.7.41 external ip, so if your server have not this external ip server will work on just local network

## Needed Dependency Import Libraries

* To run this import within an order (Just run on terminal them if you did not install before)

```
pip3 install flask
pip3 install torch torchvision torchaudio
pip3 install werkzeug
pip3 install transformers
pip3 install pillow
pip3 install BytesIO
pip3 install pyodbc
pip3 install json
pip3 install pymssql
pip3 install requests 
```
