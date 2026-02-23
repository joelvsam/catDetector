# Real-Time Cat Detection and Alert System

## Abstract

This project presents a real-time cat detection and alert system implemented on a Raspberry Pi. The system leverages a custom-trained YOLOv8n object detection model to identify cats in a live video stream from a Pi Camera. Upon detection, the system provides visual feedback on a web interface and triggers an audible alert using a passive buzzer. A PIR motion sensor is integrated to optimize performance by activating the detection logic only when motion is present. The entire system is managed by a Flask web application, offering a user-friendly interface for monitoring and control.

## 1. Introduction

The need for automated monitoring of specific animals, such as domestic cats, arises in various scenarios, including wildlife monitoring, pet tracking, or deterring strays from a particular area. This project addresses this need by developing an intelligent, low-cost, and standalone system for detecting cats in real-time. By combining a powerful deep learning model with common hardware components, we create an efficient solution that can be easily deployed in any environment with a power source. The system not only identifies cats but also provides immediate feedback through a web interface and an audible alarm, making it a practical tool for automated surveillance.

## 2. Tools and Technology Stack

The project integrates both hardware and software components to achieve its functionality.

### 2.1. Hardware
- **Raspberry Pi:** The central processing unit for the entire system.
- **Pi Camera:** Provides the live video feed for the object detection model.
- **PIR Motion Sensor:** Detects motion to trigger the detection process, conserving resources.
- **Passive Buzzer:** Serves as an audible alert mechanism upon cat detection.

### 2.2. Software and Libraries
- **Python:** The primary programming language for the project.
- **Ultralytics YOLOv8:** A state-of-the-art, real-time object detection model used for identifying cats.
- **PyTorch:** The deep learning framework used to train and run the YOLOv8 model.
- **Flask:** A micro web framework used to create the web application for live streaming and control.
- **OpenCV (cv2):** A library for computer vision tasks, including image processing and rendering bounding boxes on the video feed.
- **Picamera2:** The official library for controlling the Raspberry Pi Camera.
- **RPi.GPIO & gpiozero:** Python libraries for interfacing with the GPIO pins on the Raspberry Pi to control the PIR sensor and buzzer.
- **Jupyter Notebook:** Used for the model training and experimentation pipeline.

## 3. Methodology

The project is divided into two main phases: model training and system deployment.

### 3.1. Model Training

1.  **Dataset:** The model was trained on the **Oxford-IIIT Pet Dataset**, which contains images of 37 different breeds of cats and dogs. For this project, only the cat annotations were used.

2.  **Data Preprocessing:** The original annotations were in XML format. A script was used to parse these XML files and convert the bounding box information into the YOLO format, which requires a normalized `*.txt` file for each image.

3.  **Training:** A YOLOv8n (nano) model, pre-trained on the COCO dataset, was fine-tuned on the prepared cat dataset. The training was conducted for 50 epochs, resulting in a model (`best.pt`) optimized for detecting cats.

### 3.2. System Deployment

The trained model was deployed on a Raspberry Pi using a Python script (`final.py`). The deployment architecture is as follows:

1.  **Motion-Activated Detection:** A PIR sensor continuously monitors for motion. When motion is detected, it signals the system to start processing the camera feed. This is handled in a separate thread to avoid blocking the main application.

2.  **Video Processing:** The `Picamera2` library captures frames from the camera. Each frame is passed to the YOLOv8 model for inference.

3.  **Cat Detection and Alert:** If the model detects an object with the "cat" class, it draws a bounding box around it. Simultaneously, the `RPi.GPIO` library is used to activate a buzzer, providing an audible alert.

4.  **Web Interface:** A Flask web application serves a web page with the live video stream. The stream is an MJPEG stream where each frame is annotated with bounding boxes and a counter for the number of detected cats. The web interface also includes buttons to enable or disable the PIR sensor and the buzzer, giving the user control over the system's operation.

## 4. Future Work

While the current system is fully functional, there are several potential areas for improvement and expansion:

- **Enhanced Model:** The model could be trained on a more diverse dataset, including different lighting conditions, cat breeds, and poses to improve detection accuracy.
- **Database Integration:** Store detection events (timestamp, image) in a database for later review and analysis.
- **Cloud Integration:** Send notifications to a mobile device or a cloud dashboard when a cat is detected.
- **Advanced Alert System:** Implement different alert sounds or even a system to play a pre-recorded message to deter cats.
- **Improved Power Management:** Optimize the code and hardware usage to allow for battery-powered operation.
- **Containerization:** Use Docker to containerize the application for easier deployment and dependency management.

---
