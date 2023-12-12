import sys
import json
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton
from PyQt5.QtMultimedia import QSound

from utils.voicevox_utils import Voicevox
from utils.openjtalk_utils import OpenJTalk

class TextToSpeechGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("テキスト音声合成")
        self.setGeometry(100, 100, 400, 200)

        self.text_label = QLabel(self)
        self.text_label.setText("テキスト入力:")
        self.text_label.move(20, 20)

        self.text_entry = QLineEdit(self)
        self.text_entry.setGeometry(120, 20, 260, 30)

        self.generate_button = QPushButton("音声生成", self)
        self.generate_button.setGeometry(150, 70, 100, 30)
        self.generate_button.clicked.connect(self.generate_speech)

        self.play_button = QPushButton("再生", self)
        self.play_button.setGeometry(150, 120, 100, 30)
        self.play_button.clicked.connect(self.play_sound)

        self.tts_engine = OpenJTalk()

    def generate_speech(self):
        text = self.text_entry.text()
        wav, sr = self.tts_engine.text2wav(text)
        self.wav_data = wav
        print("音声生成完了")

    def play_sound(self):
        if hasattr(self, 'wav_data'):
            sound = QSound('tmp/test.wav')
            print("音声再生")
            sound.play()
        
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = TextToSpeechGUI()
    gui.show()
    sys.exit(app.exec_())
