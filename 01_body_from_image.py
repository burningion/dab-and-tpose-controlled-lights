import cv2
import pyopenpose as op
from imutils import translate, rotate, resize

import numpy as np

# Custom Params (refer to include/openpose/flags.hpp for more parameters)
params = dict()
params["model_folder"] = "../../models/"

vs = cv2.VideoCapture("nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)720,format=(string)NV12, framerate=(fraction)24/1 ! nvvidconv flip-method=0 ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")

# Starting OpenPose
opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()

datum = op.Datum()

while True:
    ret_val, frame = vs.read()

    datum.cvInputData = frame
    opWrapper.emplaceAndPop([datum])
    # print("Body keypoints: \n" + str(datum.poseKeypoints))
    cv2.imshow("Openpose", datum.cvOutputData)

    # quit with a q keypress
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()
vs.stop()
