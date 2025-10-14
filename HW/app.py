from flask import Flask, request, render_template, jsonify
import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image

app = Flask(__name__)

model = None
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
               'dog', 'frog', 'horse', 'ship', 'truck']

def load_model():
    global model
    if model is None:
        model = keras.models.load_model('cifar10_model.h5')
    return model

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    model = load_model()
    file = request.files['image']
    img = Image.open(file.stream).convert('RGB').resize((32, 32))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)

    pred = model.predict(img)
    pred_index = int(np.argmax(pred[0]))
    pred_class = class_names[pred_index]
    conf = float(pred[0][pred_index])

    probabilities = []
    for i, prob in enumerate(pred[0]):
        probabilities.append({
            'class': class_names[i],
            'probability': float(prob)
        })
    result = {
        'predicted_class': pred_class,
        'confidence': conf,
        'probabilities': probabilities
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)