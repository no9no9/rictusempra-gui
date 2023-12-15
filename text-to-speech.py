import tkinter as tk
import os
import numpy as np
import matplotlib.pyplot as plt
import simpleaudio
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.io import wavfile
from utils.openjtalk_utils import OpenJTalk
from utils.voicevox_utils import Voicevox
from utils.rictusempra_utils import Rictucempra

class Text2LaughterApp:
    def __init__(self,master):
        self.app_dir = os.path.abspath(os.path.dirname(__file__))
        self.master = master
        self.master.title("Text to Laughter")
        self.master.geometry("650x600")

        # Options
        self.options_frame = tk.LabelFrame(master,text="Options")
        self.options_frame.grid(row=0, column=0, padx=1, pady=1, sticky=tk.E+tk.W, columnspan=5, rowspan=1)

        self.tts_engine_var = tk.StringVar(self.options_frame)
        self.tts_engine_var.set("OpenJTalk")
        self.tts_engine_dropdown = tk.OptionMenu(self.options_frame, self.tts_engine_var, "OpenJTalk", "VOICEVOX", command=self.update_tts_engine)
        self.tts_engine_dropdown.grid(row=0, column=0, padx=1, pady=1)

        # Editors
        self.editor_frame = tk.Frame(master)
        self.editor_frame.grid(row=1, column=0, padx=10, pady=10, sticky=tk.NSEW, columnspan=4, rowspan=1)

        self.text_label = tk.Label(self.editor_frame, text="Enter Text:")
        self.text_label.grid(row=0, column=0, padx=3, pady=10)

        self.text_entry = tk.Entry(self.editor_frame, width=40)
        self.text_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.EW)

        self.synthesize_button = tk.Button(self.editor_frame, text="Synthesize", command=self.synthesize_text)
        self.synthesize_button.grid(row=0, column=2, padx=10, pady=10)  

        self.convert_button = tk.Button(self.editor_frame, text="Convert", command=self.convert_laughter)
        self.convert_button.grid(row=0, column=3, pady=10)

        # canvas and sound button
        self.plot_frame = tk.Frame(master)
        self.plot_frame.grid(row=2, column=0, columnspan=2, rowspan=1, padx=10, pady=10, sticky=tk.NSEW)

        self.play_button_frame = tk.Frame(self.plot_frame)
        self.play_button_frame.grid(row=0, column=0, columnspan=1,rowspan=2,padx=10, pady=10, sticky=tk.NS)
        self.play_button1 = tk.Button(self.play_button_frame, text="Speech", command=self.play_speech)
        self.play_button1.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)
        self.play_button2 = tk.Button(self.play_button_frame, text="Laugh", command=self.play_laughter)
        self.play_button2.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)

        self.canvas_frame = tk.Frame(self.plot_frame)
        self.canvas_frame.grid(row=0, column=1, padx=10, pady=10, sticky=tk.NSEW)
        self.fig, self.axes = plt.subplots(2, 1, figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.sr, self.wav = None, None
        self.tts_engine = OpenJTalk()
        self.rictusempra = Rictucempra()

    def update_tts_engine(self, engine):
        if engine == "OpenJTalk":
            self.tts_engine = OpenJTalk()
        elif engine == "VOICEVOX":
            self.tts_engine = Voicevox()

    def synthesize_text(self):
        self.clear_plot()
        text = self.text_entry.get()
        wav, sr = self.tts_engine.text2wav(text)
        wavfile.write(os.path.join(self.app_dir, "tmp","test.wav"), sr, wav.astype(np.int16))
        self.sr, self.wav = wavfile.read(os.path.join(self.app_dir, "tmp","test.wav"))
        self.plot_waveform(self.wav, 0)

    def convert_laughter(self):
        self.laughter = self.rictusempra.speech2laughter(self.wav)
        self.plot_waveform(self.laughter, 1)

    def plot_waveform(self, x, idx):
        duration = len(x)/self.sr 
        time = np.linspace(0., duration, len(x))
        if x.dtype == np.int16:
            x = x.astype(np.float32)/32768.0

        self.axes[idx].cla()
        self.axes[idx].plot(time, x)
        self.axes[idx].set_ylabel("Amplitude")
        self.axes[idx].set_xlim(0, duration)
        self.axes[idx].grid(True)

        self.canvas.draw()
    
    def clear_plot(self):
        self.axes[0].cla()
        self.axes[1].cla()
        self.canvas.draw()

    def play_speech(self):
        play_obj = simpleaudio.play_buffer(self.wav.astype(np.int16), 1, 2, self.sr)
        play_obj.wait_done()
    
    def play_laughter(self):
        laughter = (self.laughter*np.iinfo(np.int16).max).astype(np.int16)
        play_obj = simpleaudio.play_buffer(laughter, 1, 2, self.sr)
        play_obj.wait_done()
        

if __name__ == "__main__":
    root = tk.Tk()
    app = Text2LaughterApp(root)
    root.mainloop()

