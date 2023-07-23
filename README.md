# W5100S-EVB-PICO-WORKINGASSISTANT

## 1. Project Overview
This is a work assistance project utilizing W5100S-EVB-PICO and Arducam.

## 2. Project Details
- The project involves capturing images every 5 seconds through a camera connected to Pico and transmitting them via ethernet.
- The transmitted images are processed using a Fine-tuned YOLOv8 model to perform object detection on the user's work status. The model is trained to recognize six classes: Normal, Drowsiness, Yawning, Distraction, and Mobile usage.
- The recognized objects are counted to analyze work patterns, and the results are transmitted and displayed on a web interface.

## 3. Original Link
For more information, please visit the [original project page](https://maker.wiznet.io/Benjamin/projects/working-assistant-with-w5100s-evb-pico/?serob=4&serterm=month).
