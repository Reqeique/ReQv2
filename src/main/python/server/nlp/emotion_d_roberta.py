from flask import Flask, request
from transformers import pipeline

app = Flask(__name__)
classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True, top_k=None)

@app.route('/nlp/emotion_d_roberta', methods=['POST'])
def predict():
    data = request.form['question']
    results = classifier(data)
    
    label_to_number = {
        'joy': 1,
        'surprise': 2,
        'neutral': 3,
        'anger': 4,
        'disgust': 5,
        'sadness': 6,
        'fear': 7
    }
    
    return str(label_to_number[results[0][0]['label']])

if __name__ == '__main__':
    app.run()

