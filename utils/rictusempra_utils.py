import os
import torch
import numpy as np
import onnxruntime

class Rictucempra:
    def __init__(self):
        self.extractor = onnxruntime.InferenceSession("model/wav2vec/wav2vec.onnx")
        self.converter = onnxruntime.InferenceSession("model/rictucempra/rictucempra.onnx")
        self.vocoder = onnxruntime.InferenceSession("model/vocoder/vocoder.onnx")
        self.default_speaker = np.array([112], dtype=np.int64)

    def speech2laughter(self, speech):
        max_pow = np.max(np.abs(speech))
        laughter = self.mel2wav(self.vector2mel(self.wav2vector(speech)))
        laughter = (laughter / np.max(np.abs(laughter))) * (max_pow/np.iinfo(np.int16).max)
        return laughter
    
    def wav2vector(self, wav):
        wav_float = torch.from_numpy((wav/ np.iinfo(np.int16).max).astype(np.float32)).unsqueeze(0).numpy()
        vector = self.extractor.run(None, {"input": wav_float})[0]
        return vector
    
    def vector2mel(self, vec, speaker=None):
        frame_len = vec.shape[1]
        if speaker is None:
            speaker = self.default_speaker
        else:
            speaker = np.array([speaker], dtype=np.int64)
        vec = torch.from_numpy(vec)
        vec =  torch.nn.functional.pad(vec,(0,0,0,1000-vec.shape[1]),value=0).numpy()
        mel = self.converter.run(None, {"speakers":speaker,"ppp": vec})[0][:,:frame_len,:]
        return mel
    
    def mel2wav(self, mel):
        wav = self.vocoder.run(None, {"input":mel.transpose(0,2,1)})[0][0,0,:]
        return wav
    