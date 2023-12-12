import tkinter as tk
import os
import numpy as np
import matplotlib.pyplot as plt
import simpleaudio
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.io import wavfile
from utils.openjtalk_utils import OpenJTalk
from utils.voicevox_utils import Voicevox

class Text2LaughterApp:
    def __init__(self,master):
        self.app_dir = os.path.abspath(os.path.dirname(__file__))
        self.master = master
        self.master.title("Text to Laughter")

        self.text_label = tk.Label(master, text="Enter Text:")
        self.text_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.text_entry = tk.Entry(master, width=50)
        self.text_entry.grid(row=0, column=1, padx=10, pady=10)

        self.synthesize_button = tk.Button(master, text="Synthesize", command=self.synthesize_text)
        self.synthesize_button.grid(row=2, column=0, pady=20)

        self.play_button = tk.Button(master, text="Play", command=self.play_sound)
        self.play_button.grid(row=2, column=1, pady=20)

        self.plot_frame = tk.Frame(master)
        self.plot_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.tts_engine = OpenJTalk()

        self.sr, self.wav = wavfile.read(os.path.join(self.app_dir, "tmp","test.wav"))

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)   
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.tts_engine_label = tk.Label(master, text="TTS Engine:")
        self.tts_engine_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        self.tts_engine_var = tk.StringVar(master)
        self.tts_engine_var.set("OpenJTalk")
        self.tts_engine_dropdown = tk.OptionMenu(master, self.tts_engine_var, "OpenJTalk", "VOICEVOX", command=self.update_tts_engine)
        self.tts_engine_dropdown.grid(row=1, column=1, padx=10, pady=10)

    def update_tts_engine(self, engine):
        if engine == "OpenJTalk":
            self.tts_engine = OpenJTalk()
        elif engine == "VOICEVOX":
            self.tts_engine = Voicevox()

    def synthesize_text(self):
        text = self.text_entry.get()
        self.wav, self.sr = self.tts_engine.text2wav(text)
        wavfile.write("tmp/test.wav", self.sr, self.wav.astype(np.int16))
        self.plot_waveform()

    def plot_waveform(self):
        duration = len(self.wav)/self.sr 
        time = np.linspace(0., duration, len(self.wav))

        # 波形描画
        plt.clf()
        plt.plot(time, self.wav.astype(np.int16)/32768.0)
        plt.title("Waveform")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.grid(True)

        # 描画をTkinterに埋め込む
        self.canvas.draw()

    def play_sound(self):
        play_obj = simpleaudio.play_buffer(self.wav.astype(np.int16), 1, 2, self.sr)
        play_obj.wait_done()
        


if __name__ == "__main__":
    root = tk.Tk()
    app = Text2LaughterApp(root)
    root.mainloop()

