import serial
from app import App
from serialCom import init_serial
import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
print(ports)
port_names = []
for port, desc, hwid in sorted(ports):
    if "arduino" in desc:
        port_names.append(port)
print(port_names)
connected = False
arduino = None
for port in port_names:
    try:
        arduino = serial.Serial(port=port, baudrate=115200, timeout=.1)
        connected = True
    except serial.serialutil.SerialException:
        print(port + " not available, continuing without connection")

numMotors = 40
numFrames = 4
numPedals = 6
pattern_length2 = 20

init_serial(arduino, numMotors, numFrames)
app = App([numMotors, 0, pattern_length2, numFrames, numPedals])
app.mainloop()