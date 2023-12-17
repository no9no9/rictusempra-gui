import requests
import json 
import time
import io
import wave
import numpy as np
import json

class Voicevox():
    def __init__(self, host="127.0.0.1", port="50021"):
        self.host = host
        self.port = port
        self.speakers = self.installed_styles()
        self.speaker = 1
        self.sr = 16000
        self.max_wav_value = 32768.0
        self.headers = {
            "Content-Type": "application/json"
        }
        self.params = dict(
            text='これはテスト音声です',
            speaker=self.speaker,
        )
        self.query = self.create_audio_query(**self.params)
    

    def create_audio_query(self, text, speaker, max_retry=5):
        params = dict(
            text=text,
            speaker=speaker,
        )
        for _ in  range(max_retry):
            response = requests.post(
                f'http://{self.host}:{self.port}/audio_query', 
                params=dict(
                    text=text,
                    speaker=speaker,
                ),
                timeout=(10.0, 300.0)
            )
            if response.status_code == 200:
                query = response.json()
                break
            time.sleep(1)
        else:
            raise ConnectionError("リトライ回数が上限に到達しました")
        return query
    
    def synthesis(self,params,query,max_retry=10):
        query['outputSamplingRate'] = self.sr 
        for _ in range(max_retry):
            response = requests.post(
                f'http://{self.host}:{self.port}/synthesis', 
                headers=self.headers, 
                params=params, 
                data=json.dumps(query),
                timeout=(10.0, 300.0)
            )
            if response.status_code == 200:
                return response.content
            time.sleep(1)
        else:
            raise ConnectionError("リトライ回数が上限に到達しました")    


    def text2wav(self, text, path='tmp/test.wav'):
        query = self.create_audio_query(text, self.speaker)
        params = dict(
            text=text,
            speaker=self.speaker,
        )
        wave_bytes = self.synthesis(params, query)
        with wave.open(io.BytesIO(wave_bytes), "rb") as wav:
            params = wav.getparams()
            wave_array = np.frombuffer(wav.readframes(wav.getnframes()), dtype=np.int16)
        return wave_array, self.sr

    def installed_styles(self):
        response = requests.get(f'http://{self.host}:{self.port}/speakers')
        return response.json()


    