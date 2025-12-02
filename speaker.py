import numpy as np
import sounddevice as sd
import config

class Speaker:
    def __init__(self):
        print("[ SPEAKER.PY ] Initializing speaker.")
    
    def play(self, audio_bytes):
        print("[ SPEAKER.PY ] Audio received.")
        audio_np = np.frombuffer(audio_bytes, dtype=np.int16)

        audio_resampled = np.interp(
            np.linspace(0, len(audio_np), int(len(audio_np) * config.dac_fs / config.api_fs), endpoint=False),
            np.arange(len(audio_np)),
            audio_np
            ).astype(np.int16)
                        
        print("[ SPEAKER.PY ] Playing audio...")
        sd.play(audio_resampled, samplerate=config.dac_fs, device=config.spkr_device)
        sd.wait()
        print("[ SPEAKER.PY ] Audio finished playing.")