import cv2
import pyopenpose as op
from imutils import translate, rotate, resize

import openzwave
from openzwave.option import ZWaveOption
from openzwave.network import ZWaveNetwork

# make sure these commands get flushed by doing them first, then loading tensorflow...
# tensorflow should take enough time to start for these commands to flush
options = ZWaveOption('/dev/ttyACM0')
options.lock()

network = ZWaveNetwork(options)

import time
import numpy as np
np.random.seed(1337)

import tensorflow as tf

# make sure tensorflow doesn't take up all the gpu memory
conf = tf.ConfigProto()
conf.gpu_options.allow_growth=True
session = tf.Session(config=conf)

import keras

# Custom Params (refer to include/openpose/flags.hpp for more parameters)
params = dict()
params["model_folder"] = "../../models/"

# built in TX2 video capture source
vs = cv2.VideoCapture("nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)720,format=(string)NV12, framerate=(fraction)24/1 ! nvvidconv flip-method=0 ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")

tposer = keras.models.load_model('dab-tpose-other.h5')

# Starting OpenPose
opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()

datum = op.Datum()
np.set_printoptions(precision=4)

fps_time = 0

DAB = 1
TPOSE = 2
OTHER = 0

LIGHTS = 0

bounced = time.time()
debounce = 3 # wait 3 seconds before allowing another command

while True:
    ret_val, frame = vs.read()

    datum.cvInputData = frame
    opWrapper.emplaceAndPop([datum])

    # need to be able to see what's going on
    image = datum.cvOutputData
    cv2.putText(image,
                "FPS: %f" % (1.0 / (time.time() - fps_time)),
                (10, 20),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (0, 255, 0), 2)
    
    cv2.imshow("Openpose", image)

    if datum.poseKeypoints.any():
        first_input = datum.poseKeypoints
        try:
            first_input[:,:,0] = first_input[:,:,0] / 720
            first_input[:,:,1] = first_input[:,:,1] / 1280
            first_input = first_input[:,:,1:]
            first_input = first_input.reshape(len(datum.poseKeypoints), 50)
        except:
            continue

        output = tposer.predict_classes(first_input)
        for j in output:
            if j == 1:
                print("dab detected")
                if LIGHTS == 0 or (time.time() - bounced) < debounce:
                    continue
                for node in network.nodes:
                    for val in network.nodes[node].get_switches():
                        network.nodes[node].set_switch(val, False)
                LIGHTS = 0
                bounced = time.time()
            elif j == 2:
                print("tpose detected")
                if LIGHTS == 1 or (time.time() - bounced) < debounce:
                    continue
                for node in network.nodes:
                    for val in network.nodes[node].get_switches():
                        network.nodes[node].set_switch(val, True)
                LIGHTS = 1
                bounced = time.time()

    fps_time = time.time()
    
    # quit with a q keypress, b or m to save data
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# clean up after yourself
vs.release()
cv2.destroyAllWindows()

