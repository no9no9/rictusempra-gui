import os
import torch

from model.rictucempra.fastspeech2 import FastSpeech2

class Rictucempra:
    def __init__(self):
        self.converter = FastSpeech2()

    def speech2laughter(self, wav):
        return wav
    
    def wav2hubert(self, wav):
        return wav
    
    def hubert2mel(self, hub):
        return hub
    
    def mel2wav(self, mel):
        return mel
    