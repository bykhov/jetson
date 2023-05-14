# Face detection example (Tensorflow-based)

## [MT-CNN Model](https://github.com/ipazc/mtcnn)
* Install:
    ```bash
    sudo pip install mtcnn --no-dependencies # open-cv preinstalled, keras supposed to be installed with Tensorflow
    ```
* Code example :
    ```python
    import sys
    import cv2
    import matplotlib.pyplot as plt
    from mtcnn import MTCNN

    detector = MTCNN()
    # %% Validate camera
    window_title = "USB Camera"
    camera_id = "/dev/video0"
    video_capture = cv2.VideoCapture(camera_id, cv2.CAP_V4L2)
    ret_val, frame = video_capture.read()
    if ret_val:
        print("Camera is OK!")
    else:
        print("Camera is NOT OK!")
        sys.exit(1)

    plt.imshow(frame)
    plt.show()

    print(detector.detect_faces(frame))

    # cv2.imshow(window_title, frame) # does not work for remote SSH connection
    video_capture.release()
    ```
    

## Tried and did not work
* [VGGFace](https://github.com/rcmalli/keras-vggface) model is too big to fit in memory.
* OpenCV with preinstalated version ([example](https://towardsdatascience.com/face-detection-in-2-minutes-using-opencv-python-90f89d7c0f81), xml location [fix](https://stackoverflow.com/a/58479622)).

