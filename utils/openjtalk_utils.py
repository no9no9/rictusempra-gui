import pyopenjtalk
import numpy as np
import librosa
from scipy.io import wavfile

class OpenJTalk:
    def __init__(self):
        self.sr = 16000

    def text2wav(self, text, path="tmp/test.wav"):
        wav, orig_sr = pyopenjtalk.tts(text)
        wav = resampling(wav, orig_sr, out_sr=self.sr)
        wavfile.write(path, self.sr, wav.astype(np.int16))
        return wav, self.sr


def resampling(data, sr, out_sr):
    return librosa.resample(y=data,orig_sr=sr, target_sr=out_sr)