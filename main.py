#Main

#imports the controller and the pick_and_place sequence
from humanoid_robot.core.controller import RobotController
from humanoid_robot.sequences.tasks import pick_and_place

def main() -> None:
    #creates an object for the 'RobotController' and uses the initial 'IDLE' state
    controller = RobotController()
    #adds the sensors and actuators
    controller.add_default_components()
    #calls the function of 'pick_and_place'
    summary = pick_and_place(controller)
    #prints out a summary dictionary
    #these include the status and a log of transitions between states
    print("SUMMARY:", summary)

#this makes it so if main.py is run it will call 'main()'
#if main is imported from another module, it will not run automatically
if __name__ == "__main__":
    main()
