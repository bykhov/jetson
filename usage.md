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

### OpenCV
* [Fix](https://developer.ridgerun.com/wiki/index.php/How_to_Use_NVIDIA_OpenCV_Python_Bindings_on_Jetson_Boards) OpenCV installation
* `cv2.imshow(window_title, frame)` does not work.
* This is supposed to work (from [here](https://github.com/jetsonhacks/USB-Camera)):
  ```python
  import sys
  import cv2
  import matplotlib.pyplot as plt
    
  window_title = "USB Camera"
    
  # ASSIGN CAMERA ADDRESS HERE
  camera_id = "/dev/video0"
  # Full list of Video Capture APIs (video backends): https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html
  # For webcams, we use V4L2
  video_capture = cv2.VideoCapture(camera_id, cv2.CAP_V4L2)
  ret_val, frame = video_capture.read()
  plt.imshow(frame)
  plt.show()
  video_capture.release()
  ```



