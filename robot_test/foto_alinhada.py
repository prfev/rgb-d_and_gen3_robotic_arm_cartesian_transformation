import pyrealsense2 as rs
import numpy as np
import time
from segment_buttons_terminal import segment_buttons_from_terminal
from kortex_api.autogen.client_stubs.BaseClientRpc import BaseClient
from kortex_api.autogen.client_stubs.BaseCyclicClientRpc import BaseCyclicClient
from kortex_api.autogen.messages import Base_pb2, BaseCyclic_pb2, Common_pb2
import device_connection
import segment_targets
import cv2

def find_y_target_1(base, base_cyclic):
    action = Base_pb2.Action()
    action.name = "Example Cartesian action movement"
    action.application_data = ""

    feedback = base_cyclic.RefreshFeedback()

    cartesian_pose = action.reach_pose.target_pose
    cartesian_pose.x = feedback.base.tool_pose_x - 0.008 # (meters)
    cartesian_pose.y = feedback.base.tool_pose_y  # (meters)
    cartesian_pose.z = feedback.base.tool_pose_z  # (meters)
    cartesian_pose.theta_x = feedback.base.tool_pose_theta_x  # (degrees)
    cartesian_pose.theta_y = feedback.base.tool_pose_theta_y  # (degrees)
    cartesian_pose.theta_z = feedback.base.tool_pose_theta_z  # (degrees)

    base.ExecuteAction(action)
    time.sleep(1)
def find_x_target_1(base, base_cyclic):
    action = Base_pb2.Action()
    action.name = "Example Cartesian action movement"
    action.application_data = ""

    feedback = base_cyclic.RefreshFeedback()

    cartesian_pose = action.reach_pose.target_pose
    cartesian_pose.x = feedback.base.tool_pose_x  # (meters)
    cartesian_pose.y = feedback.base.tool_pose_y + 0.008 # (meters)
    cartesian_pose.z = feedback.base.tool_pose_z  # (meters)
    cartesian_pose.theta_x = feedback.base.tool_pose_theta_x  # (degrees)
    cartesian_pose.theta_y = feedback.base.tool_pose_theta_y  # (degrees)
    cartesian_pose.theta_z = feedback.base.tool_pose_theta_z  # (degrees)

    base.ExecuteAction(action)
    time.sleep(1)
def find_z_target(base, base_cyclic):
    action = Base_pb2.Action()
    action.name = "Example Cartesian action movement"
    action.application_data = ""

    feedback = base_cyclic.RefreshFeedback()
    torque = feedback.actuators[5].torque #NO ATUADOR
    t_e_w_f_x = float(round(feedback.base.tool_external_wrench_force_x, 2))
    t_e_w_f_y = float(round(feedback.base.tool_external_wrench_force_y, 2))
    t_e_w_f_z = float(round(feedback.base.tool_external_wrench_force_z, 2))

    cartesian_pose = action.reach_pose.target_pose
    cartesian_pose.x = feedback.base.tool_pose_x  # (meters)
    cartesian_pose.y = feedback.base.tool_pose_y # (meters)
    cartesian_pose.z = feedback.base.tool_pose_z - 0.001  # (meters)
    cartesian_pose.theta_x = feedback.base.tool_pose_theta_x + 1 # (degrees)
    cartesian_pose.theta_y = feedback.base.tool_pose_theta_y   # (degrees)
    cartesian_pose.theta_z = feedback.base.tool_pose_theta_z  # (degrees)

    base.ExecuteAction(action)
    return t_e_w_f_z
    time.sleep(1)
router = device_connection.DeviceConnection('172.22.70.97', 10000, credentials=('admin', 'admin')) #172.22.66.92
router = router.connect()
base = BaseClient(router)
base_cyclic = BaseCyclicClient(router)

try:
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 30)
    pipeline.start(config)
    align_to = rs.stream.color
    align = rs.align(align_to)
except:
    pass
#Esta função pega um novo conjunto de quadros disponível em um dispositivo
force_z = -999.0
while True:
    frames = pipeline.wait_for_frames()

    #alinha o quadro de cores ao quadro de profundidade
    aligned_frames =  align.process(frames)
    aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
    color_frame = aligned_frames.get_color_frame()

    #confere se a camera ta abrindo so dois canais.
    if not aligned_depth_frame or not color_frame: continue

    #transforma os np arrays em "imagens"
    color_intrin = color_frame.profile.as_video_stream_profile().intrinsics
    depth_image = np.asanyarray(aligned_depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())

    # adiciona o mapa de cor dentro da camada de profundidade e depois junta a imagem rgb e a do amap de cor em uma unica imagem
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
    images = np.hstack((color_image, depth_colormap))

    # centroide = segment_targets.find_target_centroide(color_image)
    
    cv2.imwrite(r'C:\Users\prfev\Desktop\TCC_Scripts\tcc_finals\data\frame_camera.jpg', color_image)
    
    # try:
    #     color_image = cv2.circle(color_image, (centroide[0],centroide[1]), 1, (255, 255, 255), 10)
    #     print(centroide[0])
    # #     if centroide[0] < 470:
    # #         find_x_target_1(base, base_cyclic)
    # except:
    #     pass
    
    # centroides = segment_buttons_from_terminal(color_image)
    
    # if force_z < 4.50:
    #     force_z = find_z_target(base, base_cyclic)
    #     print(force_z)
    # try:
    #     color_image = cv2.circle(color_image, centroides[6], 1, (255, 255, 255), 10)
    #     target = centroides[0][0]
    #     if centroides[0][0] < 530:
    #         find_x_target_1(base, base_cyclic)
    #     print(target)
    # except:
    #     pass
    # if centroides[0][1] > 240:
    #     find_y_target_1(base, base_cyclic)
    

    cv2.namedWindow('Align Example', cv2.WINDOW_NORMAL)
    cv2.imshow('Align Example', color_image)
    key = cv2.waitKey(1)
    # Press esc or 'q' to close the image window

    if key & 0xFF == ord('q') or key == 27:
        cv2.imwrite("foto.jpg",color_image)
        cv2.destroyAllWindows()
        break