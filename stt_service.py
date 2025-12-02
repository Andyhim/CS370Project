from openai import OpenAI
import config
from microphone import Microphone
import threading
import numpy as np
import wave
import io

class STT():
    def __init__(self, client, mic):
        print("[ STT_SERVICE.PY ] Initializing STT Service")
        self.client = client
        self.mic = mic
        
        self.samplerate = config.samplerate
        self.chunk_size = config.chunk_size
        
        self.is_listening = False
        self.audio_chunks = []
        
        self._thread = None
        
    def start_stt(self):
        if self.is_listening:
            return
        
        print("[ STT_SERVICE.PY ] Starting STT...")
        
        self.is_listening = True
        self.audio_chunks = []
        
        self.mic.open_stream()
        
        print("[ STT_SERVICE.PY ] Starting mic capture thread...")
        self._thread = threading.Thread(target=self._capture_loop, daemon=True)
        self._thread.start()
        
    def stop_stt(self):
        if not self.is_listening:
            return None
        
        print("[ STT_SERVICE.PY ] Stopping STT...")
        self.is_listening = False
        
        if self._thread is not None:
            self._thread.join() # wait for capture thread to finish capturing last chunk
            self._thread = None
            
        print("[ STT_SERVICE.PY ] Capture thread closed.")
        self.mic.close_stream()
        
        wav_bytes = self._build_wav_bytes(self.audio_chunks)
        
        print("[ STT_SERVICE.PY ] Sending audio bytes to LLM for transcription.")
        llm_transcription = self.client.audio.transcriptions.create(
            model="gpt-4o-transcribe",
            file=("audio.wav", wav_bytes)
        )
        
        print(f"[ STT_SERVICE.PY ] Transcription received:          ' {llm_transcription.text} '")
        print("[ STT_SERVICE.PY ] Sending text to robot.")
        return llm_transcription.text
        
    def _capture_loop(self):
        print("[ STT_SERVICE.PY ] Mic capture thread started.")
        while self.is_listening:
            chunk = self.mic.read_chunk()
            if chunk is not None:
                self.audio_chunks.append(chunk)
                
                
    def _build_wav_bytes(self, chunks):
        if not chunks:
            return b""
        
        print("[ STT_SERVICE.PY ] Building wav bytes...")
        
        pcm = np.concatenate(chunks, axis=0).astype(np.int16)
        
        buffer = io.BytesIO()
        
        with wave.open(buffer, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(self.samplerate)
            wf.writeframes(pcm.tobytes())
            
        buffer.seek(0)
        print("[ STT_SERVICE.PY ] Finished building wav bytes.")
        return buffer.read()
        