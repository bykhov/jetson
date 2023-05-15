# Person-presence example
The source [code](mobilenet_v2_example.py).

## Goal
* Inference pre-trained object-detection network and process its output
* Remote SSL access (headless)
* Light red or green LED according to a detection result.

## Network
SSD Mobilenet V2 Object detection model with FPN-lite feature extractor, shared box predictor and focal loss, trained on COCO 2017 dataset with training images scaled to 320x320 [model](https://tfhub.dev/tensorflow/ssd_mobilenet_v2/fpnlite_320x320/1) from [Tensor-Hub](https://www.tensorflow.org/hub)

* Sufficiently small with good performance
* One-line download
* One-line inference

## Performance Notes
* Very slow initialization: it takes about 5 minutes to download (~20M) and set up the network
* Inference frame rate is about 3 fps

## Blinking LEDs
The electrical scheme follows [demo](https://automaticaddison.com/how-to-blink-an-led-using-nvidia-jetson-nano/#:~:text=In%20order%20to%20get%20the,7%20on%20the%20Jetson%20Nano.) with two LEDs lighting interchangeably for presence or non-presence. I have used two LEDs with common ground (pin 9) and pins 7 and 29 to drive LEDs ([pin mapping](https://developer.nvidia.com/embedded/learn/jetson-nano-2gb-devkit-user-guide). I have used 220$\Omega$ resistors, but LEDs look too dark and I suspect internal resistance is enough. 

## What can be improved?
* Use a smaller network.
* Use TensorRT optimization with FP16 or FP8.
