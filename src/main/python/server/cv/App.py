import pyaudio
import numpy as np
from PyQt5 import QtWidgets, QtCore,QtSvg
from PyQt5.QtGui import QPainter


class VibrateRectangle(QtWidgets.QWidget):
    index = 0
    def __init__(self):
        super().__init__()

        self.frequency = 0
        self.amplitude = 0
        self.renderer = QtSvg.QSvgRenderer('C:\\Users\\Ananiya\\IdeaProjects2\\ReQ\\src\\main\\python\\client\\linux_64\\main\\ui\\g.svg')
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.timeout.connect(self.mn)
        self.timer.start(50)
        
        

        self.show()

    def nn(self, input):
     
        
        # Define some sample text
        text = input
        # Convert text to ASCII values
        ascii_values = [ord(c) for c in text]
    

        return (ascii_values)
    
    def mn(self):
        self.index = self.index +1
        self.amplitude = self.nn(""" 
        Notice the plot accurately renders time which is derived from the WAV file headers which defines the sample rate ... along with bit depth and channel count ... those attributes give the code ability to parse the binary WAV file byte by byte which get rendered as a series of points on the displayed curve ( each point is an audio sample for given channel )""")[self.index]*10000
         
    def paintEvent(self, event):
        painter = QPainter(self)
        # painter.setBrush(QtCore.Qt.red)
        x = self.width() / 2
        y = self.height() / 2
        w = self.renderer.defaultSize().width()
        h = self.renderer.defaultSize().height()
        print(self.amplitude /1000)
        if((self.amplitude / 1000000 )>1):
           w = self.renderer.defaultSize().width() * (self.amplitude / 1000000)
           h = self.renderer.defaultSize().height() * (self.amplitude /1000000)
        self.renderer.render(painter, QtCore.QRectF(x - w / 2, y - h / 2, w, h))

    def closeEvent(self, event):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        event.accept()

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = VibrateRectangle()
    sys.exit(app.exec_())