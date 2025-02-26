# Real-Time-Object-Detection-and-Classification-using-Raspberry-Pi-Pico-and-TinyML
The proposed project implements an intelligent object detection system using a Raspberry Pi Pico WH, an HC-SR04 ultrasonic sensor, and a 1602A LCD display with an I2C interface. This system utilizes TinyML for analyzing and classifying the data collected by the sensor, providing the ability to learn from the surrounding environment and improve obstacle detection.

A key aspect of this project is the real-time storage of collected data on Google Sheets, as well as locally on the Raspberry Pi Pico WH. The data, stored in a file on Google Drive, was used to train a machine learning model so that it could recognize and classify measured distances into three categories: "Alert," "Collision," and "OK." After training the model, an extended dataset was created for validation and testing, ensuring better generalization and optimal performance in obstacle detection.

Additionally, the system includes three LEDs to indicate detection status:

The green LED lights up for the "OK" state (distances greater than 30 cm).
The red LED indicates "Collision" (distances less than 10 cm).
The blue LED signals "Alert" (distances between 10 cm and 30 cm).
Furthermore, a buzzer emits warning sounds:

In the "Alert" state, it emits an intermittent sound.
In the case of a "Collision," the sound becomes continuous and faster.
