# Jetson configuration (Native, without Docker container)
## Wi-Fi
For some unknown reason, Wi-Fi does not work out of the box.
Steps:
1. Reboot:
`sudo reboot`
2. Operate wifi (from [Adding WiFi to the NVIDIA Jetson](https://learn.sparkfun.com/tutorials/adding-wifi-to-the-nvidia-jetson/all)):
    ```
    nmcli d           # list devices
    nmcli r wifi on   # ferify that wifi is on
    nmcli d wifi list # list available networks
    sudo nmcli d wifi connect SCE password samishamoon?! # connect to network
    ```
1. Check and install updates (takes some time): 
    ```
    sudo apt-get update && sudo apt-get upgrade
    sudo reboot  # reboot because of firmware/kernel update
    ```
1. Fix clock to the maximum speed (step 4 [here](https://pyimagesearch.com/2020/03/25/how-to-configure-your-nvidia-jetson-nano-for-computer-vision-and-deep-learning/)):
   ```
   sudo nvpmodel -m 0
   sudo jetson_clocks   
   ```   
1. Nice [nano](https://www.nano-editor.org/) editor: `sudo apt-get install nano`

   <!--- 2. [Git](https://git-scm.com/): `sudo apt-get install git` --->

1. Python basics:
    ```
    sudo apt-get install python3-pip
    ```

1. [jtop](https://rnext.it/jetson_stats/) command: 
`sudo -H pip3 install jetson-stats`
    
## TensorFlow 2
1. Install TensorFlow 2.7 (from [here](https://docs.nvidia.com/deeplearning/frameworks/install-tf-jetson-platform/index.html) and [here](https://jkjung-avt.github.io/jetpack-4.6/)):
    ```
   sudo apt install-y libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev \
                      zip libjpeg8-dev liblapack-dev libblas-dev gfortran
   sudo pip3 install --upgrade pip setuptools wheel
   sudo pip3 install -U pip testresources
   sudo pip3 install -U --no-deps numpy==1.19.4 future==0.18.2 mock==3.0.5 \
      keras_preprocessing==1.1.2 keras_applications==1.0.8 \
      gast==0.4.0 protobuf pybind11 cython pkgconfig
   sudo env H5PY_SETUP_REQUIRES=0 pip3 install -U h5py==3.1.0
   sudo pip3 install --pre --extra-index-url \
      https://developer.download.nvidia.com/compute/redist/jp/v46 \
      tensorflow>=2
    ```
