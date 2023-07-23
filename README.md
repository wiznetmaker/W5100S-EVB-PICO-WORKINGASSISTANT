# W5100S-EVB-PICO-WORKINGASSISTANT

## 1. Project Overview
This is a work assistance project utilizing W5100S-EVB-PICO and Arducam.

## 2. Project Details
- The project involves capturing images every 5 seconds through a camera connected to Pico and transmitting them via ethernet.
- The transmitted images are processed using a Fine-tuned YOLOv8 model to perform object detection on the user's work status. The model is trained to recognize six classes: Normal, Drowsiness, Yawning, Distraction, and Mobile usage.
- The recognized objects are counted to analyze work patterns, and the results are transmitted and displayed on a web interface.

## 3. Code and Libraries
The code was written using Thonny IDE and CircuitPython. Copy the lib folder, boot_out.txt, and code.py files from the repo to W5100S-EVB-PICO and run code.py. Refer to the link above to build the hardware by combining the W5100s-evb-pico board with the arducam and circuitpython to get the webcam working. 

We used the Bundle for Version 7.x of the CircuitPython libraries, and for the Adafruit_CircuitPython_wiznet5k library, we used the 1.12.15 release version.

Download links:
- [CircuitPython Libraries](https://circuitpython.org/libraries)
- [ArduCAM PICO_SPI_CAM Python](https://github.com/ArduCAM/PICO_SPI_CAM/tree/master/Python)
- [Adafruit_CircuitPython_Wiznet5k 1.12.15](https://github.com/adafruit/Adafruit_CircuitPython_Wiznet5k/releases/tag/1.12.15)

The code from the previous project [Upscaling Image with AI using W5100S-EVB-PICO and Arducam](https://maker.wiznet.io/Benjamin/projects/upscaling-image-with-ai-using-w5100s-evb-pico-and-arducam/) was refined and simplified using ChatGPT.

## 4. YOLOv8 Model Training
Dataset: [Roboflow Project](https://universe.roboflow.com/project-q3daq/working-0iym3)
Model: Ultralytics's YOLOv8 Nano (fast and small)
mAP50: 0.857, mAP50-95: 0.498
We utilized the free GPU provided by Google Colab.
[Google Colab Notebook](https://colab.research.google.com/drive/1NStVVPItzzwoeldfsPJ-geZATkirvg2z?usp=sharing)

## 5. Original Link
For more information, please visit the [original project page](https://maker.wiznet.io/Benjamin/projects/working-assistant-with-w5100s-evb-pico/?serob=4&serterm=month).

## 6. Similar Projects
For other similar projects, please visit [Upscaling image with AI using W5100S-EVB-Pico and Arducam](https://maker.wiznet.io/Benjamin/projects/upscaling-image-with-ai-using-w5100s-evb-pico-and-arducam/).
