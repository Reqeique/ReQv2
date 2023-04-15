from transformers import AutoTokenizer, TFDistilBertForSequenceClassification
import tensorflow as tf
from flask import Flask, request

tokenizer = AutoTokenizer.from_pretrained("AnaniyaX/decision-distilbert-uncased")
model = TFDistilBertForSequenceClassification.from_pretrained("AnaniyaX/decision-distilbert-uncased")

app = Flask(__name__)




@app.route('/nlp/decision_d_bert', methods=['POST'])
def predict():
    data = request.form['question']
    inputs = tokenizer(data, return_tensors="tf")
    outputs = model(inputs)
    predictions = tf.argmax(outputs.logits, axis=1).numpy()
    return str(predictions[0])




if __name__ == '__main__':
    app.run()