from openai import OpenAI
import numpy as np
import sounddevice as sd
import llm_client
import threading

class TTS:
    def __init__(self, client, speaker):
        self.client = client
        self.speaker = speaker
        
        self.is_speaking = False
        
        self._audio_bytes = None
        self._thread = None
    
    def speak(self, text: str):
        print("[ TTS_SERVICE.PY ] Requesting TTS audio...")
        response = self.client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=text,
            response_format="pcm",
        )

        self._audio_bytes = response.read()
        print(f"[ TTS_SERVICE.PY ] Received {len(self._audio_bytes)} bytes of audio. Sending to speaker.")
        
        
        self._play_audio()

        print("[ TTS_SERVICE.PY ] Done!")  
    
    def _play_audio(self):
        if self._audio_bytes is None:
            return
        
        self.is_speaking = True
        self.speaker.play(self._audio_bytes)
        self.is_speaking = False
        self._audio_bytes = None
        