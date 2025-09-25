#__init__

#the '__init__.py' file allows us to make a package
#it will treat the 'humanoid_robot' as a package root
#'humanoid_robot' is now importable, and python will treat it as a module

#code designed to test a humanoid robot
#the design of the processes the humanoid robot completes are based off of -
#the UML diagrams submitted in the System Design submission

#the Class Diagram: core (Sensors, Actuators, Controller, State)
#the State Machine Diagram: RobotState and transitions enforced via regulated state changes
#the Activity Diagram: perceive, decide/plan and then respond with activities and navigation
#the Sequence Diagram: the order and structure of interactions throughout a process

#the '__all__' allows us to make a list of strings that will be used in subpackages
#these subpackages are useful as it helps keep things neat
__all__ = ["core", "activities", "sequences"]
