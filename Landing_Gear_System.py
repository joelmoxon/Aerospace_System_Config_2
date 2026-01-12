from enum import Enum, auto
import time

# Landing gear states
class GearState(Enum):
    UP_LOCKED = auto()
    TRANSITIONING_DOWN = auto()
    DOWN_LOCKED = auto()
    TRANSITIONING_UP = auto()
    FAULT = auto()

# Simulated fault injection
class FaultInjector:
    fault = False
    fault_delay = 3 # additional gear movement time when fault occurs (seconds)

class LandingGearController:

    # Requirements PER-02 and PER-03
    GEAR_DOWN_TIME = 5 # seconds
    GEAR_UP_TIME = 7 # seconds

    def __init__(self):
        self.state = GearState.UP_LOCKED
        self.previous_state = GearState.UP_LOCKED

    def log(self, message):
        print(f"[{self.state.name}] {message}")

    def clear_fault(self):
        if self.state == GearState.FAULT:
            self.state = self.previous_state
            self.log("Fault cleared - system restored")
        else:
            print("\n[SYSTEM] No fault to clear")

    def move_gear(self, target_state):
         
        #Gear DOWN sequence
        if target_state == GearState.DOWN_LOCKED:
            if self.state != GearState.UP_LOCKED:
                self.log("Command rejected - Gear already DOWN")
                return
        
            self.state = GearState.TRANSITIONING_DOWN
            self.log("Gear deploying...")
            
            # Check for fault during DOWN movement
            if FaultInjector.fault:
                time.sleep(self.GEAR_DOWN_TIME)
                self.log("*** ALERT: Gear down time exceeded normal time")
                self.log("*** DIAGNOSIS: Low hydraulic pressure")
                self.log("*** Activating backup hydraulic pump ***")
                self.backup_pump_active = True
                time.sleep(FaultInjector.fault_delay)
                self.log("*** Operation complete ***")
                self.backup_pump_active = False
                FaultInjector.fault = False
                self.log("*** Fault cleared ***")
            else:
                time.sleep(self.GEAR_DOWN_TIME)
            
            self.state = GearState.DOWN_LOCKED
            self.log ("Gear down and locked")


        #Gear UP sequence
        elif target_state == GearState.UP_LOCKED:
            if self.state != GearState.DOWN_LOCKED:
                self.log("Command rejected - Gear already UP")
                return
            
            self.state = GearState.TRANSITIONING_UP
            self.log("Gear retracting...")
           
        # Check for fault during UP movement
            if FaultInjector.fault:
                time.sleep(self.GEAR_UP_TIME)
                self.log("*** ALERT: Gear up time exceeded normal time")
                self.log("*** DIAGNOSIS: Low hydraulic pressure")
                self.log("*** Activating backup hydraulic pump ***")
                self.backup_pump_active = True
                time.sleep(FaultInjector.fault_delay)
                self.log("*** Operation complete ***")
                self.backup_pump_active = False
                FaultInjector.fault = False
                self.log("*** Fault cleared ***")
            else:
                time.sleep(self.GEAR_DOWN_TIME)

            self.state = GearState.UP_LOCKED
            self.log("Gear up and locked")

    def command_gear_down(self):
        self.move_gear(GearState.DOWN_LOCKED)

    def command_gear_up(self):
        self.move_gear(GearState.UP_LOCKED)

# Control menu
def show_menu():
    print("\n" + "=" * 30)
    print("LANDING GEAR CONTROL SYSTEM")
    print("=" * 30)
    print("1. Gear DOWN")
    print("2. Gear UP")
    print("3. Inject Fault")
    print("4. clear fault")
    print("=" * 30)

def main():
    controller = LandingGearController()

    print("\n*** SYSTEM INITIALISING ***")
    print("Landing gear initialised in UP_LOCKED position")

    while True:
        show_menu()
        choice = input("Enter command: ")

        if choice == "1":
            controller.command_gear_down()
        elif choice == "2":
            controller.command_gear_up()
        elif choice == "3":
            FaultInjector.fault = True
            print("\n[SYSTEM] Fault injected")
        elif choice == "4":
            FaultInjector.fault = False
            controller.clear_fault()
        else:
            print("\n Invalid command. Please try again")

main()