from enum import Enum, auto
import time

class FaultInjector:
    isfault = True

class GearState(Enum):
    UP_LOCKED = auto()
    TRANSITIONING_DOWN = auto()
    DOWN_LOCKED = auto()

class LandingGearController:
    def __init__(self):
        self.state = GearState.UP_LOCKED

    def log(self, message):
        print(f"[{self.state.name}] {message}")

    def command_gear_down(self):
        if FaultInjector.isfault:
            if self.state == GearState.UP_LOCKED:
                self.state = GearState.TRANSITIONING_DOWN
                self.log("Gear deploying")
                self.state = GearState.DOWN_LOCKED
                time.sleep(2)
                self.log("Gear locked down")
            else:
                self.log("Command rejected")
        else:
            self.log("Fault Detected")

controller = LandingGearController()
controller.command_gear_down()
