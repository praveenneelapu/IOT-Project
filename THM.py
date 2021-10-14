import time
import sys
import ibmiotf.application
import ibmiotf.device

#Provide your IBM Watson Device Credentials
organization = "f2cody" # repalce it with organization ID
deviceType = "rsip" #replace it with device type
deviceId = "9010" #repalce with device id
authMethod = "token"
authToken = "1234567890"#repalce with token

def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data)        
        if cmd.data['command']=='motoron':
                print("MOTOR ON")
        elif cmd.data['command'] == 'motoroff':
            print("MOTOR OFF")
                
try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

deviceCli.connect()

while True:
        T=50;
        H=32;
        M=45;
        #Send Temperature,moisture & Humidity to IBM Watson
        data ={'d': { 'temperature' : T, 'humidity': H, 'moisture': M}}
        #print data
        def myOnPublishCallback():
            print ("Published Temperature = % s C" % T, "Humidity = % s" % H, "moisture= % s C/M" % M,"to IBM Watson")

        success = deviceCli.publishEvent("event", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(1)
        
        deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()
