# W5100S-EVB-PICO-WORKINGASSISTANT

## 1. Project Overview
This is a work assistance project utilizing W5100S-EVB-PICO and Arducam.

## 2. Project Details
- The project involves capturing images every 5 seconds through a camera connected to Pico and transmitting them via ethernet.
  
- The transmitted images are processed using a Fine-tuned YOLOv8 model to perform object detection on the user's work status. The model is trained to recognize six classes: Normal, Drowsiness, Yawning, Distraction, and Mobile usage.
  
- The recognized objects are counted to analyze work patterns, and the results are transmitted and displayed on a web interface.

## 3. Code and Libraries
- The code was written using Thonny IDE and CircuitPython. 

- Copy the lib folder, boot_out.txt, and code.py files from the repo to W5100S-EVB-PICO and run code.py. 

- Refer to the link above to build the hardware by combining the W5100s-evb-pico board with the arducam and circuitpython to get the webcam working. 

- We used the Bundle for Version 7.x of the CircuitPython libraries, and for the Adafruit_CircuitPython_wiznet5k library, we used the 1.12.15 release version.

Download links:
- [CircuitPython Libraries](https://circuitpython.org/libraries)
- [ArduCAM PICO_SPI_CAM Python](https://github.com/ArduCAM/PICO_SPI_CAM/tree/master/Python)
- [Adafruit_CircuitPython_Wiznet5k 1.12.15](https://github.com/adafruit/Adafruit_CircuitPython_Wiznet5k/releases/tag/1.12.15)

- The code from the previous project [Upscaling Image with AI using W5100S-EVB-PICO and Arducam](https://maker.wiznet.io/Benjamin/projects/upscaling-image-with-ai-using-w5100s-evb-pico-and-arducam/) was refined and simplified using ChatGPT.

## 4. YOLOv8 Model Training

![image](https://github.com/dbtjr1103/W5100S-EVB-PICO-WORKINGASSISTANT/assets/115054808/13861027-142c-4fab-993a-ee066d88405d)

  
### YOLOv8 Model

YOLOv8 is a powerful object detection model. It is the latest iteration in the YOLO series of models. YOLOv8 is designed to be fast and accurate, with a focus on simultaneous detection and classification. It is capable of detecting multiple objects in an image or video and classifying them in real-time, making it highly effective for many computer vision tasks.

- ![image](https://github.com/dbtjr1103/W5100S-EVB-PICO-WORKINGASSISTANT/assets/115054808/493d763f-3c68-47b7-ab90-aafeb746727b)
- ![image](https://github.com/dbtjr1103/W5100S-EVB-PICO-WORKINGASSISTANT/assets/115054808/3d38b116-25a2-4a91-919e-d732f3653881)

### Nano Model

The Nano model is a smaller and faster version of the standard model. It is designed for efficiency and can run at higher speeds with less computational resources, making it ideal for deployment on devices with limited computational power such as mobile devices and embedded systems.

- ![image](https://github.com/dbtjr1103/W5100S-EVB-PICO-WORKINGASSISTANT/assets/115054808/4bb2e3d2-1e41-4d16-9634-c98fe59599a7)

### Usage

To use these models in your project, you can install the Ultralytics package in a Python>=3.8 environment with PyTorch>=1.7 using the following command:

```bash
pip install ultralytics
```


- Dataset: [Roboflow Project](https://universe.roboflow.com/project-q3daq/working-0iym3)
- ![image](https://github.com/dbtjr1103/W5100S-EVB-PICO-WORKINGASSISTANT/assets/115054808/45899134-3630-4fc8-9e7a-f174cf524355)

- Model: Ultralytics's YOLOv8 Nano (fast and small)

- mAP50: 0.857, mAP50-95: 0.498.

- We utilized the free GPU provided by Google Colab.

- [Google Colab Notebook](https://colab.research.google.com/drive/1NStVVPItzzwoeldfsPJ-geZATkirvg2z?usp=sharing).

- Inference: ![image](https://github.com/dbtjr1103/W5100S-EVB-PICO-WORKINGASSISTANT/assets/115054808/1ce25d84-259e-40f8-9236-a4ff644a181e)


## 5. Original Link
- For more information, please visit the [original project page](https://maker.wiznet.io/Benjamin/projects/working-assistant-with-w5100s-evb-pico/?serob=4&serterm=month).

## 6. Similar Projects
- For other similar projects, please visit [Upscaling image with AI using W5100S-EVB-Pico and Arducam](https://maker.wiznet.io/Benjamin/projects/upscaling-image-with-ai-using-w5100s-evb-pico-and-arducam/).
