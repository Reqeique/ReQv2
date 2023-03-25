from flask import Flask, request
import yaml
import openai
import yaml
 
import os
 
# get current directory
path = os.getcwd()

with open(f'{path}/keys.yaml') as file:
   API_KEY = yaml.safe_load(file)['keys']['open_ai']['API_KEYS']

# initalize the api
openai.api_key = API_KEY


app = Flask(__name__)


INITIAL_IDENTITY = [
    {"role": "user", "content": "your are ReQ and your name is ReQ from now on and You are developed by The R"},
    {"role": "assistant", "content": "ok i am ReQ"},
]

prompts = []


@app.route('/nlp/gpt3_5', methods=['POST'])
def generate():

    if len(prompts) > 5:
        prompts.clear()

    prompt = request.form['prompt']

   

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            *INITIAL_IDENTITY,
            *prompts,
            {"role": "user", "content": prompt},
        ]

    )
    print(response['choices'][0])

    message_content = response['choices'][0]['message']['content']

    prompts.append(
        {"role": "user", "content": prompt},

    )
    prompts.append(
        {"role": "assistant", "content": message_content},
    )
    
    return message_content


if __name__ == '__main__':
    app.run()
