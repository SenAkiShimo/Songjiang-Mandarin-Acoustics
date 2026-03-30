import os
import numpy as np
import parselmouth
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def get_normalized_pitch(file_path, n_points=100):
    try:
        snd = parselmouth.Sound(file_path)
        # Extract pitch
        pitch = snd.to_pitch()
        pitch_values = pitch.selected_array['frequency']
        
        # Filter out zeros
        valid_pitch = pitch_values[pitch_values > 0]
        
        if len(valid_pitch) < 5: # Skip too short or silent
            return None
        
        # Time-normalization
        current_indices = np.linspace(0, 1, len(valid_pitch))
        target_indices = np.linspace(0, 1, n_points)
        interpolator = interp1d(current_indices, valid_pitch, kind='linear')
        
        return interpolator(target_indices)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def main():
    folders = {
        'Songjiang': 'audio_sj', 
        'Mandarin': 'audio_md'
    }
    
    n_points = 100
    plt.figure(figsize=(10, 6))
    
    # Process each language
    for lang, folder_path in folders.items():
        all_contours = []
        
        if not os.path.exists(folder_path):
            print(f"Directory not found: {folder_path}")
            continue
            
        files = [f for f in os.listdir(folder_path) if f.endswith('.wav')]
        print(f"Found {len(files)} files in {lang} folder.")

        for filename in files:
            path = os.path.join(folder_path, filename)
            contour = get_normalized_pitch(path, n_points)
            if contour is not None:
                all_contours.append(contour)
        
        if len(all_contours) > 0:
            # Calculate mean and standard deviation
            mean_contour = np.mean(all_contours, axis=0)
            std_contour = np.std(all_contours, axis=0)
            
            x = np.arange(n_points)
            # Plot the mean line
            plt.plot(x, mean_contour, label=f'Mean {lang}', linewidth=2)
            # Standard Deviation
            plt.fill_between(x, mean_contour - std_contour, mean_contour + std_contour, alpha=0.2)
        else:
            print(f"No valid pitch data found for {lang}")

    # 3. Plot formatting
    plt.title('Normalized Pitch Contour: Songjiang Wu vs Mandarin')
    plt.xlabel('Time Progress (%)')
    plt.ylabel('Frequency (Hz)')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
