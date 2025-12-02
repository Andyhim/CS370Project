from enum import Enum

class State(Enum):
    IDLE = 0
    LISTENING = 1
    THINKING = 2
    SPEAKING = 3
    
bouncetime = 200 # used to eliminate button "bounce"

tick_speed = 0.05 # how quickly robot should check for a new state while idle

# for STT service
samplerate = 16000 # mic sample rate
chunk_size = 1024 # size for chunks STT reads from mic

# for sounddevice
mic_hw_device = 1
spkr_device = "hw:0,0"

# for LLM service
gpt_model = "gpt-4o-mini"

# for speaker
api_fs = 24000 # sample frequency from gpt api audio
dac_fs = 48000 # sample frequency the dac is expecting