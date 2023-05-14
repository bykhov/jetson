# Person *presence* example
## Goal
* Inference pre-trained object-detection network and process its output
* Remote SSL access (fully headless)
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
The electrical scheme follows [demo](https://automaticaddison.com/how-to-blink-an-led-using-nvidia-jetson-nano/#:~:text=In%20order%20to%20get%20the,7%20on%20the%20Jetson%20Nano.) with two LEDs lighting interchangeably for presence or non-presence.

## What can be improved?
* Use a smaller network.
* Use TensorRT optimization with FP16 or FP8. I have even taken a free project on Courser ([certificate](https://coursera.org/share/678fc097e9f7fb2e99b11a569bb6cb08)). It is also similar to Nvidia [course](https://courses.nvidia.com/courses/course-v1:DLI+L-FX-18+V2/course/) (that is free for me as an academic ambassador).
