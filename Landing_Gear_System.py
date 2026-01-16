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

class LandingGearController:

    # Timing requirements from PER-02 and PER-03
    GEAR_DOWN_TIME = 5 # seconds
    GEAR_UP_TIME = 7 # seconds

    def __init__(self):
        self.state = GearState.DOWN_LOCKED

    # Log function with timestamp
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [{self.state.name}] {message}")
        time.sleep(2) # time delay to improve readability

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
                self.log("*** ROOT CAUSE: Low hydraulic pressure - primary pump")
                self.log("*** Activating backup hydraulic pump ***")
                time.sleep(FaultInjector.fault_delay)
                self.log("*** Backup operation complete - hydraulic maintenance required ***")
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
                self.log("*** ROOT CAUSE: Low hydraulic pressure - primary pump")
                self.log("*** FAILSAFE: Gear retraction aborted ***")
                self.state = GearState.DOWN_LOCKED
                self.log("*** Gear remains DOWN in failsafe mode ***")
                self.log("*** WARNING: Low hydraulic pressure remains - maintenance required ***")
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
    controller = LandingGearController()

    time.sleep(1)
    print("\n*** SYSTEM INITIALISING ***")
    time.sleep(2)
    print("Landing gear system initialised")
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