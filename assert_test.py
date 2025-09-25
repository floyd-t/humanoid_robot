#Assert Test
#using python's inbuilt assert statement to test the key behaviours of the robot

from humanoid_robot.core.controller import RobotController
from humanoid_robot.core.state import RobotState, StateError

def test_state_transitions() -> None:
    c = RobotController()
    c.add_default_components()
    #verifies the lifecycle transitions
    assert c.state == RobotState.IDLE
    c.initialise()
    assert c.state == RobotState.READY
    c.shutdown()
    assert c.state == RobotState.SHUTTING_DOWN

def test_invalid_transition_raises() -> None:
    #confirms that an incorrect transition will raise an error
    c = RobotController()
    try:
        c.set_state(RobotState.ACTING)
        raised = False
    except StateError:
        raised = True
    assert raised is True

def test_activity_loop_returns_ready() -> None:
    #runs a full 'perceive, plan, act' cycle and confirms that the robot will return to 'READY' after
    c = RobotController()
    c.add_default_components()
    c.initialise()

    #also confirms the outcome result is a string
    perception = c.perceive()
    plan = c.plan(perception)
    result = c.act(plan)
    assert c.state == RobotState.READY
    assert isinstance(result, str)

#lets the tester run the test directly with: python -m tests.assert_tests
if __name__ == "__main__":
    test_state_transitions()
    test_invalid_transition_raises()
    test_activity_loop_returns_ready()
    print("All assert tests passed.")
