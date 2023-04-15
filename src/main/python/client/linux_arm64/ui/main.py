import nltk
from PyQt5.QtCore import QPointF
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from io import BytesIO
from PIL import Image
from math import sin, pi
import sys
import pyaudio
import struct
import pvporcupine
from PyQt5.QtCore import Qt
import speech_recognition as sr
from PyQt5 import QtWidgets, QtCore, QtGui, QtSvg
import speech_recognition as sr
import threading
import time
import requests
import cv2
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import requests
from PyQt5.QtGui import QPalette
import os
import yaml
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def stemmer(sent):
    ps = PorterStemmer()

    words = word_tokenize(sent)

    stemmed_words = [ps.stem(word) for word in words]

    return (stemmed_words)


path = os.getcwd()


with open(f'{path}/keys.yaml') as file:
    kfk = yaml.safe_load(file)['keys']
    if 'nt' == os.name:
        P_API_KEY = kfk['porcupine_win']['API_KEYS']
        P_PATH = f'{path}/assets/req_nt.ppn'
    else:
        P_API_KEY = kfk['porcupine_rasp']['API_KEYS']
        P_PATH = f'{path}/assets/req_lin.ppn'


class MainWindow(QtWidgets.QMainWindow):
    transcription_signal = QtCore.pyqtSignal(str, str)

    def __init__(self):
        super().__init__()

        self.setWindowTitle('PyQt5 App with Black Title Bar')
        
        self.showFullScreen()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.porcupine = pvporcupine.create(P_API_KEY, keyword_paths=[
            P_PATH], sensitivities=[1.0])
        self.r = sr.Recognizer()
        self.setStyleSheet(
            " QMainWindow{background-color: #171717} QLabel{font-size: 18pt; font-family:Source Code Pro; color:#AAAAAA;  font-weight: bold}")

        self.svg_widget = SVGWidget(
            f'{path}/assets/logo_normal.svg')
        self.svg_widget2 = SVGWidget(
            f'{path}/assets/logo_angry.svg'
        )
        self.text_ = QtWidgets.QLabel("ReQ", self)
        self.text_.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_.setWordWrap(True)
        self.timer = QtCore.QTimer()
        self.transcription_signal.connect(self.update_transcription)
        self.timer.timeout.connect(self.spin_svg)
        # self.timer.start(10)

        self.mlayout = QtWidgets.QVBoxLayout()

        self.mlayout.addWidget(self.svg_widget)
        self.mlayout.addWidget(self.text_)

        self.is_svg_spinning = False
        self.is_svg_vibrating = (False, None)
        self.is_svg_bouncing = False
        p = pyaudio.PyAudio()
        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')

        for i in range(0, numdevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get(
                    'name'),  p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels'))
        self.audio_stream = p.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length,
            stream_callback=self.audio_callback,
        )

        widget = QtWidgets.QWidget()
        widget.setLayout(self.mlayout)
        self.setCentralWidget(widget)

    def update_transcription(self, pre, text):
        if analyze_sentiment(text):
            #    self.mlayout.insertWidget(self.svg_widget2)
            self.mlayout.replaceWidget(self.svg_widget, self.svg_widget2)
            self.svg_widget.hide()
            self.svg_widget2.show()

        self.text_.setText(f"{pre}: {text}")

    def spin_svg(self):

        self.svg_widget.angle += 10
        self.svg_widget.is_bouncing = False
        self.svg_widget.update()

    def vibrate_svg(self, input):
        self.svg_widget.vibrate(input)
        self.svg_widget.update()

    def bounce_svg(self):
        self.svg_widget.bounce()
        self.svg_widget.update()
    def reset_svg_rotation(self):
        self.angle = 0


    def reset_svg_vib(self):
        self.svg_widget.reset_vibration()

    def audio_callback(self, in_data, frame_count, time_info, status):
        pcm = struct.unpack_from("h" * self.porcupine.frame_length, in_data)
        keyword_index = self.porcupine.process(pcm)

        if keyword_index >= 0:
            self.is_svg_spinning = False
            self.is_svg_vibrating = (False, None)

            print(f'Lis')
            self.text_.setText(f'Listeneing')
            self.is_svg_bouncing = True

            if self.mlayout.indexOf(self.svg_widget2) >= 0:
                
                self.mlayout.replaceWidget(self.svg_widget2, self.svg_widget)
                self.svg_widget.show()
                self.svg_widget2.hide()

            threading.Thread(target=self.record, daemon=True).start()

        if self.is_svg_spinning:

            self.spin_svg()
        if self.is_svg_vibrating[0]:
            self.vibrate_svg(self.is_svg_vibrating[1])
        elif self.is_svg_vibrating[0] == False:
            self.reset_svg_vib()

        if self.is_svg_bouncing:
            self.reset_svg_rotation()
            self.bounce_svg()

        return None, pyaudio.paContinue

    def record(self):

        r = self.r
        #
        r.dynamic_energy_threshold = False
        with sr.Microphone() as source:

            audio = r.listen(source, 10.0, 3.0)

            # recognize speech using Google Speech Recognition
            try:
                

                transcription = r.recognize_google(audio)

                self.transcription_signal.emit("Proccessing", transcription)
                self.is_svg_bouncing = False
                self.is_svg_spinning = True

                # self.is_svg_vibrating = (True, transcription)
                if(int(decision_d_bert(transcription)) == 1):
                    self.transcription_signal.emit('',str(vit(transcription)))
                else:
                    self.transcription_signal.emit('',str(gpt3_5(transcription)))

               
            except sr.UnknownValueError:
                self.transcription_signal.emit(
                    "Error", "Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                self.transcription_signal.emit("Error",
                                               "Could not request results from Google Speech Recognition service; {0}".format(e))

    def closeEvent(self, event):
        self.audio_stream.stop_stream()
        self.audio_stream.close()
        event.accept()


class SVGWidget(QtWidgets.QWidget):
    index = 0

    def __init__(self, file_path):
        super().__init__()
        self.amplitude = 0
        self.index = 0
        self.is_bouncing = False
        self.bounce_vel = 1.1
        self.bounce_time = 0
        self.bounce_acc = 0.8
        self.bounce_pos = QPointF(0, 1)
        self.renderer = QtSvg.QSvgRenderer(file_path)
        self.angle = 0

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        # size = min(self.width(), self.height())
        # painter.setViewport((self.width() - size), (self.height() - size), size, size)
        # # painter.setWindow(self.renderer.viewBox())

        x = (self.width()/2)
        if(self.is_bouncing == True):
          
          y = (self.height()/2) + (self.bounce_pos.y()*10)
        else:
          y = self.height()/ 2
        w = self.renderer.defaultSize().width()
        h = self.renderer.defaultSize().height()
        if ((self.amplitude / 1000000) > 1):
            w = self.renderer.defaultSize().width() * (self.amplitude / 1000000)
            h = self.renderer.defaultSize().height() * (self.amplitude / 1000000)
        transform = QtGui.QTransform().translate(self.width() / 2, self.height() / 2).rotate(self.angle).translate(
            -self.width() / 2, -self.height() / 2)
        painter.setTransform(transform)

        self.renderer.render(painter, QtCore.QRectF(
            x - w / 2, y - h / 2, w, h))

    def vibrate(self, input):
        self.is_bouncing = False
        if (self.index < len(input)):
            self.index = self.index + 1
            print(self.index)
            self.amplitude = [
                *self._text_to_ascii(input), 10][self.index]*12000

    def _norm(self, value):
        return abs(sin((value*pi)/(7*2))*7)

    def bounce(self):
        self.angle = 0
        self.is_bouncing = True
        self.bounce_time = self.bounce_time + 1
        velocity = QPointF(0, (self.bounce_acc * self._norm(self.bounce_time)))
        if (velocity.y() > 0):
            self.bounce_pos = + velocity  # accelerating
        elif (velocity.y() < 0):
            self.bounce_pos = velocity

        print(self.bounce_pos, self._norm(self.bounce_time))
        if (self.bounce_time == 7):
            self.bounce_acc = -self.bounce_acc

    def reset_vibration(self):
        self.index = 0
    def reset_angle(self):
        self.angle = 0

    def _text_to_ascii(self, input):

        # Define some sample text
        text = input
        # Convert text to ASCII values
        ascii_values = [ord(c) for c in text]

        return (ascii_values)


def vit(transcription):

    # Open a connection to the camera
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    # Capture a frame from the camera
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    buf = BytesIO()
    image.save(buf, format='JPEG')

    # Send the image to the Flask server

    # Encode the frame as a JPEG image

    # Send the image to the API as a POST request
    # TODO Set this up
    SERVER_URL = 'http://b207-34-126-120-211.ngrok.io'

    # Set the data to send in the request
    data = {

        'question': transcription
    }

    # Send a POST request to the Flask server's '/intermidiate/vit' route
    response = requests.post(
        SERVER_URL + '/intermidiate/vit', data=data, files={'image': buf.getvalue()})

    # Get the answer from the response
    answer = response.text
    # Print the response from the API
    print(response.text)

    return f'<b>{answer}</b>'

    # Release the camera resource


def gpt3_5(trancription):

    # TODO Set this up
    url = ' '

    payload = {'prompt': trancription}

    headers = {
        'prompt': trancription
    }

    response = requests.request(
        "POST", url, headers=headers, data=payload, files=[])
    return response


def decision_d_bert(trancription):
   url = ' '

   payload={'question': trancription}
   
   response = requests.request("POST", url)

   print(response.text)

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
