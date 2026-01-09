from enum import Enum, auto
import time

# Fault injector
class FaultInjector:
    fault = False

# Landing gear states
class GearState(Enum):
    UP_LOCKED = auto()
    TRANSITIONING_DOWN = auto()
    DOWN_LOCKED = auto()
    TRANSITIONING_UP = auto()
    FAULT = auto()

class LandingGearController:

    # Requirements PER-02 and PER-03
    GEAR_DOWN_TIME = 5 #seconds
    GEAR_UP_TIME = 7 #seconds

    def __init__(self):
        self.state = GearState.UP_LOCKED

    def log(self, message):
        print(f"[{self.state.name}] {message}")

    def move_gear(self, target_state):
        if FaultInjector.fault:
            self.state = GearState.FAULT
            self.log("Fault detected - command rejected")
            return
        
        #Gear DOWN sequence
        if target_state == GearState.DOWN_LOCKED:
            if self.state != GearState.UP_LOCKED:
                self.log("Gear down command rejected")
                return
        
            self.state = GearState.TRANSITIONING_DOWN
            self.log("Gear deploying...")
            time.sleep(self.GEAR_DOWN_TIME)

            self.state = GearState.DOWN_LOCKED
            self.log("Gear down and locked")

        #Gear UP sequence
        elif target_state == GearState.UP_LOCKED:
            if self.state != GearState.DOWN_LOCKED:
                self.log("Gear up command rejected")
                return
            
            self.state = GearState.TRANSITIONING_UP
            self.log("Gear retracting...")
            time.sleep(self.GEAR_UP_TIME)

            self.state = GearState.UP_LOCKED
            self.log("Gear up and locked")

    def command_gear_down(self):
        self.move_gear(GearState.DOWN_LOCKED)

    def command_gear_up(self):
        self.move_gear(GearState.UP_LOCKED)

controller = LandingGearController()
# ENTER COMMAND SEQUENCE TO CONTROL LANDING GEAR

controller.command_gear_up()
controller.command_gear_up()