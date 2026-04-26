from flask import Flask, render_template, request
import os

from utils.predict import predict_image
from utils.fertilizer import get_recommendation
from utils.chatbot import chatbot_response

app = Flask(__name__)

UPLOAD_FOLDER = "static"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    recommendation = None
    image_path = None

    if request.method == 'POST':
        file = request.files['image']
        model_type = request.form['model']

        image_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(image_path)

        prediction = predict_image(image_path, model_type)

        if model_type == "cnn":
            result = f"{prediction} (CNN)"
        else:
            result = f"{prediction} (ResNet)"

        recommendation = get_recommendation(prediction)

    return render_template(
        'index.html',
        result=result,
        image=image_path,
        recommendation=recommendation
    )

@app.route('/chat', methods=['POST'])
def chat():
    message = request.form['message']
    language = request.form['language']

    response = chatbot_response(message, language)
    return response

if __name__ == "__main__":
    app.run(debug=True)