# Jetson configuration 
**Goal:** Usage of
* Headless (no GUI)
* Tensorflow 2+
* Python by remote SSL usable by a modern IDE with breakpoints, variable inspector, Copilot and etc. - [Dataspell](https://www.jetbrains.com/dataspell/) in my case.
* Native, without Docker container
* *(optional)* JupyterLab 3+ with variable inspector
* Note: `cv2.imshow` does not work for a remote connection

## General setup
### Wi-Fi
For some unknown reason, Wi-Fi does not work out of the box during the start-up setup.

The followingt steps helped me:

1. Reboot:
   `sudo reboot`
2. Operate wifi (from [Adding WiFi to the NVIDIA Jetson](https://learn.sparkfun.com/tutorials/adding-wifi-to-the-nvidia-jetson/all)):

   ```bash
   nmcli d           # list devices (optional)
   nmcli r wifi on   # verify that wifi is on (optional)
   nmcli d wifi list # list available networks (optional)
   sudo nmcli d wifi connect [SSID] password [PASSWORD] # connect to network
   ```
<!--- sudo nmcli d wifi connect SCE password samishamoon?! # connect to network --->
### Utilities and additional configuration
1. [Disable GUI](https://www.forecr.io/blogs/bsp-development/how-to-disable-desktop-gui-on-jetson-modules)
    ```bash
    sudo systemctl set-default multi-user.target
    ```
3. Check and install updates (takes some time):

   ```bash
   sudo apt update
   sudo apt install nvidia-l4t* # upgrade to Jetpack 4.6.3
   sudo apt upgrade 	# (optional) update all
   sudo reboot  		# reboot because of firmware/kernel update
   ```
4. Fix clock to the maximum speed (step 4 [here](https://pyimagesearch.com/2020/03/25/how-to-configure-your-nvidia-jetson-nano-for-computer-vision-and-deep-learning/)):

   ```bash
   sudo nvpmodel -m 0
   sudo jetson_clocks   
   ```
5. Nice [nano](https://www.nano-editor.org/) editor: 
	```bash
	sudo apt-get install nano
	```

   <!--- 2. [Git](https://git-scm.com/): `sudo apt-get install git` --->
6. Python basics:

   ```bash
   sudo apt-get install python3-pip
   ```
7. [jtop](https://rnext.it/jetson_stats/) command:
   ```bash
   sudo -H pip3 install jetson-stats
   ```

## TensorFlow
### TensorFlow 2
(from [Jetson documentation](https://docs.nvidia.com/deeplearning/frameworks/install-tf-jetson-platform/index.html),
   [jetbot script](https://github.com/NVIDIA-AI-IOT/jetbot/blob/master/scripts/create-sdcard-image-from-scratch.sh)
   and [jkjung-avt blog](https://jkjung-avt.github.io/jetpack-4.6/))
1. Install TensorFlow pre-requirements:
   ```bash
   sudo apt install -y libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev \
                     zip libjpeg8-dev liblapack-dev libblas-dev gfortran
   sudo pip3 install --upgrade pip setuptools wheel
   sudo pip3 install -U pip testresources
   sudo pip3 install -U --no-deps numpy==1.19.4 future==0.18.2 mock==3.0.5 \
     keras_preprocessing==1.1.2 keras_applications==1.0.8 \
     gast==0.4.0 protobuf pybind11 cython pkgconfig
   sudo env H5PY_SETUP_REQUIRES=0 pip3 install -U h5py==3.1.0 # takes few minutes!!!
   ```
1. Install TensorFlow 2.6.2 (may show no progress during installation)
   ```bash
   sudo pip3 install --pre --extra-index-url \
     https://developer.download.nvidia.com/compute/redist/jp/v46 \
     tensorflow>=2
   ```
2. Validate installation:
   ```
   TF_CPP_MIN_LOG_LEVEL=3 python3 -c "import tensorflow as tf; tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR); print('tensorflow version: %s' % tf.__version__); print('tensorflow.test.is_built_with_cuda(): %s' % tf.test.is_built_with_cuda()); print('tensorflow.test.is_gpu_available(): %s' % tf.test.is_gpu_available(cuda_only=False, min_cuda_compute_capability=None))"
   ```
### Tensorflow Hub
Pre-trained machine learning models ready for deployment
1. * [Cmake](https://forums.developer.nvidia.com/t/how-does-jetson-nono-update-cmake-to-3-18/182786/4) update (without QT). It is required for build the pre-requirements in the next step. Note, the later version of Cmake (e.g., 1.25) can not be installed directly since the pre-installed version (3.10) is insuffient.
    ```bash
    sudo apt install -y libssl-dev openssl1.0
    wget -c --show-progress https://github.com/Kitware/CMake/releases/download/v3.19.1/cmake-3.19.1.tar.gz
    tar xvf cmake-3.19.1.tar.gz
    mkdir cmake-3.19.1-build
    cd cmake-3.19.1-build
    cmake -DBUILD_QtDialog=OFF ../cmake-3.19.1
    make -j $(nproc)
    #make test
    sudo make install
    cmake --version
    cd ..
    ```
2. Manual install of [requirements](https://github.com/tensorflow/models/blob/master/official/requirements.txt):
    ```python
    sudo pip3 install six 
    sudo pip3 install google-api-python-client
    sudo pip3 install kaggle
    sudo pip3 install oauth2client
    sudo pip3 install psutil
    sudo pip3 install py-cpuinfo>=3.3.0    
    sudo pip3 install tensorflow-model-optimization
    sudo pip3 install tensorflow-datasets
    sudo pip3 install gin-config
    sudo pip3 install tf_slim
    sudo pip3 install Cython
    sudo pip3 install "pyyaml>=5.1,<6.0" --ignore-installed
    sudo pip3 install pycocotools
    sudo pip3 install tensorflow-hub==0.12 # newer version require Python 3.7+
    ```
3. Validate
    ```python
    import tensorflow as tf
    import tensorflow_hub as hub
    ```
* [Example](https://tfhub.dev/google/aiy/vision/classifier/food_V1/1) that also requires `sudo pip3 install scikit-image` (it takes few minutes to install)
### TensorRT
Inference optimization
1. Environment variables (from [TensorRT on the Nvidia Jetson](https://docs.donkeycar.com/guide/robot_sbc/tensorrt_jetson_nano/)); Add the following lines to your `~/.bashrc` file, e.g. by `nano ~/.bashrc`
	```bash
	# Add this to your .bashrc file
	export CUDA_HOME=/usr/local/cuda
	# Adds the CUDA compiler to the PATH
	export PATH=$CUDA_HOME/bin:$PATH
	# Adds the libraries
	export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH
	```
1. Test
	```bash
	source ~/.bashrc
	nvcc --version
	```
1. Install PyCUDA 2021.1 (by [python3.6-pycuda-2021.1](https://github.com/jetson-nano-wheels/python3.6-pycuda-2021.1))
	```bash
	 sudo pip install 'https://github.com/jetson-nano-wheels/python3.6-pycuda-2021.1/releases/download/v0.0.1/pycuda-2021.1-cp36-cp36m-linux_aarch64.whl'
	```
1. Test
	```python
	import tensorrt as trt
	```	
## Jupiter

### Jupiter Notebook

1. Install Jupiter Notebook (from [here](https://bibsian.github.io/posts/jupyter-setup/))
   ```bash
   sudo apt install -y libfreetype6-dev pkg-config libpng-dev jq  
   sudo pip3 install matplotlib 
   sudo pip3 install jupyter
   ```
2. Configure Jupyter:
   ```bash
   jupyter notebook --generate-config
   jupyter notebook password # enter password on promt
   JUPYTER_CONFIG_FILE="$HOME/.jupyter/jupyter_notebook_config.py"
   # Configuration string
   JUPYTER_CONFIG_UPDATE=\
   "c = get_config()

   # Inline plotting
   c.IPKernelApp.pylab = 'inline'

   # Notebook config
   c.NotebookApp.ip = '0.0.0.0'
   c.NotebookApp.open_browser = False  #so that the ipython notebook does not opens up a browser by default
   # Set the port to 8888
   c.NotebookApp.port = 8888

   # Configuration file for jupyter-notebook.
   c.Notebook.allow_origin='*'

   c.InteractiveShellApp.extensions = ['autoreload']
   c.InteractiveShellApp.exec_lines = ['%autoreload 2']"

   # Concat config string with original file and update config file
   sudo printf '%s\n%s\n' "$JUPYTER_CONFIG_UPDATE" "$(sudo cat $JUPYTER_CONFIG_FILE)" > $JUPYTER_CONFIG_FILE
   ```
3. Run Jupiter Notebook:
   ```bash
   jupyter notebook --ip=0.0.0.0
   ```

### Jupiter Lab

1. Dependencies:
   ```bash
   sudo apt install -y libffi-dev libssl1.0-dev
   sudo apt install -y curl
   curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash - # ignore the warning and patiently
   ```
2. Install Jupiter Lab:
   ```bash
   sudo pip3 install jupyterlab
   ```
3. (optional) Variable inspector
   ```bash
   sudo pip3 install lckr-jupyterlab-variableinspector
   ```
3. (optional) Interactive plots functionality with [ipympl](https://matplotlib.org/ipympl/)
   to be used with `%matplotlib ipympl` magic command:
   ```bash
   sudo pip3 install ipympl
   ```
4. Configure Jupyter:
   ```bash
   jupyter lab --generate-config
   jupyter notebook password # enter password on promt
   lab="$HOME/.jupyter/jupyter_lab_config.py"
   # Configuration string
   JUPYTER_CONFIG_UPDATE=\
   "c = get_config()

   # Inline plotting
   c.IPKernelApp.pylab = 'inline'

   # Notebook config
   c.NotebookApp.ip = '0.0.0.0'
   c.NotebookApp.open_browser = False  #so that the ipython notebook does not opens up a browser by default
   # Set the port to 8888
   c.NotebookApp.port = 8888

   # Configuration file for jupyter-notebook.
   c.Notebook.allow_origin='*'

   c.InteractiveShellApp.extensions = ['autoreload']
   c.InteractiveShellApp.exec_lines = ['%autoreload 2']"
   # Concat config string with original file and update config file
   sudo printf '%s\n%s\n' "$JUPYTER_CONFIG_UPDATE" "$(sudo cat $JUPYTER_CONFIG_FILE)" > $JUPYTER_CONFIG_FILE
   ```
1. Run Jupiter lab:
   ```bash
   jupyter lab --ip=0.0.0.0  
   ```

## Video
* Check if it is alive: `ls /dev/video0`
* Another way to check (from [here](https://github.com/jetsonhacks/USB-Camera)): 
  ```bash
  sudo apt install v4l-utils
  v4l2-ctl --list-devices  		# (optional) short information
  v4l2-ctl --all -d /dev/video0	# (optional) detailed information
  ```

### Headless operation
Usage of additional display and keyboard is inconvenient but, fortunately, there are few 'remote' work options.
* Jupyter server as is, with optional extensions.
* Use of IDE with remote Jupyter server support
, e.g. [Dataspell](https://www.jetbrains.com/help/dataspell/configuring-jupyter-notebook.html#remote).
It enables tools like Copilot. Unfortunately, I did not succeed to use a variable inspector in a remote Jupyter mode.
* Use of remote Python by ssh is another option that do includes convenient debugger, variable inspector and Copilot.
* Remote desktop (XRDP) can be configured (e.g. [Remote Desktop - XRDP](https://raspberry-valley.azurewebsites.net/NVIDIA-Jetson-Nano/)). I did not use it.


## Some small final remarks
* It’s a good idea to reboot after the installation: `sudo reboot`
* The order **is** important:
    ```python
    import cv2
    import tensorflow as tf
    ```
* Don't import `tensorflow` if you don't have to.

## Some interesting guides
There are many interesting Jetson posts, I have found them (unfortunately, yet) unuseful:
* [Jetson Nano DNN image](https://github.com/Qengineering/Jetson-Nano-image) - did not succeed to run Jupyter
* [OpenCV upgrage](https://github.com/Qengineering/Install-OpenCV-Jetson-Nano) - after install it altered some other packages