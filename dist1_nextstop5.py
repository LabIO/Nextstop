#Libraries
import RPi.GPIO as GPIO
import time
import datetime
import OSC
from gpiozero import MotionSensor

# define pin for motion sensor
pir = MotionSensor(17) 

# set time interval between readings
T = 0.1

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM) # Use phisical pin numbering

GPIO_LED = 4
GPIO_BUTT = 21
GPIO.setup(GPIO_BUTT, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 21 as input


# set led pin
GPIO.setup(GPIO_LED,GPIO.OUT)


#setup osc client
oscClient = OSC.OSCClient()
oscClient.connect(('localhost',5000))



if __name__ == '__main__':
    try:

        while True:
			
            ### detect motion
            if pir.motion_detected:
                motion = 1
                #print(motion)
                GPIO.output(GPIO_LED,True)
            else:
                motion = 0
                #print(motion)
                GPIO.output(GPIO_LED,False)
            time.sleep(T)
            
            # send motion 
            oscmsg1 = OSC.OSCMessage()
            oscmsg1.setAddress("/move")
            oscmsg1.append(motion)
            oscClient.send(oscmsg1)
            oscmsg1.clearData()
            
            ### check button
            if GPIO.input(GPIO_BUTT) == GPIO.HIGH:
                #print("Button pushed!")
                butt = 0
            else:
                butt = 1
			
            
            # send button    
            oscmsg = OSC.OSCMessage()
            oscmsg.setAddress("/butt")
            oscmsg.append(butt)
            oscClient.send(oscmsg)
            oscmsg.clearData()
				
            
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("  Measurement stopped by User")
