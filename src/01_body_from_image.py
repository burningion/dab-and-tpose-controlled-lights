import cv2
import pyopenpose as op
from imutils import translate, rotate, resize

import time
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
np.set_printoptions(precision=4)

dabs = []
tposes = []
other = []

fps_time = 0

while True:
    ret_val, frame = vs.read()

    datum.cvInputData = frame
    opWrapper.emplaceAndPop([datum])

    # need to be able to see what's going on
    image = datum.cvOutputData
    cv2.putText(image,
                "FPS: %f" % (1.0 / (time.time() - fps_time)),
                (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (0, 255, 0), 2)
    
    cv2.imshow("Openpose", image)
    fps_time = time.time()
    
    # quit with a q keypress, b or m to save data
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif key == ord("b"):
        print("Dab: " + str(datum.poseKeypoints))
        dabs.append(datum.poseKeypoints[0])
    elif key == ord("m"):
        print("TPose: " + str(datum.poseKeypoints))
        tposes.append(datum.poseKeypoints[0])
    elif key == ord("/"):
        print("Other: " + str(datum.poseKeypoints))
        other.append(datum.poseKeypoints[0])

# write our data as numpy binary files
# for analysis later

dabs = np.asarray(dabs)
tposes = np.asarray(tposes)
other = np.asarray(other)

np.save('dabs.npy', dabs)
np.save('tposes.npy', tposes)
np.save('other.npy', other)

# clean up after yourself
vs.release()
cv2.destroyAllWindows()

