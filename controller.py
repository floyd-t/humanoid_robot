#Controller

from __future__ import annotations
#dataclass simplifies class usage and helps generate '__init__' and '__repr__'
from dataclasses import dataclass, field
from typing import Dict, Any, List
#enforces already established states
from .state import RobotState, StateError
#input devices
from .sensors import VisionSensor, IMUSensor
#output devices
from .actuators import Motor, Gripper, ActuatorError

@dataclass
class RobotController:
    #ensures that the starting state is IDLE
    state: RobotState = RobotState.IDLE
    sensors: Dict[str, Any] = field(default_factory=dict)
    actuators: Dict[str, Any] = field(default_factory=dict)
    #list of state transitions for testing/reporting
    log: List[str] = field(default_factory=list)

    #adds the established parts into a list
    def add_default_components(self) -> None:
        self.sensors["vision"] = VisionSensor()
        self.sensors["imu"] = IMUSensor()
        self.actuators["left_leg"] = Motor(name="left_leg")
        self.actuators["right_leg"] = Motor(name="right_leg")
        self.actuators["arm"] = Motor(name="arm")
        self.actuators["gripper"] = Gripper()

    #this ensures that only valid state changes can occur
    #it will log transitions or, if invalid, will raise 'StateError' instead
    def set_state(self, new_state: RobotState) -> None:
        if not self._is_valid_transition(self.state, new_state):
            raise StateError(f"Invalid transition: {self.state.name} -> {new_state.name}")
        self.log.append(f"{self.state.name} -> {new_state.name}")
        self.state = new_state

    @staticmethod
    #defines the rules for which states can be reached through other stages
    #for example, 'READY' can only become 'PERCEIVING' or 'SHUTTING_DOWN'
    def _is_valid_transition(cur: RobotState, nxt: RobotState) -> bool:
        allowed = {
            RobotState.IDLE: {RobotState.INITIALISING, RobotState.SHUTTING_DOWN},
            RobotState.INITIALISING: {RobotState.READY, RobotState.ERROR},
            RobotState.READY: {RobotState.PERCEIVING, RobotState.SHUTTING_DOWN},
            RobotState.PERCEIVING: {RobotState.PLANNING, RobotState.ERROR},
            RobotState.PLANNING: {RobotState.ACTING, RobotState.ERROR},
            RobotState.ACTING: {RobotState.READY, RobotState.ERROR},
            RobotState.ERROR: {RobotState.SHUTTING_DOWN, RobotState.IDLE},
            RobotState.SHUTTING_DOWN: set(),
        }
        return nxt in allowed[cur]

    #moves robot into 'INITIALISING' then 'READY'
    def initialise(self) -> None:
        self.set_state(RobotState.INITIALISING)
        self.set_state(RobotState.READY)

    #moves robot to 'SHUTTING_DOWN'
    def shutdown(self) -> None:
        self.set_state(RobotState.SHUTTING_DOWN)

    #moves robot to 'PERCEIVING', and returns readings
    def perceive(self) -> Dict[str, Any]:
        self.set_state(RobotState.PERCEIVING)
        data = {name: s.read() for name, s in self.sensors.items()}
        return data

    #defines a 'plan' so that the default state is 'idle'
    def plan(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        self.set_state(RobotState.PLANNING)
        plan = {"action": "idle", "target": None}
        objs = perception.get("vision", {}).get("objects", [])
        imu_safe = perception.get("imu", {}).get("is_safe", True)
        #if the IMU is at an unsafe tilt it will attempt to use 'recover_balance'
        if not imu_safe:
            plan = {"action": "recover_balance", "target": None}
        #it will also try to pick up the box as an elif function
        elif "box" in objs:
            plan = {"action": "pick", "target": "box"}
        #if neither, will remain idle
        return plan

    #sets the state to 'ACTING'
    def act(self, plan: Dict[str, Any]) -> str:
        self.set_state(RobotState.ACTING)
        try:
            #recover balance, use legs to stabilise
            if plan["action"] == "recover_balance":
                self.actuators["left_leg"].move_to(0.0, speed=0.2)
                self.actuators["right_leg"].move_to(0.0, speed=0.2)
                result = "rebalanced"
                return result
            #pick box up, moves arms and closes gripper hands
            elif plan["action"] == "pick" and plan["target"] == "box":
                self.actuators["arm"].move_to(1.0, speed=0.5)
                self.actuators["gripper"].close()
                result = "picked:box"
                return result
            #remains idle
            else:
                result = "idle"
                return result
        #if an actuator fails, returns with an 'ERROR' state
        except ActuatorError:
            self.set_state(RobotState.ERROR)
            raise
        #returns to ready if no error
        finally:
            if self.state != RobotState.ERROR:
                self.set_state(RobotState.READY)
