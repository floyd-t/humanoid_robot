#Navigation

from __future__ import annotations
from typing import Tuple, Dict, Any
#'RobotController' adds the states, sensors and actuators defined elsewhere
from ..core.controller import RobotController

#'perceive_plan_act' functions by taking an instance of 'RobotController' and calling functions
#it calls 'perceive()', 'plan()' and 'act()'
#it returns a 'perception'(sensor readings), 'plan'(describes how it intends to function/respond and a 'result'
def perceive_plan_act(controller: RobotController) -> Tuple[Dict[str, Any], Dict[str, Any], str]:

    #calls the 'perceive()' method/function
    perception = controller.perceive()
    #calls the 'plan()' method/function
    plan = controller.plan(perception)
    #calls the 'act()' method/function, and returns a string of the result
    result = controller.act(plan)
    #places the results from 'perceive()', 'plan()' and 'act()' together in a tuple
    return perception, plan, result
