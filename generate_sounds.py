# generate_sounds.py
import numpy as np
import wave
import struct
import os

SOUNDS_DIR = "sounds"
os.makedirs(SOUNDS_DIR, exist_ok=True)

def generate_tone(filename, freq, duration=0.15, volume=0.5):
    """Generate a short tone and save as a .wav file."""
    sample_rate = 44100
    amplitude = 32767 * volume
    num_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, num_samples, False)
    wave_data = np.sin(2 * np.pi * freq * t)

    # Convert to 16-bit data
    wave_data = np.int16(wave_data * amplitude)

    with wave.open(os.path.join(SOUNDS_DIR, filename), "w") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        for sample in wave_data:
            wav_file.writeframes(struct.pack('<h', sample))

def main():
    print("🎵 Generating game sound effects...")

    generate_tone("paddle_hit.wav", freq=600, duration=0.1, volume=0.5)
    generate_tone("wall_bounce.wav", freq=400, duration=0.12, volume=0.4)
    generate_tone("score.wav", freq=900, duration=0.3, volume=0.7)

    print("✅ Sound files generated in /sounds folder.")

if __name__ == "__main__":
    main()
