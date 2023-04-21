from nlp import decision_d_bert
from intermidiate import App
from flask import Flask

app = Flask(__name__)

if __name__ == '__main__':
    app.register_blueprint(decision_d_bert.app)
    app.register_blueprint(App.app)
    app.run()
