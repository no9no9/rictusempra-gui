import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QMessageBox

class AudioProcessingApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("音声処理アプリ")

        # 入力WAVEデータのパス
        self.input_path_label = QLabel("入力WAVEデータのパス:")
        self.input_path_entry = QLineEdit(self)
        self.browse_input_button = QPushButton("参照", self)
        self.browse_input_button.clicked.connect(self.browse_input_path)

        # 保存先のパス
        self.output_path_label = QLabel("保存先のパス:")
        self.output_path_entry = QLineEdit(self)
        self.browse_output_button = QPushButton("参照", self)
        self.browse_output_button.clicked.connect(self.browse_output_path)

        # 実行ボタン
        self.process_button = QPushButton("処理開始", self)
        self.process_button.clicked.connect(self.process_audio)

        # レイアウト
        layout = QVBoxLayout(self)
        layout.addWidget(self.input_path_label)
        layout.addWidget(self.input_path_entry)
        layout.addWidget(self.browse_input_button)
        layout.addWidget(self.output_path_label)
        layout.addWidget(self.output_path_entry)
        layout.addWidget(self.browse_output_button)
        layout.addWidget(self.process_button)

        self.show()

    def browse_input_path(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "入力WAVEデータの選択", "", "WAVE files (*.wav);;All Files (*)")
        if file_path:
            self.input_path_entry.setText(file_path)

    def browse_output_path(self):
        dir_path = QFileDialog.getExistingDirectory(self, "保存先の選択")
        if dir_path:
            self.output_path_entry.setText(dir_path)

    def process_audio(self):
        input_path = self.input_path_entry.text()
        output_path = self.output_path_entry.text()

        if input_path and output_path:
            try:
                # WAVEデータの読み込みと処理
                # ここに音声処理のコードを追加する
                # 例: audio = audio.reverse()

                # 処理された音声を保存
                
                QMessageBox.information(self, "処理完了", "音声の処理が完了しました。")
            except Exception as e:
                QMessageBox.critical(self, "エラー", f"エラーが発生しました: {str(e)}")
        else:
            QMessageBox.warning(self, "入力エラー", "入力WAVEデータのパスと保存先のパスを指定してください.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = AudioProcessingApp()
    sys.exit(app.exec_())
