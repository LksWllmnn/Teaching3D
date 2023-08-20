from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import sys
import json
import numpy as np


ap = argparse.ArgumentParser()
ap.add_argument("-t", "--type", type=str,
	default="DICT_ARUCO_ORIGINAL",
	help="type of ArUCo tag to detect")
args = vars(ap.parse_args())

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

detectgray = True
drawaxes = True

if ARUCO_DICT.get(args["type"], None) is None:
	print("[INFO] ArUCo tag of '{}' is not supported".format(
		args["type"]))
	sys.exit(0)

print("[INFO] detecting '{}' tags...".format(args["type"]))
arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[args["type"]])
arucoParams = cv2.aruco.DetectorParameters_create()

print("[INFO] starting video stream...")
vs = cv2.VideoCapture(0)
time.sleep(2.0)

# with open('camera.json', 'r') as json_file:
# 	camera_data = json.load(json_file)
# dist = np.array(camera_data["dist"])
# mtx = np.array(camera_data["mtx"])

# mtx = np.array([[656.89800288, 0.0, 601.92562476],
#                 [0.0, 691.24719445, 409.2436554],
#                 [0.0, 0.0, 1.0]])

# dist = np.array([[0.15816723, -0.17639408, 0.02540254, -0.02053277, 0.24165205]])
mtx = array1 = np.array([[703.57411461, 0.0, 318.17855849],
                   [0.0, 661.81087171, 234.52481886],
                   [0.0, 0.0, 1.0]])
dist = array2 = np.array([[8.26735188e-01, -9.93087235e+00, 1.88377326e-02, 3.76866546e-03, 3.55690223e+01]])

ret, frame = vs.read()
h, w = frame.shape[:2]

print("Frame Width:", w)
print("Frame Height:", h)

newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 0, (w, h))
mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w, h), cv2.CV_32FC1)
x, y, w1, h1 = roi
yh1 = y + h1
xw1 = x + w1

while True:
	ret, frame = vs.read()
	
	dst1 = cv2.remap(frame, mapx, mapy, cv2.INTER_LINEAR)
	frame = dst1[y:yh1, x:xw1]

	if detectgray:
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		(corners, ids, rejected) = cv2.aruco.detectMarkers(gray, arucoDict, parameters=arucoParams)
	else:
		(corners, ids, rejected) = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams)

	if len(corners) > 0:
		if drawaxes:
			for i in range(0, len(ids)):
				rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.02, mtx, dist)
				cv2.drawFrameAxes(frame, mtx, dist, rvec, tvec, 0.02) 

		ids = ids.flatten()
		cv2.aruco.drawDetectedMarkers(frame, corners, ids)

	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	if key == ord("q"):
		break

cv2.destroyAllWindows()
vs.stop()