import time
import numpy as np

# Constants
CALIBRATE = 0
MOVE  = 1
FRAME = 2
UP    = 0
DOWN  = 1
NOCALIBRATION = 0
CALIBRATION   = 1
FRAME_CONFIG  = '101101'

# Globals
arduino = None
numMotors = 0
motor_pos = []
frame_pos = []
numFrames = 0

def init_serial(serial, num_motors, num_frames):
    global arduino, numMotors, motor_pos
    arduino = serial
    if not arduino == None:
        arduino.flush()
    numMotors = num_motors
    for i in range(numMotors):
        motor_pos.append(-1)
    init_frames(num_frames)

def init_frames(num_frames):
    global frame_pos, numFrames
    numFrames = num_frames
    frame_pos = []
    for i in range(numFrames):
        frame_pos.append(-1)

def config_frames(threading_matrix):
    frame_config     = []
    #Match Threading to FrameConfig
    for i in range(numFrames):
        temp_frame = []
        for j in range(numMotors):
            if threading_matrix[i][j] == 1:
                temp_frame.append(j)
        frame_config.append(temp_frame)
   
    print("Frame Config = ", frame_config)

    #Transmit Singular Frame
    for x in range(len(frame_config)):
        motor_list_string = ""
        frame_num         = str("{:02d}".format(x))
        motor_list        = frame_config[x]
        motor_list_string += frame_num

        #print("Frame Number = ", frame_num)
        for y in motor_list:
            motor_list_string += str("{:02d}".format(y))
        motor_list_string += '\r'
        #print("Motor List w/ Frame Num = ", motor_list_string)

        #Sending Frame Config Command & Data
        write_read_frameConfig(motor_list_string)
        time.sleep(0.1)

def write_read_frameConfig(motor_list_string):
    frame_config_msg = "722"
    data = ""
    #Sending Frame Config Command
    print("Sending Value: ", bytes(frame_config_msg+"\n", 'utf-8'))
    arduino.write(bytes(frame_config_msg+"\n", 'utf-8'))

    #Sending Frame Config
    print("Sending Value: ", bytes(motor_list_string, 'utf-8'))
    arduino.write(bytes(motor_list_string+",", 'utf-8'))

    time.sleep(0.1)

    #Receiving
    print("Waiting w/ = ", arduino.in_waiting)
    print("data =")
    while arduino.in_waiting:
        data += str(arduino.readline().decode())

    print(data)

def write_read(x):
    print("sent: " + x)
    arduino.write(bytes(x+"\n", 'utf-8'))
    time.sleep(0.1)
    data = ""
    while arduino.in_waiting:
        data += str(arduino.readline()) + "\n"
    return data

def get_message_str(motor, calibration, direction, mode):
    return str(motor << 4 | direction << 3 | mode << 1 | calibration)

def move_motor(motor, calibration, direction, mode):
    print(write_read(get_message_str(motor, calibration, direction, mode)))
    if mode == MOVE:
        motor_pos[motor-1] = direction
    if mode == FRAME:
        frame_pos[motor-1] = direction

def calibrate_all():
    for i in range(numMotors):
        print(write_read(get_message_str(i+1, CALIBRATION, 0, 0)))
        motor_pos[i] = DOWN
    for i in range(numFrames):
        frame_pos[i] = DOWN

def move_row(row):
    inds = [i for i, x in enumerate(row) if x == 1]
    for i in inds:
        if motor_pos[i] == DOWN:
            move_motor(i + 1, NOCALIBRATION, UP, MOVE)
    inds = [i for i, x in enumerate(row) if x == 0]
    for i in inds:
        if motor_pos[i] == UP:
            move_motor(i + 1, NOCALIBRATION, DOWN, MOVE)
    print(row)

def move_frame(frames):
    print(frames)
    # all 1's in frames should move that frame up, otherwise move that frame down
    inds = [i for i, x in enumerate(frames) if x == 1]
    print(inds)
    for i in inds:
        print(frame_pos[i])
        if frame_pos[i] == DOWN:
            move_motor(i + 1, NOCALIBRATION, UP, FRAME)
    inds = [i for i, x in enumerate(frames) if x == 0]
    for i in inds:
        if frame_pos[i] == UP:
            move_motor(i + 1, NOCALIBRATION, DOWN, FRAME)
