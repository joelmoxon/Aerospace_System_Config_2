"""
===============================================================
BAE SYSTEMS - LANDING GEAR CONTROL SYSTEM
===============================================================

System Name:        Landing Gear Control System (LGCS)
Version:            1.0
Classification:     Prototype 

Created By:         Joel Moxon
Date Created:       3rd January 2026
Date Approved:      15th January 2026
Approved By:        Graham Burvill

Baseline ID:        LGCS-BL-1.0
Language:           Python 

Change History:
---------------------------------------------------------------
Version    Date           Author              Description
---------------------------------------------------------------
1.0      15/01/2026     Joel Moxon          Initial prototype 

===============================================================
"""
from enum import Enum, auto
import time
from datetime import datetime

# Landing gear states
class GearState(Enum):
    UP_LOCKED = auto()
    TRANSITIONING_DOWN = auto()
    DOWN_LOCKED = auto()
    TRANSITIONING_UP = auto()

# Simulated fault injection
class FaultInjector:
    fault = False
    fault_delay = 3 # additional gear movement time when fault occurs (seconds)

# Log events to console and file
class SystemLogger:
    def __init__(self, filename="landing_gear.log"):
        self.filename = filename
        with open(self.filename, 'w') as f:
            f.write(f"=== Landing Gear System Log ===\n")
            f.write(f"Log started: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n")
            f.write("=" * 30 + "\n\n")

    def write(self, message, state_name=None):
        timestamp = datetime.now().strftime("%H:%M:%S")
        if state_name:
            formatted = f"[{timestamp}] [{state_name}] {message}"
        else:
            formatted = f"[{timestamp}] {message}"
        print(formatted)
        with open(self.filename, 'a') as f:
            f.write(formatted + "\n")

class LandingGearController:

    # Timing requirements from PER-02 and PER-03
    GEAR_DOWN_TIME = 5 # seconds
    GEAR_UP_TIME = 7 # seconds

    def __init__(self, logger):
        self.state = GearState.DOWN_LOCKED
        self.logger = logger

    # Log function with timestamp
    def log(self, message):
        self.logger.write(message, self.state.name)

    # Function to view faults
    def view_fault(self):
        if FaultInjector.fault:
            print("\n[SYSTEM] *** HYDRAULIC FAULT ACTIVE ***")
            print("[SYSTEM] Primary hydraulic pump failure detected")
            print("[SYSTEM] Technician required before next flight")
            time.sleep(3)
        else:
            print("\n[SYSTEM] No active faults")
            time.sleep(2)

    def move_gear(self, target_state):
         
        # Gear DOWN sequence
        if target_state == GearState.DOWN_LOCKED:
            if self.state != GearState.UP_LOCKED:
                self.log("Command rejected - Gear already DOWN")
                return
        
            self.state = GearState.TRANSITIONING_DOWN
            self.log("Gear deploying...")
            
            # Check for fault during DOWN movement
            if FaultInjector.fault:
                time.sleep(self.GEAR_DOWN_TIME)
                self.log("*** ALERT: Gear down time exceeded parameter")
                time.sleep(2)
                self.log("*** ROOT CAUSE: Low hydraulic pressure - primary pump")
                time.sleep(2)
                self.log("*** Activating backup hydraulic pump ***")
                time.sleep(FaultInjector.fault_delay)
                self.log("*** Backup operation complete - hydraulic maintenance required ***")
                time.sleep(2)
            else:
                time.sleep(self.GEAR_DOWN_TIME)
            
            self.state = GearState.DOWN_LOCKED
            self.log("Gear down and locked")

        # Gear UP sequence
        elif target_state == GearState.UP_LOCKED:
            if self.state != GearState.DOWN_LOCKED:
                self.log("Command rejected - Gear already UP")
                return
            
            self.state = GearState.TRANSITIONING_UP
            self.log("Gear retracting...")
           
            # Check for fault during UP movement
            if FaultInjector.fault:
                time.sleep(self.GEAR_UP_TIME)
                self.log("*** ALERT: Gear up time exceeded parameter")
                time.sleep(2)
                self.log("*** ROOT CAUSE: Low hydraulic pressure - primary pump")
                time.sleep(2)
                self.log("*** FAILSAFE: Gear retraction aborted ***")
                time.sleep(2)
                self.state = GearState.DOWN_LOCKED
                self.log("*** Gear remains DOWN in failsafe mode ***")
                time.sleep(2)
                self.log("*** Hydraulic maintenance required ***")
                time.sleep(2)
                return
            else:
                time.sleep(self.GEAR_UP_TIME)

            self.state = GearState.UP_LOCKED
            self.log("Gear up and locked")

    # Function to move gear DOWN
    def command_gear_down(self):
        self.move_gear(GearState.DOWN_LOCKED)
   
    # Function to move gear UP
    def command_gear_up(self):
        self.move_gear(GearState.UP_LOCKED)

# Control menu
def show_menu(controller):
    print("\n" + "=" * 30)
    print("LANDING GEAR CONTROL SYSTEM")
    print("=" * 30)
    print(f"Current Position: {controller.state.name}")
    print("=" * 30)
    print("1. Gear UP")
    print("2. Gear DOWN")
    print("3. Inject Hydraulic Fault")
    print("4. View Faults")
    print("5. Simulate System Reset")
    print("=" * 30)

# Function to initialise menu and run commands
def main():
    logger = SystemLogger()
    controller = LandingGearController(logger)

    time.sleep(1)
    print("\n*** SYSTEM INITIALISING ***")
    time.sleep(2)
    logger.write("System initialised")
    time.sleep(2)

    while True:
        show_menu(controller)
        choice = input("Enter command: ")

        if choice == "1":
            time.sleep(0.7)
            controller.command_gear_up()
            time.sleep(1)
        elif choice == "2":
            time.sleep(0.7)
            controller.command_gear_down()
            time.sleep(1)
        elif choice == "3":
            time.sleep(0.7)
            FaultInjector.fault = True
            print("\n[SYSTEM] Fault injected")
            time.sleep(1)
        elif choice == "4":
            time.sleep(0.7)
            controller.view_fault()
            time.sleep(1)
        elif choice == "5":
            time.sleep(0.7)
            FaultInjector.fault = False
            controller = LandingGearController
            main()
        else:
            print("\nInvalid command. Please try again")

main()
