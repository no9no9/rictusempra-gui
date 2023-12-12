import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton
import requests
import wave

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

    def generate_speech(self):
        text = self.text_entry.text()
        if text:
            # VOICEVOXのREST APIエンドポイント
            host = "127.0.0.1"
            port = "50021"
            # リクエストヘッダー
            headers = {
                "Content-Type": "application/json"
            }
            # リクエストボディ
            params = (
                ('text',text),
                ('speaker', '1')
            )
            query = requests.post(f'http://{host}:{port}/audio_query', params=params)
            try:
                # POSTリクエストを送信
                response = requests.post(f'http://{host}:{port}/synthesis', headers=headers, params=params,json=json.dumps(query.json()))
                # レスポンスの音声データを取得
                audio_data = response.content
                # 音声データをファイルに保存
                wf = wave.open("output.wav", "wb")
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(24000)
                wf.writeframes(audio_data)
                wf.close()
                # 音声再生などの処理を追加
                # ...
            except requests.exceptions.RequestException as e:
                print("音声生成に失敗しました:", e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = TextToSpeechGUI()
    gui.show()
    sys.exit(app.exec_())
