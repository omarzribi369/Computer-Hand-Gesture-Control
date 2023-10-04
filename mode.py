#!/usr/bin/env python
# coding: utf-8

# In[3]:

# import the required libraries
import cv2 # OpenCV library for computer vision
import numpy # library for numerical operations
import mouse # library for controlling mouse actions
import mediapipe # library for media processing
import time # library for measuring time
import math # library for mathematical operations
import numpy as np # alias for numpy library
import pyautogui # library for controlling GUI actions
import autopy # library for controlling GUI actions
from ctypes import cast, POINTER # for casting variables to specific types
from comtypes import CLSCTX_ALL # for specifying context type in activation
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume # library for controlling audio endpoint
from math import hypot # library for mathematical operations
import screen_brightness_control as sbc # library for controlling screen brightness
import keyboard
import threading
# activate audio endpoint
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)


#Get the width and height of the screen
wScr, hScr = autopy.screen.size()
#Set the minimum height value
hmin = 50
#Set the maximum height value
hmax = 200
#Set the width of the volume bar
volBar = 400
#Set the initial volume percentage to 0
volPer = 0
#Set the initial volume to 0
vol = 0
#Set the color of the volume bar
color = (0,215,255)
#Set the initial playback time to 0
pTime = 0



def scrollone(img,lmList,fingers):
    
    # Check if the landmark list is not empty
    if len(lmList) != 0 and len(fingers)==5:
        
        # Check if two fingers are present
        if fingers == [0,1,0,0,0]:
            
            def simulate_hotkey():
                pyautogui.hotkey('up')
            thread = threading.Thread(target=simulate_hotkey)
            thread.start()
            
        # Check if three fingers are present
        if fingers == [0,1,1,0,0]:
            
            def simulate_hotkey():
                pyautogui.hotkey('down')
            thread = threading.Thread(target=simulate_hotkey)
            thread.start()
            
        




def scroll(img,lmList,fingers):
    
    # Check if the landmark list is not empty
    if len(lmList) != 0:
        
        # Check if two fingers are present
        if fingers == [0,1,0,0,0]:
            # Scroll down by 300 units
            pyautogui.scroll(300) 
        # Check if three fingers are present
        if fingers == [0,1,1,0,0]:
            # Scroll up by 300 units
            pyautogui.scroll(-300)
        # Check if no fingers are present
 
                    

def volume2(img, lmList, fingers, color, volume, volRange, minVol, maxVol):
    try:
        
        # Check if lmList is not empty
        if len(lmList) != 0:
            # Calculate the angle between the index and thumb fingers
            angle = math.degrees(math.atan2(lmList[4][2] - lmList[2][2], lmList[4][1] - lmList[2][1]) - math.atan2(lmList[8][2] - lmList[6][2], lmList[8][1] - lmList[6][1]))
            # Adjust the volume based on the angle
            vol = np.interp(angle, [0, 90], [minVol, maxVol])
            # Set the master volume level using the calculated volume
            volume.SetMasterVolumeLevel(vol, None)
            # Calculate the position of the volume bar
            volBar = np.interp(vol, [minVol, maxVol], [400, 150])
            # Calculate the percentage of the volume
            volPer = np.interp(vol, [minVol, maxVol], [0, 100])
            # Convert the volume to an integer
            volN = int(vol)
            # Check if the volume is divisible by 4
            if volN % 4 != 0:
                volN = volN - volN % 4
                if volN >= 0:
                    volN = 0
                elif volN <= -64:
                    volN = -64
                elif vol >= -11:
                    volN = vol
            # Draw two circles and a line to represent the hand gesture
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            cv2.circle(img, (x1, y1), 10, color, cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, color, cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), color, 3)
            cv2.circle(img, (cx, cy), 8, color, cv2.FILLED)
            # Draw a red circle at the center of the gesture if the volume is too low
            if volN <= -50:
                cv2.circle(img, (cx, cy), 11, (0, 0, 255), cv2.FILLED)
            # Draw an outline of the volume bar
            cv2.rectangle(img, (30, 150), (55, 360), (209, 206, 0), 3)
            # Fill the volume bar with the calculated position
            cv2.rectangle(img, (30, int(volBar)), (55, 360), (215, 255, 127), cv2.FILLED)
            # Display the percentage of the volume
            cv2.putText(img, f'{int(volPer)}%', (25, 389), cv2.FONT_HERSHEY_COMPLEX, 0.9, (209, 206, 0), 3)
            
    except IndexError:
        # Handle case where the landmark list does not have required landmarks
        print("index out of range")
        return img

        


def brightness(img, lmList):
    try:
        x_1, y_1 = lmList[4][1], lmList[4][2]
        # Store x,y coordinates of (tip of) index finger
        x_2, y_2 = lmList[20][1], lmList[20][2]
        # Draw two green filled circles at (x_1, y_1) and (x_2, y_2)
        cv2.circle(img, (x_1, y_1), 7, (0, 255, 0), cv2.FILLED)
        cv2.circle(img, (x_2, y_2), 7, (0, 255, 0), cv2.FILLED)
        # Draw a green line between (x_1, y_1) and (x_2, y_2)
        cv2.line(img, (x_1, y_1), (x_2, y_2), (0, 255, 0), 3)
        # Calculate the distance between two points
        L = hypot(x_2-x_1, y_2-y_1)
        # Map the distance to a brightness level between 0 and 100
        b_level = np.interp(L, [15, 220], [0, 100])
        # Set the brightness to the calculated level
        sbc.set_brightness(int(b_level))
      
    except IndexError:
        # Handle case where the landmark list does not have required landmarks
        print("index out of range")
        return img


    
    
    

def take_screenshots(img,lmList,fingers):
    # Get current timestamp
    #timestamp = int(time.time())
    # Generate filename
    #filename = "screenshot_{}.png".format(timestamp)
    # Take screenshot
    #screenshot = pyautogui.screenshot()
    # Save screenshot
    #screenshot.save(filename)
    def simulate_hotkey():
            pyautogui.hotkey('win', 'printscreen')
    thread = threading.Thread(target=simulate_hotkey)
    thread.start()
        

def detect_finger_gesture(L_prev,lmList):
    try:
        x_1, y_1 = lmList[4][1], lmList[4][2]
        x_2, y_2 = lmList[12][1], lmList[12][2]
        hand_distance = hypot(x_2 - x_1, y_2 - y_1)
        # Check if both x_1 and y_1 are defined
        if x_1 is not None and y_1 is not None:
            # Check if both x_2 and y_2 are defined
            if x_2 is not None and y_2 is not None:
                # Calculate the current distance between two points
                L = hypot(x_2 - x_1, y_2 - y_1)
                # Calculate a factor to adjust the thresholds based on the hand distance
                distance_factor = hand_distance / 1000
                # Calculate adjusted thresholds based on distance factor
                opening_threshold = int(60 * distance_factor)
                closing_threshold = int(60 * distance_factor)
                # Check if the two fingers are opening
                if L > L_prev + opening_threshold:
                    # Add a shortcut to maximize the window
                    print("Maximizing Window")
                    keyboard.press_and_release('windows+up')
                    time.sleep(0.5)
                # Check if the two fingers are closing
                elif L < L_prev - closing_threshold:
                    # Add a shortcut to minimize the window
                    print("Minimizing Window")
                    keyboard.press_and_release('windows+down')
                    time.sleep(0.5)
                return L
    except IndexError:
        # Handle case where the landmark list does not have required landmarks
        print("index out of range")
        return img            
    
    return None
               
                
            
                


             


# In[ ]:




