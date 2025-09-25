#Actuators

from __future__ import annotations
from dataclasses import dataclass

#the 'Exception' is for when the robot is asked to do something that it physically cannot
class ActuatorError(Exception):
    pass

#represents an actuator (arm/leg joint)
#there will be a specific string name and max speed, the position is simulated
@dataclass
class Motor:
    name: str
    max_speed: float = 1.0
    position: float = 0.0

    #'move_to()' allows for the movement of the motor and checks if the speed is invalid
    #if valid, it will update with the new position
    #if invalid, it will raise an 'ActuatorError' instead
    def move_to(self, position: float, speed: float = 0.5) -> float:
        if speed < 0 or speed > self.max_speed:
            raise ActuatorError(f"Speed {speed} out of range for {self.name}")
        self.position = position
        return self.position

#models a 'gripper' so that the hand can be open or closed with Boolean values
#using binary for its hand/gripper allows for a simplified model
@dataclass
class Gripper:

    name: str = "gripper"
    closed: bool = False

    def close(self) -> bool:
        self.closed = True
        return self.closed

    def open(self) -> bool:
        self.closed = False
        return self.closed
