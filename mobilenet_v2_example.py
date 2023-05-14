import numpy as np
import pandas as pd
import cv2
# import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import time
import Jetson.GPIO as GPIO

import os
os.environ['TFHUB_DOWNLOAD_PROGRESS'] = "1" # https://github.com/tensorflow/hub/issues/283

# %% Validate camera
def init_camera(camera_id="/dev/video0"):
    """Initialize the camera and return the video_capture object."""
    video_capture = cv2.VideoCapture(camera_id, cv2.CAP_V4L2)
    print("Camera is OK!")
    return video_capture


def stop_camera(video_capture):
    """Stop the camera."""
    video_capture.release()
    print("Camera is stopped!")


def read_image(video_capture):
    """Read a frame from the camera and return it as a numpy array."""
    ret_val, frame = video_capture.read()
    if ret_val:
        print("Frame read.")
        return frame
    else:
        raise Exception("Camera is NOT OK!")


def init_detector():
    """Initialize the detector network and
    return the detector and the corresponding classes."""
    labelmap_url = "https://raw.githubusercontent.com/google-coral/test_data/master/coco_labels.txt"
    classes = pd.read_csv(labelmap_url, header=None)
    print("Classes ready!")
    # https://tfhub.dev/tensorflow/ssd_mobilenet_v2/fpnlite_320x320/1
    detector = hub.load("https://tfhub.dev/tensorflow/ssd_mobilenet_v2/fpnlite_320x320/1")
    print("Detector ready!")
    return detector, classes


def find_person(detector_output, classes):
    """Check if a person is found in the detector output."""
    result = {key: value.numpy() for key, value in detector_output.items()}
    idx = result['detection_classes'][0,:]-1 == 0
    prob = result['detection_scores'][0, idx]
    if prob.max() > 0.5:    # 50% probability or more
        print("Person found!")
        return True
    else:
        print("Person NOT found!")
        return False


# %% Download and set up the model
detector, classes = init_detector()

# %% First run takes longer to initialize the network
video_capture = init_camera()
frame = read_image(video_capture)
image = np.expand_dims(frame, 0)
# plt.imshow(frame)
detector_output = detector(image)

# %% GPIO setup
led_pin_red  = 7
led_pin_green = 29
GPIO.setmode(GPIO.BOARD)
GPIO.setup(led_pin_red, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(led_pin_green, GPIO.OUT, initial=GPIO.LOW)

# %% Detection loop


tic = time.time()
num_loops = 100

for _ in range(num_loops):
    frame = read_image(video_capture)
    # The model expects an input of (None, width, height, 3).
    image = np.expand_dims(frame, 0)
    # plt.imshow(frame)
    detector_output = detector(image)
    if find_person(detector_output, classes):
        GPIO.output(led_pin_green, GPIO.LOW)
        GPIO.output(led_pin_red, GPIO.HIGH)
    else:
        GPIO.output(led_pin_red, GPIO.LOW)
        GPIO.output(led_pin_green, GPIO.HIGH)


toc = time.time() # Time of completion
print("FPS: ", num_loops/(toc-tic))

# %%
stop_camera(video_capture) # Stop the camera
