import sounddevice as sd
import numpy as np
import time

mic_card = 1   # your mic card number from arecord -l
dac_card = 1   # your DAC card number from aplay -l
fs = 44100

def callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    # convert mono -> stereo if needed and S32->S16
    if indata.shape[1] > 1:
        mono = indata.mean(axis=1, keepdims=True)
    else:
        mono= indata
    
    outdata[:] = mono

with sd.Stream(samplerate=fs,
               blocksize=1024,
               dtype='int32',
               channels=1,
               device=(mic_card, dac_card),
               callback=callback):
    print("Megaphone live! Press Ctrl+C to stop")
    while True:
        time.sleep(1)
