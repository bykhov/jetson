# Jetson configuration (Native, without Docker container)
## Wi-Fi
For some unknow reason, Wi-Fi does not work out of the box.
Steps:
1. Reboot:
`sudo reboot`
2. Operate wifi (from [Adding WiFi to the NVIDIA Jetson](https://learn.sparkfun.com/tutorials/adding-wifi-to-the-nvidia-jetson/all)):
    ```
    nmcli d
    nmcli r wifi on
    nmcli d wifi list
    sudo nmcli d wifi connect SCE password samishamoon?!
    ```
1. Check and install updates: 
    ```
    sudo apt-get update && sudo apt-get upgrade
    sudo reboot
    ```
1. Nice [nano](https://www.nano-editor.org/) editor: `sudo apt-get install nano`

1. Python packages:
    ```
    sudo apt install python3-pip python-pip
    ```

1. [jtop](https://rnext.it/jetson_stats/) command: 
`sudo -H pip3 install jetson-stats`
    
