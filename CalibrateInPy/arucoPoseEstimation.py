#script from here: https://github.com/niconielsen32/ComputerVision/blob/master/ArUco/arucoPoseEstimation.py 20.08.23
#some parts are edited from lw

import numpy as np
import cv2
import sys
import time
import socket

server_ip = "127.0.0.1"  # Replace with the C# server's IP address
server_port = 12345  # Replace with the C# server's port


ARUCO_DICT = {
	"DICT_4X4_50": cv2.aruco.DICT_4X4_50,
	"DICT_4X4_100": cv2.aruco.DICT_4X4_100,
	"DICT_4X4_250": cv2.aruco.DICT_4X4_250,
	"DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
	"DICT_5X5_50": cv2.aruco.DICT_5X5_50,
	"DICT_5X5_100": cv2.aruco.DICT_5X5_100,
	"DICT_5X5_250": cv2.aruco.DICT_5X5_250,
	"DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
	"DICT_6X6_50": cv2.aruco.DICT_6X6_50,
	"DICT_6X6_100": cv2.aruco.DICT_6X6_100,
	"DICT_6X6_250": cv2.aruco.DICT_6X6_250,
	"DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
	"DICT_7X7_50": cv2.aruco.DICT_7X7_50,
	"DICT_7X7_100": cv2.aruco.DICT_7X7_100,
	"DICT_7X7_250": cv2.aruco.DICT_7X7_250,
	"DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
	"DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
	"DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
	"DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
	"DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
	"DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}

def pose_estimation(frame, aruco_dict_type, matrix_coefficients, distortion_coefficients, camIndex):
    global everyArucoCaptured0
    global everyArucoCaptured1

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.aruco_dict = cv2.aruco.Dictionary_get(aruco_dict_type)
    parameters = cv2.aruco.DetectorParameters_create()

    corners, ids, rejected_img_points = cv2.aruco.detectMarkers(gray, cv2.aruco_dict,parameters=parameters,
        cameraMatrix=matrix_coefficients,
        distCoeff=distortion_coefficients) 
    
    

    rvecAll = []
    tvecAll = []

    if len(corners) > 0:
        if(len(ids) == 12): 
            if(camIndex == 0): everyArucoCaptured0 = True
            if(camIndex == 1): everyArucoCaptured1 = True
        else:
            if(camIndex == 0): everyArucoCaptured0 = False
            if(camIndex == 1): everyArucoCaptured1 = False


        for i in range(0, len(ids)):
            rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.02, matrix_coefficients, distortion_coefficients)
            cv2.aruco.drawDetectedMarkers(frame, corners)
            cv2.aruco.drawAxis(frame, matrix_coefficients, distortion_coefficients, rvec, tvec, 0.01)
            rvecAll.append(rvec)
            tvecAll.append(tvec)  

    return frame, rvecAll, tvecAll

def compute_relation(rVecAll, tVecAll, rVecAll1, tVecAll1):
    relative_rotations = []
    relative_translations = []
    
    for i in range(len(rVecAll)):
               
        relative_rotation = rVecAll[i] * (1 / rVecAll1[i])
        relative_translation = tVecAll1[i] - tVecAll[i]
        
        relative_rotations.append(relative_rotation)
        relative_translations.append(relative_translation)

    # Calculate the average relative rotation and translation
    sum_relative_rotation = sum(relative_rotations)
    sum_relative_translation = sum(relative_translations)
    
    average_relative_rotation = sum_relative_rotation / len(relative_rotations)
    average_relative_translation = sum_relative_translation / len(relative_translations)
    
    return average_relative_rotation, average_relative_translation

aruco_type = "DICT_5X5_50"
arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[aruco_type])
arucoParams = cv2.aruco.DetectorParameters_create()
intrinsic_camera = np.array(((703.57411461, 0.0, 318.17855849),(0.0, 661.81087171, 234.52481886),(0,0,1)))
distortion = np.array((-0.43948,0.18514,0,0))

everyArucoCaptured0 = False
everyArucoCaptured1 = False


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

cap1 = cv2.VideoCapture(2)
cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while cap.isOpened():
    ret, img = cap.read()
    ret1, img1 = cap1.read()
    frame, rVecAll, tVecAll = pose_estimation(img, ARUCO_DICT[aruco_type], intrinsic_camera, distortion, 0)
    frame1, rVecAll1, tVecAll1 = pose_estimation(img1, ARUCO_DICT[aruco_type], intrinsic_camera, distortion, 1)
    combined_frame = np.vstack((frame, frame1))
    new_height = combined_frame.shape[0] // 2
    new_width = combined_frame.shape[1] // 2
    combined_frame_resized = cv2.resize(combined_frame, (new_width, new_height))
    
    cv2.imshow('Estimated Pose', combined_frame_resized)
    if(everyArucoCaptured0 & everyArucoCaptured1):
        arr, art = compute_relation(rVecAll, tVecAll, rVecAll1, tVecAll1)
        print("Average Relative Rotation:")
        print(arr)

        print("Average Relative Translation:")
        print(art)
        arr_str = np.array2string(arr, separator=',')
        art_str = np.array2string(art, separator=',')

        data_to_send = f"{arr_str}||{art_str}"

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((server_ip, server_port))
            client_socket.send(data_to_send.encode())

        break

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cap1.release()
cv2.destroyAllWindows()