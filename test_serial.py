import serial
import time
import numpy as np

#Test File for Configuring the Frames on Arduino

x           = 722
test_config = "00092638110523\r"
data    = ""
arduino = serial.Serial(port="COM7", baudrate=115200, timeout=1) 
time.sleep(2)

if not arduino == None:
  arduino.flush()
  arduino.reset_input_buffer()
  arduino.reset_output_buffer()

#Sending Frame Config Command
print("Sending Value: ", bytes(str(x)+"\n", 'utf-8'))
arduino.write(bytes(str(x)+"\n", 'utf-8'))

#time.sleep(1)

#Sending Frame Config
print("Sending Value: ", bytes(str(test_config), 'utf-8'))
arduino.write(bytes(str(test_config)+",", 'utf-8'))

time.sleep(0.1)

#Receiving
print("Waiting w/ = ", arduino.in_waiting)
print("data =")
while arduino.in_waiting:
  data += str(arduino.readline().decode())

print(data)
