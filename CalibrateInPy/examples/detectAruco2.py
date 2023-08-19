import cv2
import numpy as np

# ArUco dictionary and parameters
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_100)
aruco_params = cv2.aruco.DetectorParameters_create()

# Start video capture from default camera (camera index 0)
cap = cv2.VideoCapture(0)

mtx = np.array([[656.89800288, 0.0, 601.92562476],
                [0.0, 691.24719445, 409.2436554],
                [0.0, 0.0, 1.0]])

dist = np.array([[0.15816723, -0.17639408, 0.02540254, -0.02053277, 0.24165205]])

while True:
    ret, frame = cap.read()
    
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect ArUco markers
    corners, ids, rejected = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=aruco_params)

    if len(corners) > 0:
        # Draw markers and axes
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, 0.02, mtx, dist)
        # for i in range(len(ids)):
        #     cv2.aruco.drawAxis(frame, mtx, dist, rvecs[i], tvecs[i], 0.02)

    # Display the frame
    cv2.imshow("ArUco Detection", frame)

    # Exit loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()