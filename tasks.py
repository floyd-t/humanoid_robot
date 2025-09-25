#Tasks

from __future__ import annotations
from typing import Dict, Any
#brings in the 'RobotController' and 'perceive_plan_act'
from ..core.controller import RobotController
from ..activities.navigation import perceive_plan_act

#this makes the robot try to pick up the box, then place it
def pick_and_place(controller: RobotController) -> Dict[str, Any]:

    #moves the state from IDLE to INITIALISING then READY
    controller.initialise()
    #runs the imported loop, therefore capturing sensor data, decision and action result
    perception, plan, result = perceive_plan_act(controller)
    #if an object is picked up the following occurs
    picked = result.startswith("picked:")
    if picked:
        #it will release the box
        controller.actuators["gripper"].open()
        #it will return its arms to their default position
        controller.actuators["arm"].move_to(0.0, speed=0.5)
        status = "placed"
    else:
        #if nothing detected, it will do nothing
        status = "no_object"
    #once the loop is finished, the machine will move into it's 'SHUTTING_DOWN' state
    controller.shutdown()
    #returns with a summary, including whether an object was grabbed, whether it was placed
    #it will also return with a log of all the state transitions to help with testing
    return {"picked": picked, "status": status, "log": controller.log}
