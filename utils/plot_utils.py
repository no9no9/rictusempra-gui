import matplotlib.pyplot as plt
import librosa
import numpy as np

def plot_spectrogram(axes,wav,sr=16e3):
    spec = librosa.stft(wav, n_fft=1024, hop_length=320)
    spec_db = librosa.amplitude_to_db(np.abs(spec))
    frame_time = librosa.frames_to_time(np.arange(spec_db.shape[1]), sr=sr, hop_length=320)
    bin_freq = librosa.fft_frequencies(sr=sr, n_fft=1024)

    axes.imshow(spec_db, cmap='magma', origin='lower', aspect='auto')
    axes.set_xticks(np.arange(0, spec_db.shape[1], 10))
    axes.set_xticklabels(frame_time[np.arange(0, spec_db.shape[1], 10)])
    axes.set_yticks([0, 513-1])
    axes.set_yticklabels([int(bin_freq[0]), int(bin_freq[513-1])])
    axes.set_xlim(0, spec_db.shape[1]-1)

    
    