## GPIO 
Example of GPIO usage are [here](https://github.com/NVIDIA/jetson-gpio).
Does not require any additional installation.

Some more explanations are [here](https://automaticaddison.com/how-to-blink-an-led-using-nvidia-jetson-nano/).

## Camera

### OpenCV
* The recommended way to use camera is (adapted from [USB-Camera](https://github.com/jetsonhacks/USB-Camera)):
  ```python
  import sys
  import cv2
  import matplotlib.pyplot as plt
    
  window_title = "USB Camera"
  camera_id = "/dev/video0"
  video_capture = cv2.VideoCapture(camera_id, cv2.CAP_V4L2)
  ret_val, frame = video_capture.read()
  plt.imshow(frame)
  plt.show()
  video_capture.release()
  ```
* `cv2.imshow(window_title, frame)` does not work **remotely**  (from full examples from [USB-Camera](https://github.com/jetsonhacks/USB-Camera)).
* [Fix](https://developer.ridgerun.com/wiki/index.php/How_to_Use_NVIDIA_OpenCV_Python_Bindings_on_Jetson_Boards) OpenCV installation (only if you have to!)

### Jetcam
This is supposed to work [Jetcam](https://github.com/NVIDIA-AI-IOT/jetcam). However, I found camera resource release too challenging.
1. Install [Jetcam](https://github.com/NVIDIA-AI-IOT/jetcam) following `Setup`.
2. Use [example](https://github.com/NVIDIA-AI-IOT/jetcam/blob/master/notebooks/usb_camera/usb_camera.ipynb). 
Note to change the camera device to `capture_device=0`




