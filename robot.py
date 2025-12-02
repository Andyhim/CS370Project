from openai import OpenAI
import llm_client
import tts_service
import config
from config import State
import time
from button import Button
from led import LEDController
from stt_service import STT
from llm_service import LLM
from tts_service import TTS
import llm_client
from microphone import Microphone
from speaker import Speaker
import threading
import faces
from display import Display

class Robot:
    def __init__(self):
        print("[ ROBOT.PY ] Initializing Robot.")
        self.is_running = False
        
        from state_manager import StateManager
        self.state_manager = StateManager(robot_inst=self)
        
        self.listen_button = Button(pin=4)
        self.listen_button.register_callback(self.state_manager.prompt_button_push)
        
        self.led = LEDController(red_pin=13, green_pin=6, blue_pin=5)
        self.led.set_state(self.state_manager.state)
        
        self.display = Display()
        self.display.current_face = faces.IDLE
        self._dis_thread = threading.Thread(target=self.display.display_face, daemon=True)
        self._dis_thread.start()
        
        self.mic = Microphone()
        self.speaker = Speaker()
        
        self.client = llm_client.get_client()
        
        self.stt = STT(self.client, self.mic)
        self.llm = LLM(self.client)
        self.tts = TTS(self.client, self.speaker)
        
        self._tts_thread = None
        
    def set_state(self, new_state):
        print(f"[ ROBOT.PY ] set_state called. Sending new state to manager: {new_state}")
        self.state_manager.set_state(new_state)
        self.led.set_state(self.state_manager.state)
        self.display.frame = 1
        self.display.current_face = faces.get(new_state.name)
        
    def run(self):
        print("[ ROBOT.PY ] RUNNING ROBOT...")
        self.is_running = True
        
        while self.is_running:
            if self.state_manager.state == State.IDLE:
                time.sleep(config.tick_speed)
            
            elif self.state_manager.state == State.LISTENING:
                # print("[ ROBOT.PY ] Now in state LISTENING")
                # run STT
                self.do_listening()
                
            elif self.state_manager.state == State.THINKING:
                # run LLM
                self.do_thinking()
            
            elif self.state_manager.state == State.SPEAKING:
                # run TTS
                self.do_speaking()
                    
    def do_listening(self):
        self.stt.start_stt()
        
    def do_thinking(self):
        text = self.stt.stop_stt()
        response = self.llm.prompt(text)
      
        self._tts_thread = threading.Thread(target=self.tts.speak, kwargs={"text": response}, daemon=True)
        self._tts_thread.start()
        while(not self.tts.is_speaking):
            pass
        self.set_state(State.SPEAKING)
        
    def do_speaking(self):
        if self._tts_thread is not None:
            self._tts_thread.join() # wait for speaker thread to stop playing
            self._tts_thread = None

        self.set_state(State.IDLE)
        
    def cleanup(self):
        print("[ ROBOT.PY ] Goodbye!")
        self.led.all_off()
        self.display.done = True
        self._dis_thread.join()
        self.display.clear()
        