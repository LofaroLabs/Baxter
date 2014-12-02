import sys
sys.path.append('/home/archr/hubo_simulation/files/dynamixel')
import os
import dynamixel
import serial_stream
import time
import random
import sys
import subprocess
import optparse
import yaml
import dynamixel_network
import numpy as np
from ovrsdk import *

#Oclus
panlist = [0, 0, 0, 0, 0];
tiltlist = [0, 0, 0, 0, 0];
#Assigning from profile
Ax = [1024,2047]


def rad2dyn(rad):
    return np.int(np.floor( (rad + np.pi)/(2.0 * np.pi) * 1024 ))

def dyn2rad(en):
    return ((en*2.0*np.pi)/Ax[0]) - np.pi

def main(settings): 
    portName = settings['port']
    baudRate = settings['baudRate']
    highestServoId = settings['highestServoId']

    # Establish a serial connection to the dynamixel network.
    # This usually requires a USB2Dynamixel
    serial = serial_stream.SerialStream(port=portName, baudrate=baudRate, timeout=1)
    net = dynamixel_network.DynamixelNetwork(serial)
    
    # Ping the range of servos that are attached
    print "Scanning for Dynamixels..."
    net.scan(1, highestServoId)
    
    myActuators = []
    for dyn in net.get_dynamixels():
        print dyn.id
        myActuators.append(net[dyn.id])
    
    if not myActuators:
      print 'No Dynamixels Found!'
      sys.exit(0)
    else:
      print "...Done"
    
    for actuator in myActuators:
        '''actuator.moving_speed = 80
        actuator.synchronized = True
        actuator.torque_enable = True'''
        #actuator.torque_limit = 400
        #actuator.max_torque = 400
        actuator.moving_speed = 1023
        #print "actuator speed %d" %(actuator._get_moving_speed());
        actuator.synchronized = True
        #actuator._set_torque_limit(0)
        actuator.torque_enable = True
        #myActuators[1]._set_moving_speed(1023);         

    '''Oculus Rift stuff'''
    ovr_Initialize()
    hmd = ovrHmd_Create(0)
    hmdDesc = ovrHmdDesc()
    ovrHmd_GetDesc(hmd, byref(hmdDesc))
    print hmdDesc.ProductName
    ovrHmd_StartSensor( \
        hmd, 
        ovrSensorCap_Orientation | 
        ovrSensorCap_YawCorrection, 
        0
    )


    #read data in real-time           
    timeout = time.time() + 60*180   #Terminate 180 minutes from now
    while True:    
        actuator.read_all()
        time.sleep(0.016)                
        ss = ovrHmd_GetSensorState(hmd, ovr_GetTimeInSeconds())
        pose = ss.Predicted.Pose
        tilt = rad2dyn(pose.Orientation.x*np.pi);
        #tiltscaled=tilt*1.00;
        #myActuators[8]._set_goal_position(tilt);
        pan = rad2dyn(pose.Orientation.y*np.pi);
        #panscaled=pan*1.20;
        #myActuators[9]._set_goal_position(pan);  
        #tiltlist.append(rad2dyn(pose.Orientation.x*np.pi));
        #panlist.append(rad2dyn(pose.Orientation.y*np.pi));  
        #panlist.pop(0);    
        #tiltlist.pop(0);                
        #tilt = np.mean(tiltlist);
        #pan = np.mean(panlist);  '''
        #myActuators[0]._set_synchronized(1);        
        myActuators[0]._set_goal_position(pan);         
        myActuators[1]._set_goal_position(tilt);           
        '''print "myact 0 speed %d" %(myActuators[0]._get_moving_speed());            
        print "myact 1 speed %d" %(myActuators[1]._get_moving_speed());  
        #print "myact 0 load %d" %(myActuators[0]._get_current_load());       
        #print "myact 1 load %d" %(myActuators[1]._get_current_load());       
        print "myact 0 load %d" %(myActuators[0]._get_torque_limit());       
        print "myact 1 load %d" %(myActuators[1]._get_torque_limit()); 
        #print "myact %d" %(myActuators[1]._get_moving_speed());           
        print "myact 0 pos %d" %(myActuators[0]._get_goal_position());
        print "myact 1 pos %d" %(myActuators[1]._get_goal_position());  '''
        print "tilt %d pan %d" %(tilt,pan)
        net.synchronize()     

def validateInput(userInput, rangeMin, rangeMax):
    '''
    Returns valid user input or None
    '''
    try:
        inTest = int(userInput)
        if inTest < rangeMin or inTest > rangeMax:
            print "ERROR: Value out of range [" + str(rangeMin) + '-' + str(rangeMax) + "]"
            return None
    except ValueError:
        print("ERROR: Please enter an integer")
        return None
    
    return inTest

if __name__ == '__main__':
    
    parser = optparse.OptionParser()
    parser.add_option("-c", "--clean",
                      action="store_true", dest="clean", default=False,
                      help="Ignore the settings.yaml file if it exists and \
                      prompt for new settings.")
    
    (options, args) = parser.parse_args()
    
    # Look for a settings.yaml file
    settingsFile = 'settings.yaml'
    if not options.clean and os.path.exists(settingsFile):
        with open(settingsFile, 'r') as fh:
            settings = yaml.load(fh)
    # If we were asked to bypass, or don't have settings
    else:
        settings = {}
        if os.name == "posix":
            portPrompt = "Which port corresponds to your USB2Dynamixel? \n"
            # Get a list of ports that mention USB
            try:
                possiblePorts = subprocess.check_output('ls /dev/ | grep -i usb',
                                                        shell=True).split()
                possiblePorts = ['/dev/' + port for port in possiblePorts]
            except subprocess.CalledProcessError:
                sys.exit("USB2Dynamixel not found. Please connect one.")
                
            counter = 1
            portCount = len(possiblePorts)
            for port in possiblePorts:
                portPrompt += "\t" + str(counter) + " - " + port + "\n"
                counter += 1
            portPrompt += "Enter Choice: "
            portChoice = None
            while not portChoice:                
                portTest = raw_input(portPrompt)
                portTest = validateInput(portTest, 1, portCount)
                if portTest:
                    portChoice = possiblePorts[portTest - 1]

        else:
            portPrompt = "Please enter the port name to which the USB2Dynamixel is connected: "
            portChoice = raw_input(portPrompt)
    
        settings['port'] = portChoice
        
        # Baud rate
        baudRate = None
        while not baudRate:
            brTest = raw_input("Enter baud rate [Default: 1000000 bps]:")
            if not brTest:
                baudRate = 1000000
            else:
                baudRate = validateInput(brTest, 9600, 1000000)
                    
        settings['baudRate'] = baudRate
        
        # Servo ID
        highestServoId = None
        while not highestServoId:
            hsiTest = raw_input("Please enter the highest ID of the connected servos: ")
            highestServoId = validateInput(hsiTest, 1, 255)
        
        settings['highestServoId'] = highestServoId
        
        # Save the output settings to a yaml file
        with open(settingsFile, 'w') as fh:
            yaml.dump(settings, fh)
            print("Your settings have been saved to 'settings.yaml'. \nTo " +
                   "change them in the future either edit that file or run " +
                   "this example with -c.")
    
    main(settings)
