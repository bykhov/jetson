## GPIO 
Example of GPIO usage are [here](https://github.com/NVIDIA/jetson-gpio).
Does not require any additional installation.

Some more explanations are [here](https://automaticaddison.com/how-to-blink-an-led-using-nvidia-jetson-nano/).

## Camera
* Check if it is alive: `ls /dev/video0`
* Another way to check (from [here](https://github.com/jetsonhacks/USB-Camera): 
  ```
  sudo apt install v4l-utils
  v4l2-ctl --list-devices
  v4l2-ctl --all -d /dev/video0
  ```
### Jetcam
The recommended way to use camera is [Jetcam](https://github.com/NVIDIA-AI-IOT/jetcam).
Note to change the camera device to `capture_device=1` in `notebooks/usb_camera/usb_camera.ipynb`:


### OpenCV
* This is supposed to work (adapted from [USB-Camera](https://github.com/jetsonhacks/USB-Camera)):
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
* `cv2.imshow(window_title, frame)` does not work (from full examples from [USB-Camera](https://github.com/jetsonhacks/USB-Camera)).
* [Fix](https://developer.ridgerun.com/wiki/index.php/How_to_Use_NVIDIA_OpenCV_Python_Bindings_on_Jetson_Boards) OpenCV installation (only if you have to!)

