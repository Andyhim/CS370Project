import numpy as np
import sounddevice as sd
from openai import OpenAI
import config

# Initialize API
client = OpenAI(api_key=config.OPENAI_API_KEY)

# ---------- TTS REQUEST ----------
text = "You're all I can think of, every drop I drink up. You're my soda pop, my little soda pop."

print("Requesting TTS audio...")
response = client.audio.speech.create(
    model="gpt-4o-mini-tts",
    voice="alloy",
    input=text,
    response_format="pcm",   # 16-bit PCM (works with aplay + sounddevice)
)

audio_bytes = response.read()
print(f"Received {len(audio_bytes)} bytes of audio.")


# ---------- PLAYBACK ----------
# Convert raw bytes → numpy array
audio_np = np.frombuffer(audio_bytes, dtype=np.int16)

API_FS = 24000
DAC_FS = 48000

audio_resampled = np.interp(
    np.linspace(0, len(audio_np), int(len(audio_np) * DAC_FS / API_FS), endpoint=False),
    np.arange(len(audio_np)),
    audio_np
    ).astype(np.int16)
                
print("Playing audio...")
sd.play(audio_resampled, samplerate=DAC_FS, device="hw:0,0")
sd.wait()
print("Done!")
