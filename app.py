import re
from flask import Flask,render_template, url_for ,flash , redirect
import joblib 
from flask import request
import numpy as np

import os
from flask import send_from_directory

import pandas as pd
import pickle


filename = 'SVM.sav'
loaded1_model = pickle.load(open("RandomForestGene.sav", 'rb'))
app=Flask(__name__,template_folder='template')


dir_path = os.path.dirname(os.path.realpath(__file__))
# UPLOAD_FOLDER = dir_path + '/uploads'
# STATIC_FOLDER = dir_path + '/static'
UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static'
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'








@app.route('/upload', methods=['POST','GET'])

def upload_file():

    if request.method == 'GET':
        return render_template('index.html')
    else:
        try:
            file = request.files['image']
            df = pd.read_csv(file)
 
            pred = loaded1_model.predict(df)
            print(pred)
            print(df)


            return render_template('predict.html', image_file_name = file.filename, label = "Lol", accuracy = 80)
        except:
            file = request.files['image']
            full_name = os.path.join(UPLOAD_FOLDER, file.filename)
            uploaded_file = request.files['file']
            lines = uploaded_file.readlines()
            print(lines)
            flash("Please select the image first !!", "danger")      
            return redirect(url_for("Malaria"))

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)



@app.route("/")



# @app.route("/home")
# def home():
#     return render_template("home.html")
 




# @app.route("/cancer")
# def cancer():
#     return render_template("cancer.html")


@app.route("/BreastCancer_Model1")
def diabetes():
    #if form.validate_on_submit():
    return render_template("clinc.html")






@app.route("/BreastCancer_Gene")
def Malaria():
    return render_template("index.html")


to_predict_list = [43,25,0,14.18,14.18,2,3,1,0,1,1]
def ValuePredictor(to_predict_list, size):
    
    print(to_predict_list)
    lst_ext = []
    loaded_model = pickle.load(open(filename, 'rb'))
    poped = to_predict_list.pop(8)

    result = trueorfalse(poped)

    to_predict_list.extend([result])
    poped = to_predict_list.pop(8)

    result = trueorfalse(poped)

    to_predict_list.extend([result])
    poped = to_predict_list.pop(8)

    result = trueorfalse(poped)

    to_predict_list.extend([result])
    
    
    
    
    
    
    poped = to_predict_list.pop(5)
    if poped == 1 :
        lst_ext.extend([1,0,0])
        
    elif poped == 2:
        lst_ext.extend([0,1,0])
    else:
        lst_ext.extend([0,0,1])
    
    poped = to_predict_list.pop(5)
    if poped == 1 :
        lst_ext.extend([1,0,0])
    elif poped == 2:
        lst_ext.extend([0,1,0])
    else:
        lst_ext.extend([0,0,1])


    poped = to_predict_list.pop(5)
    if poped == 1 :
        lst_ext.extend([1,0,0])
    elif poped == 2:
        lst_ext.extend([0,1,0])
    else:
        lst_ext.extend([0,0,1])



    print(lst_ext)

    
    to_predict_list.extend(lst_ext)


    
    dummy = np.array(to_predict_list)

    reshaped = dummy.reshape(1, -1)
    result = loaded_model.predict(reshaped)
    print(result)

    




    return result[0] 


def trueorfalse(b):
    if int(b)==0:
        return False
    else:
        return True


@app.route('/result',methods = ["POST"])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list=list(to_predict_list.values())
        
        to_predict_list = list(map(int, to_predict_list))
        result = ValuePredictor(to_predict_list,30)

    if(int(result)==0):
        prediction='Sorry ! Suffering'
    else:
        prediction='Congrats ! you are Healthy' 
    return(render_template("result.html", prediction=prediction))


if __name__ == "__main__":
    app.run(debug=True)
