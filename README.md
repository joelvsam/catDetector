# catDetector
Cat Detection using Raspberry Pi and YOLO detection model
A Raspberry Pi 4 Model B is used for this project.

Open the link https://drive.google.com/file/d/1pXYTHO10JxiZAftAYDCLgxqQIEioaPHZ/view?usp=drive_link and download the file OxfordPets.zip.
Extract it.
Open YOLOFinal.ipynb in Jupyter
Run the code.
The training may take upto 24 hours.
After training is completed, it generate a message pointing where 'best.pt' is saved.
Alternatively use the best.pt from this repository if you dont want to train the model yourself.

-Raspberry Pi Setup-
Connect the camera module to the Raspberry Pi.
Connect the Outpin pin of PIR sensor to GPIO12 of the Raspberry Pi.
Connect the Vcc and Ground of PIR sensor to pins 4 and 6 of Raspberry Pi respectively.
Connect the positive of the buzzer to GPIO18 and negative to the pin 30.
Make sure the raspberry pi imaging is completed.

-Running Python Code-
Connect the Raspberry Pi to a monitor, mouse and keyboard.
Alternatively you can use RealVNC Viewer in your PC for remote control of the Raspberry Pi.
Transfer the python code final.py and best.pt to the Raspberry Pi using a USB or remotely.
Run the Terminal on Raspberry Pi.
Create a virtual environment.
Install the following packages
pip install --upgrade pip
pip install flask gpiozero ultralytics opencv-python numpy.

-Running the application-
Activate your virtual environment.
Run python final.py.
Open a browser on any device in the same network and go to: http://<raspberry_pi_ip>:5000
You will see the Flask webpage.





