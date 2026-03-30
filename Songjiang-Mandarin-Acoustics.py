import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import os

def analyze_speech(file_path, label):
    # Load audio file
    y, sr = librosa.load(file_path, sr=None)
    
    # Create figure for plotting
    plt.figure(figsize=(12, 8))
    
    # Plot Waveform
    plt.subplot(2, 1, 1)
    librosa.display.waveshow(y, sr=sr)
    plt.title(f'Waveform: {label}')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')

    # Compute Mel-Spectrogram
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
    S_dB = librosa.power_to_db(S, ref=np.max)

    # Plot Spectrogram
    plt.subplot(2, 1, 2)
    librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='mel')
    plt.colorbar(format='%+2.0f dB')
    plt.title(f'Mel-Spectrogram: {label}')
    
    plt.tight_layout()
    plt.show()

file_path_sj = 'audio_sj/01.wav'
file_path_md = 'audio_md/01.wav'

analyze_speech(file_path_sj, 'Songjiang Wu - Sentence 01')
analyze_speech(file_path_md, 'Mandarin - Sentence 01')

print(f"Current Working Directory: {os.getcwd()}")
print(f"Files in this folder: {os.listdir('.')}")