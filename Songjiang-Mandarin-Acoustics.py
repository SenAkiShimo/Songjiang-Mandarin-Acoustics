import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import os
import parselmouth
import pandas as pd

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

import os
import librosa
import parselmouth
import numpy as np
import pandas as pd

def extract_features(file_path, label):
    #for MFCC
    y, sr = librosa.load(file_path, sr=None)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_mean = np.mean(mfccs, axis=1) # Average over time

    #for Pitch
    snd = parselmouth.Sound(file_path)
    pitch = snd.to_pitch()
    pitch_values = pitch.selected_array['frequency']
    
    # Filter out no voice
    pitch_values = pitch_values[pitch_values > 0]
    
    if len(pitch_values) > 0:
        mean_pitch = np.mean(pitch_values)
        max_pitch = np.max(pitch_values)
        min_pitch = np.min(pitch_values)
        pitch_range = max_pitch - min_pitch
    else:
        mean_pitch = max_pitch = min_pitch = pitch_range = 0

    return {
        'label': label,
        'mean_pitch': mean_pitch,
        'pitch_range': pitch_range,
        'mfcc_1': mfcc_mean[0]
    }

results = []
folders = {'Songjiang': 'audio_sj', 'Mandarin': 'audio_md'}

for lang, folder_path in folders.items():
    files = sorted([f for f in os.listdir(folder_path) if f.endswith('.wav')])
    
    for filename in files:
        full_path = os.path.join(folder_path, filename)
        print(f"Processing: {full_path}")
        features = extract_features(full_path, lang)
        results.append(features)

df = pd.DataFrame(results)
print("\n--- Feature Summary ---")
print(df.groupby('label').mean()) # See the averages per language

# Optional: Save to CSV for later
# df.to_csv('acoustic_results.csv', index=False)


#file_path_sj = 'audio_sj/01.wav'
#file_path_md = 'audio_md/01.wav'

#analyze_speech(file_path_sj, 'Songjiang Wu - Sentence 01')
#analyze_speech(file_path_md, 'Mandarin - Sentence 01')

#print(f"Current Working Directory: {os.getcwd()}")
#print(f"Files in this folder: {os.listdir('.')}")