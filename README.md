# Real-Time-Object-Detection-and-Classification-using-Raspberry-Pi-Pico-and-TinyML
The proposed project implements an intelligent object detection system using a Raspberry Pi Pico WH, an HC-SR04 ultrasonic sensor, and a 1602A LCD display with an I2C interface. This system utilizes TinyML for analyzing and classifying the data collected by the sensor, providing the ability to learn from the surrounding environment and improve obstacle detection.

A key aspect of this project is the real-time storage of collected data on Google Sheets, as well as locally on the Raspberry Pi Pico WH. The data, stored in a file on Google Drive, was used to train a machine learning model so that it could recognize and classify measured distances into three categories: "Alert," "Collision," and "OK." After training the model, an extended dataset was created for validation and testing, ensuring better generalization and optimal performance in obstacle detection.

Additionally, the system includes three LEDs to indicate detection status:

- The green LED lights up for the "OK" state (distances greater than 30 cm).
- The red LED indicates "Collision" (distances less than 10 cm).
- The blue LED signals "Alert" (distances between 10 cm and 30 cm).

Furthermore, a buzzer emits warning sounds:
- In the "Alert" state, it emits an intermittent sound.
- In the case of a "Collision," the sound becomes continuous and faster.


## Importance in the Embedded Systems Field

Embedded systems are fundamental to the development of modern technologies, with applications in various fields such as robotics, industrial automation, and autonomous vehicles. By integrating TinyML, this project significantly enhances on-device data processing, reducing the need for a constant connection to a central server. This approach optimizes resource consumption and enables the system to operate in isolated environments or areas with limited network access.

## Design

Hardware:
- Raspberry Pi Pico WH
- HC-SR04 sensor
- 1602A LCD with I2C interface
- 3 LEDs (green, red, blue)
- 220 Ohm resistors
- Buzzer
- Wires and Breadboard
  
Software:
- Thonny – Integrated Development Environment (IDE) used for writing and testing Python code on the Raspberry Pi Pico WH.
- MicroPython
- TensorFlow and TensorFlow Lite – for developing and converting the machine learning model.
- Scikit-learn – for data preprocessing and training the machine learning model.
- Matplotlib – for visualizing model performance and data analysis.
- Google Sheets API – for integrating and storing collected data in real time on Google Sheets.

## Demonstration Sequence Details

- System Presentation
  ![CircuitFInalFinal123](https://github.com/user-attachments/assets/aa6ba531-990a-4847-b791-a9b3ae0a860d)
  
- Physical Circuit
![475687350_3931644573755068_6428512334918054765_n](https://github.com/user-attachments/assets/62c09ae1-6894-4900-a08d-cde8824d1762)
  
- Model Accuracy
![Precizia](https://github.com/user-attachments/assets/b2f0fdf3-9475-406c-b591-0bae357210e1)

- The Dataset Stored in Google Drive
![Screenshot_6](https://github.com/user-attachments/assets/799e3902-e47a-45fe-9797-8073bd8e8d17)
