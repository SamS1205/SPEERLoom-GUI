import serial
from app import App
from serialCom import init_serial
from constants import *
import serial.tools.list_ports

connected = False
arduino = None

ports = serial.tools.list_ports.comports()
print(ports)
port_names = []
for port, desc, hwid in sorted(ports):
    if "arduino" in desc:
        port_names.append(port)
print(port_names)
for port in port_names:
    try:
        arduino = serial.Serial(port=port, baudrate=115200, timeout=.1)
        connected = True
    except serial.serialutil.SerialException:
        print(port + " not available, continuing without connection")
numMotors = NUM_MOTORS
numFrames = 4
numPedals = 6
pattern_length2 = 20

init_serial(arduino, numMotors, numFrames)
app = App([numMotors, 0, pattern_length2, numFrames, numPedals])
app.mainloop()
#TODO: Add a hard reset here so the motors reset to down position