import sounddevice as sd
import numpy as np
import config

class Microphone():
    def __init__(self):
        print("[ MICROPHONE ] Initializing microphone.")
        self.stream = None
        
    def open_stream(self):
        if self.stream is not None:
            return
        print("[ MICROPHONE ] Opening microphone stream.")
        self.stream = sd.InputStream(
            samplerate = config.samplerate,
            channels=1,
            dtype="int16"
        )
        self.stream.start()
        
    def read_chunk(self):
        if self.stream is None:
            return None
        
        # print("[ MICROPHONE ] Reading microphone capture chunk.")
        
        audio, overflowed = self.stream.read(config.chunk_size)
        if overflowed:
            print("[ MICROPHONE.PY ] WARNING: Overflow in microphone buffer!")
            
        return audio.copy()
    
    def close_stream(self):
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
            self.stream = None
            print("[ MICROPHONE ] Closed microphone stream.")