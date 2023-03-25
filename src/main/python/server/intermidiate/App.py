from flask import Flask, request
from PIL import Image
from transformers import pipeline

app = Flask(__name__)

vqa_pipeline = pipeline("visual-question-answering")

@app.route('/intermidiate/vit', methods=['POST'])
def vqa():
    image_data = request.files['image']
    # print(image_data)
    question = request.form['question']

    image = Image.open(image_data)
    
    answer = vqa_pipeline(image, question, top_k=1)

    return answer[0]['answer']

if __name__ == '__main__':
    app.run()

