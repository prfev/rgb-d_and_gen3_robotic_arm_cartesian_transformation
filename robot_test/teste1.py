
import sys
import os
import time
import threading

from kortex_api.autogen.client_stubs.BaseClientRpc import BaseClient
from kortex_api.autogen.client_stubs.BaseCyclicClientRpc import BaseCyclicClient

from kortex_api.autogen.messages import Base_pb2, BaseCyclic_pb2, Common_pb2

# Maximum allowed waiting time during actions (in seconds)
TIMEOUT_DURATION = 20

# Create closure to set an event after an END or an ABORT
def check_for_end_or_abort(e):
    """Return a closure checking for END or ABORT notifications
    Arguments:
    e -- event to signal when the action is completed
        (will be set when an END or ABORT occurs)
    """
    def check(notification, e = e):
        print("EVENT : " + \
              Base_pb2.ActionEvent.Name(notification.action_event))
        if notification.action_event == Base_pb2.ACTION_END \
        or notification.action_event == Base_pb2.ACTION_ABORT:
            e.set()
    return check
 
def example_move_to_home_position(base):
    # Make sure the arm is in Single Level Servoing mode
    base_servo_mode = Base_pb2.ServoingModeInformation()
    base_servo_mode.servoing_mode = Base_pb2.SINGLE_LEVEL_SERVOING
    base.SetServoingMode(base_servo_mode)
    
    # Move arm to ready position
    print("Moving the arm to a safe position")
    action_type = Base_pb2.RequestedActionType()
    action_type.action_type = Base_pb2.REACH_JOINT_ANGLES
    action_list = base.ReadAllActions(action_type)
    action_handle = None
    for action in action_list.action_list:
        if action.name == "Home":
            action_handle = action.handle

    if action_handle == None:
        print("Can't reach safe position. Exiting")
        return False

    e = threading.Event()
    notification_handle = base.OnNotificationActionTopic(
        check_for_end_or_abort(e),
        Base_pb2.NotificationOptions()
    )

    base.ExecuteActionFromReference(action_handle)
    finished = e.wait(TIMEOUT_DURATION)
    base.Unsubscribe(notification_handle)

    if finished:
        print("Safe position reached")
    else:
        print("Timeout on action notification wait")
    return finished

def find_y_target_1(base, base_cyclic):
    action = Base_pb2.Action()
    action.name = "Example Cartesian action movement"
    action.application_data = ""

    feedback = base_cyclic.RefreshFeedback()

    cartesian_pose = action.reach_pose.target_pose
    cartesian_pose.x = feedback.base.tool_pose_x  # (meters)
    cartesian_pose.y = feedback.base.tool_pose_y - 0.01 # (meters)
    cartesian_pose.z = feedback.base.tool_pose_z  # (meters)
    cartesian_pose.theta_x = feedback.base.tool_pose_theta_x  # (degrees)
    cartesian_pose.theta_y = feedback.base.tool_pose_theta_y  # (degrees)
    cartesian_pose.theta_z = feedback.base.tool_pose_theta_z  # (degrees)

    e = threading.Event()
    notification_handle = base.OnNotificationActionTopic(
        check_for_end_or_abort(e),
        Base_pb2.NotificationOptions()
    )

    base.ExecuteAction(action)
    time.sleep(1)

    finished = e.wait(TIMEOUT_DURATION)
    base.Unsubscribe(notification_handle)

    if finished:
        print("Cartesian movement completed")
    else:
        print("Timeout on action notification wait")
    return finished

def example_angular_action_movement(base):
    
    print("Starting angular action movement ...")
    action = Base_pb2.Action()
    action.name = "Example angular action movement"
    action.application_data = ""

    actuator_count = base.GetActuatorCount()

    # Place arm straight up
    for joint_id in range(actuator_count.count):
        joint_angle = action.reach_joint_angles.joint_angles.joint_angles.add()
        joint_angle.joint_identifier = joint_id
        joint_angle.value = 0

    e = threading.Event()
    notification_handle = base.OnNotificationActionTopic(
        check_for_end_or_abort(e),
        Base_pb2.NotificationOptions()
    )
    
    print("Executing action")
    base.ExecuteAction(action)

    print("Waiting for movement to finish ...")
    finished = e.wait(TIMEOUT_DURATION)
    base.Unsubscribe(notification_handle)

    if finished:
        print("Angular movement completed")
    else:
        print("Timeout on action notification wait")
    return finished

def wrench_mode_test():
    wrench = Base_pb2.WrenchMode()

def example_cartesian_action_movement(base, base_cyclic, cart):
    
    print("Starting Cartesian action movement ...")
    action = Base_pb2.Action()
    action.name = "Example Cartesian action movement"
    action.application_data = ""

    feedback = base_cyclic.RefreshFeedback()
    torque = feedback.actuators[5].torque #NO ATUADOR
    t_e_w_f_x = float(round(feedback.base.tool_external_wrench_force_x, 2))
    t_e_w_f_y = float(round(feedback.base.tool_external_wrench_force_y, 2))
    t_e_w_f_z = float(round(feedback.base.tool_external_wrench_force_z, 2))
    t_e_w_t_x = float(round(feedback.base.tool_external_wrench_torque_x, 2))
    t_e_w_t_y = float(round(feedback.base.tool_external_wrench_torque_y, 2))
    t_e_w_t_z = float(round(feedback.base.tool_external_wrench_torque_z, 2))
    """print(t_e_w_f_x)
    print(t_e_w_f_y)
    print(t_e_w_f_z)
    print(t_e_w_t_x)
    print(t_e_w_t_y)
    print(t_e_w_t_z)"""
    interconnect = feedback.interconnect.gripper_feedback
    # print(interconnect)

    cartesian_pose = action.reach_pose.target_pose
    cartesian_pose.x = feedback.base.tool_pose_x  # (meters)
    cartesian_pose.y = feedback.base.tool_pose_y + 0.001  # (meters)
    cartesian_pose.z = feedback.base.tool_pose_z  # (meters)
    cartesian_pose.theta_x = feedback.base.tool_pose_theta_x  # (degrees)
    cartesian_pose.theta_y = feedback.base.tool_pose_theta_y  # (degrees)
    cartesian_pose.theta_z = feedback.base.tool_pose_theta_z  # (degrees)

    e = threading.Event()
    notification_handle = base.OnNotificationActionTopic(
        check_for_end_or_abort(e),
        Base_pb2.NotificationOptions()
    )

    print("Executing action")
    base.ExecuteAction(action)

    print("Waiting for movement to finish ...")
    finished = e.wait(TIMEOUT_DURATION)
    base.Unsubscribe(notification_handle)

    if finished:

        print("Cartesian movement completed")
    else:
        print("Timeout on action notification wait")
    return finished

def abluble():
    
    # Import the utilities helper module
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    import utilities

    # Parse arguments
    args = utilities.parseConnectionArguments()
    
    # Create connection to the device and get the router
    a = 0
    with utilities.DeviceConnection.createTcpConnection(args) as router:

        # Create required services
        base = BaseClient(router)
        base_cyclic = BaseCyclicClient(router)

        # Example core
        success = True


        # aux = calcular.mapeamento()
        bt = []

        # for i, j  in enumerate(aux):
        #     bt.append(j)

        dicio = {}
        dicio["pivor"] = [0.461,-0.106, 0.086, 174.335, 2.322, 89.27]
        dicio["ver"] = [0.37, -0.131, 0.244,174.294, 2.298, 89.297]

        """dicio["conf"] = [0.418, -0.136, 0.0519, 174.271, 2.388, 89.259]
        dicio["1"] = [0.483, -0.085, 0.054, 174.271, 2.388, 89.259]
        dicio["3"] = [0.483, -0.130, 0.054, 174.271, 2.388, 89.259]
        dicio["cor"] = [0.418, -0.079,0.0519, 174.271, 2.388, 89.259]
        dicio["0"] = [0.418, -0.109, 0.052, 174.271, 2.388, 89.259]
        dicio["2"] = [0.483, -0.109, 0.054, 174.271, 2.388, 89.259]
        dicio["4"] = [0.462, -0.085, 0.053, 174.271, 2.388, 89.259]
        dicio["5"] = [0.462, -0.109, 0.053, 174.271, 2.388, 89.259]
        dicio["6"] = [0.462, -0.130, 0.053, 174.271, 2.388, 89.259]
        dicio["7"] = [0.438, -0.085, 0.054, 174.271, 2.388, 89.259]
        dicio["8"] = [0.438, -0.109, 0.054, 174.271, 2.388, 89.259]
        dicio["9"] = [0.438, -0.130, 0.054, 174.271, 2.388, 89.259]"""

        
        # success &= example_move_to_home_position(base)
        # success &= example_cartesian_action_movement(base, base_cyclic,dicio["ver"])

        success &= find_y_target_1(base, base_cyclic)
        # success &= example_cartesian_action_movement(base, base_cyclic,dicio["pivor"])
        
        # for i in bt:
        #     success &= example_cartesian_action_movement(base, base_cyclic,dicio[i])
        #     success &= example_cartesian_action_movement(base, base_cyclic,dicio["pivor"]) 
        
        # success &= example_cartesian_action_movement(base, base_cyclic,dicio["conf"])
        # success &= example_cartesian_action_movement(base, base_cyclic,dicio["pivor"]) 

        # success &= example_cartesian_action_movement(base, base_cyclic,dicio["ver"])       
        # success &= example_move_to_home_position(base)
        # success &= example_angular_action_movement(base)

        # You can also refer to the 110-Waypoints examples if you want to execute
        # a trajectory defined by a series of waypoints in joint space or in Cartesian space
        # a+=1
        # print(a)
        # time.sleep(20)
        
        