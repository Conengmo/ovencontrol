# ovencontrol

This project consists of two parts: Python code to process measurements and design a controler, and Arduino code that implements the controller.

Note that you need a specially modified oven to actually work with the controller.


## Python
First install the package localy without copying files by running this pip command:

`pip install -e {path to the folder with this file}`

or on linux:

`pip install --user -e {path to the folder with this file}`

Next you can run the files in the 'ovencontrol' folder to:

- open and plot the system identication data
- model the plant (i.e. the oven)
- model the controller
- open and plot the controller test data


## Arduino

The Arduino part consists of three files. 

'AutoPID.cpp' and 'AutoPID.h' are the AutoPID library by rdownin4 under MIT license.

https://github.com/r-downing/AutoPID

'ovencontrol.ino' is the Arduino script.

If you want to change the timings, you can do that by altering the values in `getSetPoint()`. Note that in some phases the phase is ended at a certain temperature, and in some after a certain number of seconds. 

