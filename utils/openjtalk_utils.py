import pyopenjtalk
import numpy as np
import librosa
from scipy.io import wavfile

class OpenJTalk:
    def __init__(self):
        self.sr = 16000

    def text2wav(self, text, path="tmp/test.wav"):
        wav, orig_sr = pyopenjtalk.tts(text)
        wav = wav[round(orig_sr*0.2):-round(orig_sr*0.2)]
        wav = librosa.resample(y=wav,orig_sr=orig_sr, target_sr=self.sr)
        wavfile.write(path, self.sr, wav.astype(np.int16))
        return wav, self.sr
