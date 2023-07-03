import serial
import time
import numpy as np

x    = 1111110010
data = ""
arduino = serial.Serial(port="COM7", baudrate=115200, timeout=1) 
time.sleep(2)

if not arduino == None:
  arduino.flush()
  arduino.reset_input_buffer()
  arduino.reset_output_buffer()

#Sending & Receiving

#Sending
print("Sending Value: ", bytes(str(x)+"\n", 'utf-8'))
arduino.write(bytes(str(x)+"\n", 'utf-8'))

time.sleep(0.1)

#Receiving
print("Waiting w/ = ", arduino.in_waiting)
while arduino.in_waiting:
  data += str(arduino.readline().decode())

print("data = ", data)
