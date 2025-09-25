#State

#Enum defines named values, auto assigns values to states so for example 1 = READY
from enum import Enum, auto

#These are the states named in the State Transition Diagram
class RobotState(Enum):

    #Each state reflects a certain status that the robot can potentially be in
    IDLE = auto()
    INITIALISING = auto()
    READY = auto()
    PERCEIVING = auto()
    PLANNING = auto()
    ACTING = auto()
    ERROR = auto()
    SHUTTING_DOWN = auto()

#This prevents incorrect movement between states by creating an error type
#valid state transitions help ensure that the robot is predictable
class StateError(Exception):

    pass
