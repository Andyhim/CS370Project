from robot import Robot
import config
from config import State

class StateManager:
    def __init__(self, robot_inst: Robot):
        print("[ STATE_MANAGER.PY ] Initializing State Manager")
        self.robot = robot_inst
        self.state = State.IDLE
        
    # determines what has to be true before the robot can enter listening state
    def can_listen(self):
        return self.state == (State.IDLE or State.SPEAKING)
    
    def can_think(self):
        return self.state == State.LISTENING
    
    def can_speak(self):
        return self.state == State.THINKING
        
    def prompt_button_push(self):
        print(f"[ STATE_MANAGER.PY ] Prompt button push received. State = {self.state}")
        
        if self.can_listen():
            self.robot.set_state(State.LISTENING)
        elif self.can_think():
            self.robot.set_state(State.THINKING)
        else:
            print("[ STATE_MANAGER.PY ] Listen button push ignored.")
            
    def set_state(self, new_state):
        print(f"[ STATE_MANAGER.PY ] State transition: {self.state} -> {new_state}")
        self.state = new_state
        
        