# W5100S-EVB-PICO-WORKINGASSISTANT

## 1. Project Overview
- This is a work assistance project utilizing W5100S-EVB-PICO and Arducam.

## 2. Project Details
- ![image](https://github.com/dbtjr1103/W5100S-EVB-PICO-WORKINGASSISTANT/assets/115054808/689e8eb8-cade-4f04-a20e-ddaa7af0697f)

- The project involves capturing images every 5 seconds through a camera connected to Pico and transmitting them via ethernet.
  
- The transmitted images are processed using a Fine-tuned YOLOv8 model to perform object detection on the user's work status. The model is trained to recognize five classes: Normal, Drowsiness, Yawning , Distraction, and Mobile usage.
  
- The recognized objects are counted to analyze work patterns, and the results are transmitted and displayed on a web interface.

## 3. Code and Libraries
- The code was written using Thonny IDE and CircuitPython. 

- Copy the lib folder, boot_out.txt, and code.py files from the repo to W5100S-EVB-PICO and run code.py. 

- Refer to the link above to build the hardware by combining the W5100s-evb-pico board with the arducam and circuitpython to get the webcam working. 

- We used the Bundle for Version 7.x of the CircuitPython libraries, and for the Adafruit_CircuitPython_wiznet5k library, we used the 1.12.15 release version.

- Download links:
  - [CircuitPython Libraries](https://circuitpython.org/libraries)
  - [ArduCAM PICO_SPI_CAM Python](https://github.com/ArduCAM/PICO_SPI_CAM/tree/master/Python)
  - [Adafruit_CircuitPython_Wiznet5k 1.12.15](https://github.com/adafruit/Adafruit_CircuitPython_Wiznet5k/releases/tag/1.12.15)

- The code from the previous project [Upscaling Image with AI using W5100S-EVB-PICO and Arducam](https://maker.wiznet.io/Benjamin/projects/upscaling-image-with-ai-using-w5100s-evb-pico-and-arducam/) was refined and simplified using ChatGPT.

- The ArduCam OV2640 Module requires CS, MOSI, MISO, SCLK pins for SPI connection, and SDA, SCL pins for I2C connection. This project modified the source code of ArduCam to use SPI1.

    - SPI1 configuration for ArduCam OV2640:
      - CS --> GPIO 13
      - MOSI --> GPIO 11
      - MISO --> GPIO 12
      - SCLK --> GPIO 10

    - I2C configuration for ArduCam OV2640:
      - SDA --> GPIO 8
      - SCL --> GPIO 9


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
-  ![image](https://github.com/dbtjr1103/W5100S-EVB-PICO-WORKINGASSISTANT/assets/115054808/7ddcfc63-1f3b-4953-b7aa-3bac7163973c)


- Inference:
    ![image](https://github.com/dbtjr1103/W5100S-EVB-PICO-WORKINGASSISTANT/assets/115054808/1ce25d84-259e-40f8-9236-a4ff644a181e)

## 5. Inference to Web
- Run the `working_assistant.py` file.
- Code Explanation:

    - **Setup**: The script first sets up a Flask application and defines some global variables. `url` is the URL from which images are fetched. `save_dir` is the directory where fetched images are saved. `inference_dir` is the directory where images after inference are saved. `results` is a dictionary that keeps track of the count of different object detection results.

    - **fetch_image_and_inference()**: This function runs in an infinite loop. In each iteration, it fetches an image from the URL, saves it to the `save_dir`, runs a YOLO object detection model on the image, and updates the `results` dictionary based on the output of the model. The function then waits for 10 seconds before starting the next iteration.

    - **serve_image()**: This is a Flask route that serves an HTML page. The page contains an image element that displays the latest inferred image and several paragraph elements that display the counts of different object detection results. The page refreshes every 10 seconds.

    - **get_inferred_image()**: This is another Flask route that serves the latest inferred image. The image is fetched from the `inference_dir`.

    - **Main Execution**: If the script is run as the main program, it starts the `fetch_image_and_inference()` function in a new thread and then starts the Flask application.


## 6. Original Link
- For more information, please visit the [original project page](https://maker.wiznet.io/Benjamin/projects/working-assistant-with-w5100s-evb-pico/?serob=4&serterm=month).

## 7. Similar Projects
- For other similar projects, please visit [Upscaling image with AI using W5100S-EVB-Pico and Arducam](https://maker.wiznet.io/Benjamin/projects/upscaling-image-with-ai-using-w5100s-evb-pico-and-arducam/).
