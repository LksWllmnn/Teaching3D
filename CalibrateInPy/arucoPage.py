import argparse
import cv2
import sys
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=True, help="path to output image containing ArUCo tag")
ap.add_argument("-i", "--id", type=int, required=True, help="ID of first ArUCo tag to generate")
ap.add_argument("-t", "--type", type=str, default="DICT_ARUCO_ORIGINAL", help="type of ArUCo tag to generate")
ap.add_argument("-d", "--dpi", type=str, default="72", help="the DPI of the output print")
ap.add_argument("-s", "--size", type=int, default=50, help="the size in mm of the ArUco tag")
ap.add_argument("-m", "--margin", type=int, default=5, help="the size in mm of the margins between the ArUco tags")
ap.add_argument("-x", "--x", type=int, default=3, help="number of ArUco tags in the X direction")
ap.add_argument("-y", "--y", type=int, default=4, help="number of ArUco tags in the Y direction")
ap.add_argument("--write-id", default=True, action=argparse.BooleanOptionalAction, help="write the id of the tag or not")
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

if ARUCO_DICT.get(args["type"], None) is None:
	print("[INFO] ArUCo tag of '{}' is not supported".format(args["type"]))
	sys.exit(0)

#arucoDict = cv2.aruco.Dictionary(ARUCO_DICT[args["type"]], 50)
arucoDict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT[args["type"]])
tag_type = args["type"]

A4_width = 210
A4_height = 297

x = args["x"]
y = args["y"]
size = args["size"]
margin = args["margin"]
text_size = 8

write_id = args["write_id"]


if not(write_id):
	text_size = 0


if x < 1 or y < 1:
	print(f"[INFO] Please make sure that the grid contains at least one tag - i.e. (x > 0) and (y > 0). Currently, x = {x} and y = {y}.")
	sys.exit(0)


rest_x = A4_width - (x * size + (x - 1) * margin)
rest_y = A4_height - (y * size + y * text_size + (y - 1) * margin)


stop = False

if rest_x < 0:
	print(f"[INFO] Please ensure that the grid fits on the page. Consider reducing the number of tags in the x-direction. Currently, x = {x}.")
	stop = True

if rest_y < 0:
	print(f"[INFO] Please ensure that the grid fits on the page. Consider reducing the number of tags in the y-direction. Currently, y = {y}.")
	stop = True

if stop:
	sys.exit(0)


half_rest_x = int(np.floor(rest_x/2))
half_rest_y = int(np.floor(rest_y/2))

A4_DICT = {
	"72": (595, 842),
	"96": (794, 1123)
}


if A4_DICT.get(args["dpi"], None) is None:
	print("[INFO] A4 print of {} DPI is not supported. Please try one of the following: 72, 96.".format(args["dpi"]))
	sys.exit(0)
	
dpi = A4_DICT[args["dpi"]]
	
page = np.ones((dpi[1],dpi[0],3), dtype="uint8")*255

multiplier = np.min([dpi[0]/A4_width, dpi[1]/A4_height])


size_m = int(np.floor(size * multiplier))
text_size_m = int(np.floor(text_size * multiplier))
margin_m = int(np.floor(margin * multiplier))
half_rest_x_m = int(np.floor(half_rest_x * multiplier))
half_rest_y_m = int(np.floor(half_rest_y * multiplier))

tag_id = args["id"]

print(f"[INFO] creating {x*y} tags from the {tag_type} dictionary. Starting with id:{tag_id}")
for i in range(0, y):
	for j in range(0, x):
		img = np.ones((size_m,size_m,3), dtype="uint8")*255
		i_val = half_rest_y_m + i*size_m + i*margin_m + 2*i*text_size_m
		j_val = half_rest_x_m + j*size_m + j*margin_m
		tag = np.zeros((size_m, size_m, 1), dtype="uint8")
		cv2.aruco.generateImageMarker(arucoDict, tag_id, size_m, tag, 1)
		if write_id:
			if "APRILTAG" in tag_type:
				text_string = f"April id: {tag_id}"
			else:
				text_string = f"ArUco id: {tag_id}"
			cv2.putText(page, text_string, (j_val, i_val-margin_m), 
						fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.6, color=(0, 0, 0))
		page[i_val:i_val+size_m, j_val:j_val+size_m] = tag
		tag_id += 1

cv2.imwrite(args["output"], page)
cv2.imshow("ArUCo Tags Page", page)
cv2.waitKey(0)