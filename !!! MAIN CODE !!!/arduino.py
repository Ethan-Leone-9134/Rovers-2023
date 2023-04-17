# !/usr/bin/env python3
# -- coding: utf-8 -*-

# NOTE: Do not remove above code, it tells the pi what coding language is being used!

# Author - Ethan Leone
# Date - March 31st, 2023
# Description - This file is the python portion of a connection between a raspberry pi and an arduino 
# Notes - This connection does require some feedback after each command from the arduino in order to proceed.

# Funtion List
# connect - Establishes usb connection
# reset - Resets the arduino
# tellArm - Sends a G-Code string to the arduino as a number
# exit - Break usb connection
# gCode2num - Converts the G-Code string to the number

# %% Start Imports ###
import time                 # Allows to pause
import serial as ser        # Interfaces with the arduino
### End imports ###


#%%####### Start Custom Functions ##########

def connect():
    # Function to establish a connection with an arduino using serial connection via a USB cable
    # Inputs  : none
    # Outputs : none
    # Globals : uno - Holds the serial connection to the arduino

    global uno  # Serial communication variable

    while True:                                                 # Loop until the connection has been established
        try:
            uno = ser.Serial('/dev/ttyACM0', 115200, timeout=0.1)       # Enable arduino communication (pi)
            # Notes for serial function which established the connection:
            # Inputs  : port - String name of the port which the arduino connects to the device
            #           baudWidth - Rate of communication between pi and arduino (MUST be the same on both)
            #           timeout=0.1 - Specifies seconds for the arduino to wait for data
            # Outputs : uno - serial connection between devices
        except:
            print("ERROR : The arudino is not connected to the Pi. Attempting to reconnect...")     # Inform that the connection has not been made
            time.sleep(0.5)                                             # Wait half a second
        else:
            time.sleep(1.8)                                             # Gives the connection time to finalize
            print("--- Arduino Connection Is Established ---")
            print("-----------------------------------------")
            break


def reset():
    # Function reset the connected arduino and gives a 2-second delay to allow the arduino to finish resetting
    # Inputs  : none
    # Outputs : none
    # Globals : uno - Holds the serial connection to the arduino

    global uno              # Call the connection
    uno.setDTR(False)       # Set active to false
    time.sleep(0.1)         # Give it 1/10 second to process
    uno.setDTR(True)        # Set active to true
    time.sleep(1.9)           # Allow uno to run the setup function and start


def tellArm(gCode):
    # Tells the arduino what to do
    # Inputs  : gCode - command for the arm
    # Outputs : none
    # Globals : uno - Holds the serial connection to the arduino
    # Example : setPin(10, 0) - Turns off pin 10

    global uno

    gCommand = gCode2num(gCode)

    try:
        uno.write(str(gCommand).encode())                # Try to transmit through serial connection
    except:
        print("Arduino is no longer connected !!!")     # Warn about a disconnection if transmittion fails
        connect()                          # Attempt to reconnect to arduino
    else:
        noResponse = 1                                  # Logical variable to know if the arduino has returned a response
        while noResponse:
            data = uno.readline()                       # Read the serial monitor
            if data:                                    # If the serial monitor said anything
                rawData = data.rstrip('\n'.encode('latin-1'))  # Convert monitor to bytes
                print("Arduino: " + rawData.decode('latin-1'))  # Print data
                noResponse = 0                          # Let main code progress


def exit():
    # Callback function to disable pins 3-12 on the arduino
    # Inputs  - none
    # Outputs - none
    # Globals : uno - Holds the serial connection to the arduino

    global uno                  # Calls the arduino communication variable

    print("----------------------------")  # Ending display
    try:
        time.sleep(0.5)         # Let arduino disable pins
        reset()                 # Restart arduino
        uno.close()             # End arduino communication
    except:
        print("The arduino was disconnected improperly.")
    else:
        print("--- Arduino Disconnected ---")
        print("----------------------------")
    print("---- Program Terminated ----")
    print("----------------------------")


def gCode2num(inputString):
    inputString = inputString.replace(" ", "")
    length = len(inputString)
    [firstChar, secondChar] = inputString[:2]
    if length > 2:
        command = ('%04d' % (int(inputString[2:]))).replace('-', '9')
    else:
        command = '0000'
    if firstChar == 'P':
        comCode = f"1{secondChar}{command}"
    elif firstChar == 'S':
        comCode = f"2{secondChar}{command}"
    elif firstChar == 'Q':
        comCode = f"3{secondChar}{command}"
    elif firstChar == 'M':
        comCode = f"4{secondChar}{command}"
    elif firstChar == 'R':
        comCode = f"5{secondChar}{command}"
    elif firstChar == 'K':
        comCode = f"6{secondChar}{command}"
    elif firstChar == 'H':
        comCode = f"7{secondChar}{command}"
    elif firstChar == 'E':
        comCode = f"8{secondChar}{command}"
    else:
        comCode = "000000"

    return comCode
