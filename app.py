from flask import Flask, render_template, request, send_from_directory
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow import expand_dims
import numpy as np
import os
import random

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/uploads/'
model = load_model('best_model.h5')

def enemy_choice():
    choice = random.randint(0,2)
    if (choice == 0):
        return "Batu"
    elif (choice == 1):
        return "Gunting"
    else:
        return "Kertas"

def battle_condition(yours, enemy):
    if (yours == enemy):
        return "Seri!"
    elif (yours == "Gunting"):
        if (enemy == "Kertas"):
            return "Anda menang!"
        else:
            return "Anda kalah!"
    elif (yours == "Kertas"):
        if (enemy == "Gunting"):
            return "Anda kalah!"
        else:
            return "Anda menang!"
    else:
        if (enemy == "Kertas"):
            return "Anda kalah!"
        else:
            return "Anda menang!"

def convert_prediction(predicted):
    if (predicted[0] == 1):
        return('Batu')
    elif (predicted[1] == 1):
        return('Gunting')
    elif (predicted[2] == 1):
        return('Kertas')
    else:
        return('Tidak dapat diprediksi')

def predict_label(img_path):
    loaded_img = load_img(img_path, target_size=(200, 300))
    img_array = img_to_array(loaded_img) / 255.0
    img_array = expand_dims(img_array, 0)
    predicted_bit = np.round(model.predict(img_array)[0]).astype('int')
    prediction_jankenpon = convert_prediction(predicted_bit)
    return prediction_jankenpon

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.files:
            image = request.files['image']
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(img_path)
            prediction = predict_label(img_path)
            enemy = enemy_choice()
            battle = battle_condition(prediction, enemy)
            return render_template('index.html', uploaded_image=image.filename, prediction=prediction, enemy=enemy, battle=battle)

    return render_template('index.html')

@app.route('/display/<filename>')
def send_uploaded_image(filename=''):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)