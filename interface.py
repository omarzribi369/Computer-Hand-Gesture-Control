#Importing necessary modules
from PIL import Image,ImageTk # for working with images and displaying them in tkinter
from tkinter import Scrollbar,PhotoImage # for creating scrollbar and displaying image in tkinter
import customtkinter # custom tkinter library
import cv2 # for image processing
import mediapipe as mp # for hand tracking
import numpy as np # for working with arrays
import mode as md # custom module for hand gestures
import mouse # for mouse control
import pyautogui, autopy # for simulating keyboard and mouse actions
import time # for sleep and time calculations
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume # for audio control
from comtypes import CLSCTX_ALL # for audio control
from ctypes import cast, POINTER # for audio control
import threading # for running multiple processes simultaneously
import os # for working with files and directories
from win10toast import ToastNotifier # for creating desktop notifications in Windows 10
from multiprocessing import Process
import pygame
from plyer import notification
import csv
import math
import joblib
import pandas as pd

customtkinter.set_appearance_mode("Dark")  # Modes: system (default), light, dark
#customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

notification_shown = False
notif = False
pausenotif=False
resumenotif=False
toaster = ToastNotifier()

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands 

# Setting the width and height of the camera
wCam, hCam = 640, 480
# Initializing the camera using OpenCV
cap = cv2.VideoCapture(1)
# Setting the camera width and height
cap.set(3,wCam)
cap.set(4,hCam)
# Initializing a variable to store the time
pTime = 0
# Getting the default audio device
devices = AudioUtilities.GetSpeakers()
# Activating the audio device
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
# Casting the audio interface to a pointer
volume = cast(interface, POINTER(IAudioEndpointVolume))
# Getting the volume range for the audio device
volRange = volume.GetVolumeRange()
# Get screen size
wScr, hScr = autopy.screen.size() 
print(wScr, hScr)
# Set default values for the initial X and Y positions
pX, pY = 0, 0  
# Set default values for the current X and Y positions
cX, cY = 0, 0
# Set the minimum volume
minVol = -63
# Get the maximum volume from the volRange list and print the list
maxVol = volRange[1]
print(volRange)
# Set the minimum and maximum hue values
hmin = 50
hmax = 200
# Set the volume bar width
volBar = 400
# Set the volume percentage to 0
volPer = 0
# Set the volume to 0
vol = 0
# Set the color used for drawing
color = (0,215,255)
# Set the list of tip IDs
tipIds = [4, 8, 12, 16, 20]
# Set the default mode to an empty string
mode = ''
# Set the default active status to 0
active = 0
# Disable the fail-safe feature of pyautogui
pyautogui.FAILSAFE = False

L_prev=0
cl=0
start_time = 0
has_executed = True
threshold=1
scroll_start_time=0
SCROLL_DURATION = 0.5
k= time.time()
n=0
right=False
b=0
close_mode_active=False
time1=0


KEY_POINTS = [0, 4 ,5, 8, 12, 16, 20,3,9,6,10,14,18]



model = joblib.load('RFC_model.pkl')


class App(customtkinter.CTk):
    
    def __init__(self):
        super().__init__()
        self.mod=''
        #mouse smooth
        self.smooth=2
        #accelerator variable
        self.acc=4
        self.preprocessing_enabled = False
        self.custom = False
        self.ac=False
        self.close_pro=False
        self.run=False
        self.p = None
        self.ch=True
        self.ges=''
        self.gest1=''
        self.gest2=''
        self.gest3=''
        self.gest4=''
        self.gest5=''
        self.gest6=''
        self.gest7=''
        self.gest8=''
        self.gest9=''
        self.gest10=''
        self.gest11=''
        self.gest12=''
        self.gest13=''
        self.gest14=''
        self.gest15=''
        self.gest16=''
        self.gest17=''
        self.gest18=''
        self.gest19=''
        self.gest20=''
        self.textc='white'
        self.hoverc='#005e80'
        main_font = customtkinter.CTkFont(family="Helvetica", size=12)
        # configure window
        self.title("hand gesture controler")
        self.geometry(f"{1100}x{580}")
        self.picture_frame_visible = False
        self.visible=False
        self.visible1=False
        self.st=0
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        
        
        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=6, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(12, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Menu", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame,text="Get started" ,command=self.clicked)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame,text="options" ,command=self.option)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame,text="about us", command=self.about)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame,text="game",command=self.start_process)
        self.sidebar_button_4.grid(row=8, column=0, padx=20, pady=10)
        
        
        
       
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=4, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Dark","Light"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=5, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 20))

        
        
        # create label to display webcam feed
        
        
        self.video_label = customtkinter.CTkLabel(self, width=300, height=150, text=None)
        self.video_label.grid(row=0, column=1, padx=50, pady=(10,70), sticky="nsew")
        #self.video_label.place(x=200, y=10)
        
        
        
        
        self.sidebar_button1 = customtkinter.CTkButton(
           
            self,
            # Set the button text to "start"
            text="start",
            # Set the button click action to the clicked1 method
            command=self.star,
            # Set the button height to 40 and width to 120
            height=40,
            width=120,
            # Set the button border width to 2 and corner radius to 20
            
            corner_radius=20
           
)
        self.sidebar_button1.place(x=550, y=650)
        self.sidebar_button2 =  customtkinter.CTkButton(
           
            self,
            # Set the button text to "stop"
            text="stop",
            # Set the button click action to the clicked1 method
            command=self.stop,
            # Set the button height to 40 and width to 120
            height=40,
            width=120,
            # Set the button border width to 2 and corner radius to 20
            
            corner_radius=20
)
        self.sidebar_button2.place(x=850, y=650)
        
        # create sidebar frame and position it
        self.sidebar_frame1 = customtkinter.CTkFrame(self, width=200, height=500, corner_radius=0)
        self.sidebar_frame1.place(x=0, y=0)
        
        # create label for smoothing and position it
        self.smoothing_label = customtkinter.CTkLabel(self, text="Smooth:")
        self.smoothing_label.place(x=230, y=10)
        self.smoothing_label.place_forget()
        #create option menu for smoothing and position it
        self.smoothing = customtkinter.CTkOptionMenu(
          self, 
          values=["1","2","3", "4","5", "6","7", "8"],
          command=lambda value: self.update_smooth(value))
        self.smoothing.place(x=230, y=30)
        self.smoothing.place_forget()
        
        # create label for accelerator and position it
        self.accelerator = customtkinter.CTkLabel(self, text="accelerator:")
        self.accelerator.place(x=230, y=10)
        self.accelerator.place_forget()
        #create option menu for accelerator and position it
        self.accelerator1 = customtkinter.CTkOptionMenu(
          self, 
          values=["1","2","3", "4","5", "6","7", "8","9","10"],
          command=lambda value: self.update_accelerator(value))
        self.accelerator1.place(x=230, y=30)
        self.accelerator1.place_forget()
        
        # create label for contrast and position it
        self.contrast = customtkinter.CTkLabel(self, text="contrast:")
        self.contrast.place(x=230, y=50)
        self.contrast.place_forget()
        # create option menu for contrast and position it
        self.contrast1 = customtkinter.CTkOptionMenu(
          self, 
          values=["disable","enable"],
          command=lambda value: self.update_preprocessing_enabled(value)
          )
        self.contrast1.place(x=230, y=80)
        self.contrast1.place_forget()
        
        self.brightness1 = customtkinter.CTkLabel(self, text="brightness:")
        self.brightness1.place(x=230, y=50)
        self.brightness1.place_forget()
        # create option menu for contrast and position it
        self.brightness = customtkinter.CTkOptionMenu(
          self, 
          values=["disable","enable"],
          command=lambda value: self.update_brightness(value)                
          
          )
        self.brightness.place(x=230, y=80)
        self.brightness.place_forget()
        
        
        self.close1 = customtkinter.CTkLabel(self, text="close:")
        self.close1.place(x=230, y=50)
        self.close1.place_forget()
        # create option menu for contrast and position it
        self.close = customtkinter.CTkOptionMenu(
          self, 
          values=["disable","enable"],
          command=lambda value: self.update_close(value)                
          
          )
        self.close.place(x=230, y=80)
        self.close.place_forget()
        
        self.custom1 = customtkinter.CTkLabel(self, text="Customisable gestures")
        self.custom1.place(x=230, y=320)
        self.custom1.place_forget()
        
        self.custom_button = customtkinter.CTkOptionMenu(
          self, 
          values=["disable","enable"],
          command=lambda value: self.custom_enabled(value)
          )
        self.custom_button.place(x=230, y=350)
        self.custom_button.place_forget()
        
       
        
        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=600, height=600, font=("Roboto", 24))
        self.textbox.place(x=230, y=30)
        self.textbox.place_forget()
        self.textbox.insert("0.0","As a developer, I am always looking for innovative   ways to make technology more accessible and user-friendly. That's why I created a computer hand gesture controller using a webcam application.\n\nThe idea for this project came to me when I was thinking about how people interact with technology. While traditional input devices like keyboards and mice are effective, they can be cumbersome and limit the user's mobility. I wanted to create a more intuitive and natural way for people to control their computers.\n\nUsing a webcam application, I developed a hand gesture recognition system that allows users to control their computer using simple hand movements. By mapping different gestures to specific actions, users can navigate their computer, launch applications, and perform various tasks without ever touching a keyboard or mouse.\n\nI believe that this technology has the potential to revolutionize the way we interact with our devices, especially for people with physical disabilities or mobility issues. It provides a more accessible and user-friendly interface that allows everyone to easily control their computer with ease.\n\nOverall, I am proud to have developed this technology and I hope that it will continue to evolve and improve in the future. By leveraging the power of artificial intelligence and computer vision, we can create a more intuitive and natural way for people to interact with technology, making it more accessible and user-friendly for everyone.")
        
        # Open and resize the first image
        image1 = Image.open("im1.jpg").convert('RGBA')
        image1 = image1.resize((500, 280))
        # Create a PhotoImage object for the first image
        self.pic = ImageTk.PhotoImage(image1)
        # Create a custom Tkinter label widget for the first image
        self.im1 = customtkinter.CTkLabel(self, image=self.pic, text=None, width=300, height=280)
        # Place the first image label widget on the window
        self.im1.place(x=350, y=60)
        # Hide the first image label widget
        self.im1.place_forget()
        
        # Open and resize the second image
        image2 = Image.open("im3.jpg").convert('RGBA')
        image2 = image2.resize((500, 281))
        # Create a PhotoImage object for the second image
        self.pic1 = ImageTk.PhotoImage(image2)
        # Create a custom Tkinter label widget for the second image
        self.im0 = customtkinter.CTkLabel(self, image=self.pic1, text=None, width=300, height=300)
        # Place the second image label widget on the window
        self.im0.place(x=350, y=120)
        # Hide the second image label widget
        self.im0.place_forget()
        
        # add 10 buttons to get started menu 
        self.sidebar_button_1 = customtkinter.CTkButton(
            # Attach the button to the first sidebar frame
            self.sidebar_frame1,
            # Set the button text to "cursor"
            text="cursor",
            # Set the button click action to the clicked1 method
            command=self.clicked1,
            text_color=self.textc,
            hover= True,
            hover_color= self.hoverc,
            height=30,
            width= 90,
            border_width=2,
            corner_radius=20,
            border_color= "#4682B4",
            fg_color= "transparent"
)
        # Place the button in the first row and first column of the sidebar frame with padding of 20 and 15 pixels
        self.sidebar_button_1.grid(row=0, column=0, padx=20, pady=15)

        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame1, text="scroll", command=self.clicked2
               ,
    
    text_color="white",
    hover= True,
    hover_color= "#005e80",
    height=30,
    width= 90,
    border_width=2,
    corner_radius=20,
    border_color= "#4682B4",
    fg_color= "transparent"
   
                                      )
        self.sidebar_button_2.grid(row=0, column=1, padx=20, pady=15)

        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame1, text="volume", command=self.clicked3
                                                       ,
    
    text_color="white",
    hover= True,
    hover_color= "#005e80",
    height=30,
    width= 90,
    border_width=2,
    corner_radius=20,
    border_color= "#4682B4",
    fg_color= "transparent"
)
        self.sidebar_button_3.grid(row=0, column=2, padx=20, pady=15)
        
        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame1, text="brightness", command=self.clicked4
                                                       ,
    
    text_color="white",
    hover= True,
    hover_color= "#005e80",
    height=30,
    width= 90,
    border_width=2,
    corner_radius=20,
    border_color= "#4682B4",
    fg_color= "transparent"
)
        self.sidebar_button_4.grid(row=0, column=3, padx=20, pady=15)
        
        self.sidebar_button_5 = customtkinter.CTkButton(self.sidebar_frame1, text="pause", command=self.clicked5,
                                                       
    
    text_color="white",
    hover= True,
    hover_color= "#005e80",
    height=30,
    width= 90,
    border_width=2,
    corner_radius=20,
    border_color= "#4682B4",
    fg_color= "transparent"
)
        self.sidebar_button_5.grid(row=0, column=4, padx=20, pady=15)
        
        self.sidebar_button_6 = customtkinter.CTkButton(self.sidebar_frame1, text="resume", command=self.clicked6,
    
    text_color="white",
    hover= True,
    hover_color= "#005e80",
    height=30,
    width= 90,
    border_width=2,
    corner_radius=20,
    border_color= "#4682B4",
    fg_color= "transparent"
)
        self.sidebar_button_6.grid(row=0, column=5, padx=20, pady=15)        

        self.sidebar_button_7 = customtkinter.CTkButton(self.sidebar_frame1, text="screenshot", command=self.clicked7
                                                       ,
    
   text_color="white",
    hover= True,
    hover_color= "#005e80",
    height=30,
    width= 90,
    border_width=2,
    corner_radius=20,
    border_color= "#4682B4",
    fg_color= "transparent"
)
        self.sidebar_button_7.grid(row=0, column=6, padx=20, pady=15)        
        
        self.sidebar_button_8 = customtkinter.CTkButton(self.sidebar_frame1, text="close", command=self.clicked8
                                                       ,
   text_color="white",
    hover= True,
    hover_color= "#005e80",
    height=30,
    width= 90,
    border_width=2,
    corner_radius=20,
    border_color= "#4682B4",
    fg_color= "transparent"
)
        self.sidebar_button_8.grid(row=0, column=7, padx=20, pady=15)        
        
        self.sidebar_button_9 = customtkinter.CTkButton(self.sidebar_frame1, text="maxmin", command=self.clicked9
                                                       ,
    
    text_color="white",
    hover= True,
    hover_color= "#005e80",
    height=30,
    width= 90,
    border_width=2,
    corner_radius=20,
    border_color= "#4682B4",
    fg_color= "transparent"
)
        self.sidebar_button_9.grid(row=0, column=8, padx=20, pady=15)       

        self.sidebar_button_10 = customtkinter.CTkButton(self.sidebar_frame1, text="program", command=self.clicked10
                                                       ,
    
    text_color="white",
    hover= True,
    hover_color= "#005e80",
    height=30,
    width= 90,
    border_width=2,
    corner_radius=20,
    border_color= "#4682B4",
    fg_color= "transparent"
)
        self.sidebar_button_10.grid(row=0, column=9, padx=20, pady=15)        
        # Hide the sidebar-frme1 
        self.sidebar_frame1.place_forget()
        
        # add 10images to get started menu
        # Load image and convert to RGBA format
        image = Image.open("pic01.png").convert('RGBA')
        # Resize image to 1000 x 562
        image = image.resize((1000, 562))
        # Convert image to a tkinter compatible PhotoImage object
        self.picture = ImageTk.PhotoImage(image)
        # Create a custom label widget with image and no text
        self.picture_label = customtkinter.CTkLabel(self, image=self.picture, text=None, width=1000, height=562)
        # Position the label widget at coordinates (350, 60)
        self.picture_label.place(x=350, y=60)
        # Hide the label widget
        self.picture_label.place_forget()
        
        image1 = Image.open("pic2.png").convert('RGBA')
        image1 = image1.resize((1000, 562))
        self.picture1 = ImageTk.PhotoImage(image1)
        self.picture_label1 = customtkinter.CTkLabel(self, image=self.picture1, text=None, width=1000, height=562)
        self.picture_label1.place(x=350, y=60)
        self.picture_label1.place_forget()
        
        image2 = Image.open("pic5.png").convert('RGBA')
        image2 = image2.resize((1000, 562))
        self.picture1 = ImageTk.PhotoImage(image2)
        self.picture_label2 = customtkinter.CTkLabel(self, image=self.picture1, text=None, width=1000, height=562)
        self.picture_label2.place(x=350, y=60)
        self.picture_label2.place_forget()
        
        image3 = Image.open("pic51.png").convert('RGBA')
        image3 = image3.resize((1000, 562))
        self.picture3 = ImageTk.PhotoImage(image3)
        self.picture_label3 = customtkinter.CTkLabel(self, image=self.picture3, text=None, width=1000, height=562)
        self.picture_label3.place(x=350, y=60)
        self.picture_label3.place_forget()
        
        image4 = Image.open("pic06.png").convert('RGBA')
        image4 = image4.resize((1000, 562))
        self.picture4 = ImageTk.PhotoImage(image4)
        self.picture_label4 = customtkinter.CTkLabel(self, image=self.picture4, text=None, width=1000, height=562)
        self.picture_label4.place(x=350, y=60)
        self.picture_label4.place_forget()
        
        image5 = Image.open("pic07.png").convert('RGBA')
        image5 = image5.resize((1000, 562))
        self.picture5 = ImageTk.PhotoImage(image5)
        self.picture_label5 = customtkinter.CTkLabel(self, image=self.picture5, text=None, width=1000, height=562)
        self.picture_label5.place(x=350, y=60)
        self.picture_label5.place_forget()
        
        image6 = Image.open("pic08.png").convert('RGBA')
        image6 = image6.resize((1000, 562))
        self.picture6 = ImageTk.PhotoImage(image6)
        self.picture_label6 = customtkinter.CTkLabel(self, image=self.picture6, text=None, width=1000, height=562)
        self.picture_label6.place(x=350, y=60)
        self.picture_label6.place_forget()
        
        image7 = Image.open("pic09.png").convert('RGBA')
        image7 = image7.resize((1000, 562))
        self.picture7 = ImageTk.PhotoImage(image7)
        self.picture_label7 = customtkinter.CTkLabel(self, image=self.picture7, text=None, width=1000, height=562)
        self.picture_label7.place(x=350, y=60)
        self.picture_label7.place_forget()
        
        image8 = Image.open("pic10.png").convert('RGBA')
        image8 = image8.resize((1000, 562))
        self.picture8 = ImageTk.PhotoImage(image8)
        self.picture_label8 = customtkinter.CTkLabel(self, image=self.picture8, text=None, width=1000, height=562)
        self.picture_label8.place(x=350, y=60)
        self.picture_label8.place_forget()
        
        image9 = Image.open("pic11.png").convert('RGBA')
        image9 = image9.resize((1000, 562))
        self.picture9 = ImageTk.PhotoImage(image9)
        self.picture_label9 = customtkinter.CTkLabel(self, image=self.picture9, text=None, width=1000, height=562)
        self.picture_label9.place(x=350, y=60)
        self.picture_label9.place_forget()
        
        ges1 = Image.open("g1.png").convert('RGBA')
        ges1 = ges1.resize((112, 94))
        self.picges1 = ImageTk.PhotoImage(ges1)
        self.picges1_label1 = customtkinter.CTkLabel(self, image=self.picges1, text=None, width=100, height=10)
        
        self.opges1 = customtkinter.CTkOptionMenu(
          self, 
          values=["","scroll_up","scroll_down","volume","cursor","VLC"],
        command=lambda value: self.update_gesture1(value))
        
        ges2 = Image.open("g2.png").convert('RGBA')
        ges2 = ges2.resize((66, 69))
        self.picges2 = ImageTk.PhotoImage(ges2)
        self.picges2_label1 = customtkinter.CTkLabel(self, image=self.picges2, text=None, width=100, height=10)
        
        
        self.opges2 = customtkinter.CTkOptionMenu(
          self, 
          values=["","scroll_up","scroll_down","volume","cursor","VLC"],
        command=lambda value: self.update_gesture2(value))
        
        
        ges3 = Image.open("g3.png").convert('RGBA')
        ges3 = ges3.resize((70, 87))
        self.picges3 = ImageTk.PhotoImage(ges3)
        self.picges3_label1 = customtkinter.CTkLabel(self, image=self.picges3, text=None, width=100, height=10)
        
        self.opges3 = customtkinter.CTkOptionMenu(
          self, 
          values=["","scroll_up","scroll_down","volume","cursor","VLC"],
        command=lambda value: self.update_gesture3(value))
        
        ges4 = Image.open("g4.png").convert('RGBA')
        ges4 = ges4.resize((70, 97))
        self.picges4 = ImageTk.PhotoImage(ges4)
        self.picges4_label1 = customtkinter.CTkLabel(self, image=self.picges4, text=None, width=100, height=10)
        
        
        self.opges4 = customtkinter.CTkOptionMenu(
          self, 
          values=["","scroll_up","scroll_down","volume","cursor","VLC"],
        command=lambda value: self.update_gesture4(value))
        
        
        ges5 = Image.open("g5.png").convert('RGBA')
        ges5 = ges5.resize((70, 96))
        self.picges5 = ImageTk.PhotoImage(ges5)
        self.picges5_label1 = customtkinter.CTkLabel(self, image=self.picges5, text=None, width=100, height=10)
        
        
        self.opges5 = customtkinter.CTkOptionMenu(
          self, 
          values=["","scroll_up","scroll_down","volume","cursor","VLC"],
        command=lambda value: self.update_gesture5(value))
        
        
        ges6 = Image.open("g6.png").convert('RGBA')
        ges6 = ges6.resize((80, 75))
        self.picges6 = ImageTk.PhotoImage(ges6)
        self.picges6_label1 = customtkinter.CTkLabel(self, image=self.picges6, text=None, width=100, height=10)
        
        
        self.opges6 = customtkinter.CTkOptionMenu(
          self, 
          values=["","chrome","Telegam","window file","brightness_up","brightness_down"],
        command=lambda value: self.update_gesture6(value))
        
        
        ges7 = Image.open("g7.png").convert('RGBA')
        ges7 = ges7.resize((70, 85))
        self.picges7 = ImageTk.PhotoImage(ges7)
        self.picges7_label1 = customtkinter.CTkLabel(self, image=self.picges7, text=None, width=100, height=10)
        
        
        self.opges7 = customtkinter.CTkOptionMenu(
          self, 
          values=["","chrome","Telegam","window file","brightness_up","brightness_down"],
        command=lambda value: self.update_gesture7(value))
        
        
        ges8 = Image.open("g8.png").convert('RGBA')
        ges8 = ges8.resize((94, 112))
        self.picges8 = ImageTk.PhotoImage(ges8)
        self.picges8_label1 = customtkinter.CTkLabel(self, image=self.picges8, text=None, width=100, height=10)
        
        
        self.opges8 = customtkinter.CTkOptionMenu(
          self, 
          values=["","chrome","Telegam","window file","brightness_up","brightness_down"],
        command=lambda value: self.update_gesture8(value))
        
        
        ges9 = Image.open("g9.png").convert('RGBA')
        ges9 = ges9.resize((94, 112))
        self.picges9 = ImageTk.PhotoImage(ges9)
        self.picges9_label1 = customtkinter.CTkLabel(self, image=self.picges9, text=None, width=100, height=10)
        
        
        self.opges9 = customtkinter.CTkOptionMenu(
          self, 
          values=["","chrome","Telegam","window file","brightness_up","brightness_down"],
        command=lambda value: self.update_gesture9(value))
        
        
        ges10 = Image.open("g10.png").convert('RGBA')
        ges10 = ges10.resize((80, 82))
        self.picges10 = ImageTk.PhotoImage(ges10)
        self.picges10_label1 = customtkinter.CTkLabel(self, image=self.picges10, text=None, width=100, height=10)
        
        
        self.opges10 = customtkinter.CTkOptionMenu(
          self, 
          values=["","chrome","Telegam","window file","brightness_up","brightness_down"],
        command=lambda value: self.update_gesture10(value))
        
        
        ges11 = Image.open("g11.png").convert('RGBA')
        ges11 = ges11.resize((82, 80))
        self.picges11 = ImageTk.PhotoImage(ges11)
        self.picges11_label1 = customtkinter.CTkLabel(self, image=self.picges11, text=None, width=100, height=10)
        
        
        self.opges11 = customtkinter.CTkOptionMenu(
          self, 
          values=["","right","left","switch_onglet","switch_tab","screenshot"],
        command=lambda value: self.update_gesture11(value))
        
        
        ges12 = Image.open("g12.png").convert('RGBA')
        ges12 = ges12.resize((70, 93))
        self.picges12 = ImageTk.PhotoImage(ges12)
        self.picges12_label1 = customtkinter.CTkLabel(self, image=self.picges12, text=None, width=100, height=10)
        
        
        self.opges12 = customtkinter.CTkOptionMenu(
          self, 
          values=["","right","left","switch_onglet","switch_tab","screenshot"],
        command=lambda value: self.update_gesture12(value))
        
        
        ges13 = Image.open("g13.png").convert('RGBA')
        ges13 = ges13.resize((50, 87))
        self.picges13 = ImageTk.PhotoImage(ges13)
        self.picges13_label1 = customtkinter.CTkLabel(self, image=self.picges13, text=None, width=100, height=10)
        
        
        self.opges13 = customtkinter.CTkOptionMenu(
          self, 
          values=["","right","left","switch_onglet","switch_tab","screenshot"],
        command=lambda value: self.update_gesture13(value))
        
        
        ges14 = Image.open("g14.png").convert('RGBA')
        ges14 = ges14.resize((85, 88))
        self.picges14 = ImageTk.PhotoImage(ges14)
        self.picges14_label1 = customtkinter.CTkLabel(self, image=self.picges14, text=None, width=100, height=10)
        
        
        self.opges14 = customtkinter.CTkOptionMenu(
          self, 
          values=["","right","left","switch_onglet","switch_tab","screenshot"],
        command=lambda value: self.update_gesture14(value))
        
        
        ges15 = Image.open("g15.png").convert('RGBA')
        ges15 = ges15.resize((100, 97))
        self.picges15 = ImageTk.PhotoImage(ges15)
        self.picges15_label1 = customtkinter.CTkLabel(self, image=self.picges15, text=None, width=100, height=10)
        
        
        self.opges15 = customtkinter.CTkOptionMenu(
          self, 
          values=["","right","left","switch_onglet","switch_tab","screenshot"],
        command=lambda value: self.update_gesture15(value))
        
        
        ges16 = Image.open("g16.png").convert('RGBA')
        ges16 = ges16.resize((100, 97))
        self.picges16 = ImageTk.PhotoImage(ges16)
        self.picges16_label1 = customtkinter.CTkLabel(self, image=self.picges16, text=None, width=100, height=10)
        
        
        self.opges16 = customtkinter.CTkOptionMenu(
          self, 
          values=["","media_pause","copy","paste","undo","ondo"],
        command=lambda value: self.update_gesture16(value))
        
        
        ges17 = Image.open("g17.png").convert('RGBA')
        ges17 = ges17.resize((85, 83))
        self.picges17 = ImageTk.PhotoImage(ges17)
        self.picges17_label1 = customtkinter.CTkLabel(self, image=self.picges17, text=None, width=100, height=10)
        
        
        self.opges17 = customtkinter.CTkOptionMenu(
          self, 
          values=["","media_pause","copy","paste","undo","ondo"],
        command=lambda value: self.update_gesture17(value))
        
        
        ges18 = Image.open("g18.png").convert('RGBA')
        ges18 = ges18.resize((69, 66))
        self.picges18 = ImageTk.PhotoImage(ges18)
        self.picges18_label1 = customtkinter.CTkLabel(self, image=self.picges18, text=None, width=100, height=10)
        
        
        self.opges18 = customtkinter.CTkOptionMenu(
          self, 
          values=["","select_all","save","zoom_in","zoom_out"],
        command=lambda value: self.update_gesture18(value))
        
        
        ges19 = Image.open("g19.png").convert('RGBA')
        ges19 = ges19.resize((80, 82))
        self.picges19 = ImageTk.PhotoImage(ges19)
        self.picges19_label1 = customtkinter.CTkLabel(self, image=self.picges19, text=None, width=100, height=10)
        
        
        self.opges19 = customtkinter.CTkOptionMenu(
          self, 
          values=["","select_all","save","zoom_in","zoom_out"],
        command=lambda value: self.update_gesture19(value))
        
        
        ges20 = Image.open("g20.png").convert('RGBA')
        ges20 = ges20.resize((82, 80))
        self.picges20 = ImageTk.PhotoImage(ges20)
        self.picges20_label1 = customtkinter.CTkLabel(self, image=self.picges20, text=None, width=100, height=10)
        
        
        self.opges20 = customtkinter.CTkOptionMenu(
          self, 
          values=["","select_all","save","zoom_in","zoom_out"],
        command=lambda value: self.update_gesture20(value))
        
        
        # Initialize the video capture object to capture video from the default camera (0)
        self.capture = cv2.VideoCapture(0)
        # Set the width and height of the video feed to the current width and height of the capture object
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Initialize the Hands object from the MediaPipe Hands library with minimum detection and tracking confidence set to 0.8
        self.hands=mp_hands.Hands(
        min_detection_confidence=0.8,
        min_tracking_confidence=0.8)
        # Call the update_video_feed function to start processing video frames
        self.update_video_feed()
        
    
    x,y=autopy.screen.size() 
    cv2.namedWindow("Webcam Feed", cv2.WINDOW_NORMAL)  # Create a resizable window to show the webcam feed
    cv2.setWindowProperty("Webcam Feed", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN) # Set the window to fullscreen
    cv2.setWindowProperty("Webcam Feed", cv2.WND_PROP_AUTOSIZE, cv2.WINDOW_NORMAL) # Set the window to not resize automatically
    cv2.resizeWindow("Webcam Feed", 180, 100) # Set the window size to 180x100
    cv2.setWindowProperty("Webcam Feed", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN) # Set the window to fullscreen
    cv2.moveWindow("Webcam Feed", 0-180, 0-100) # Set the window position to (0, 500)    
    cv2.setWindowProperty("Webcam Feed", cv2.WND_PROP_TOPMOST, 1) # Set the window always on top
    cv2.setWindowProperty("Webcam Feed", cv2.WND_PROP_TOPMOST, 1) # Set the window always on top
    def update_video_feed(self):
        global pTime
        global notification_shown 
        global notif
        global L_prev
        global has_executed
        global mode
        global active,cl,ac
        global pX, pY, cX, cY
        global wScr, hScr
        global right
        global start_time 
        global threshold
        global scroll_start_time
        global SCROLL_DURATION
        global k,n,b
        global close_mode_active
        global time1
        global pausenotif
        global scaled_landmarks
        global resumenotif
        # Define helper functions to put text on the image
        def putText(mode, loc=(250, 70), color=(0, 100,255)):
            cv2.putText(cv2image, str(mode), loc, cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, color, 3)
        def putText1(mode, loc=(100, 90), color=(255, 100,0)):
            cv2.putText(cv2image1, str(mode), loc, cv2.FONT_HERSHEY_COMPLEX_SMALL, 5, color, 3)
        
        # Capture a frame from the video feed      
        success, img = self.capture.read()
        # If preprocess_enabled is True, preprocess the frame using a function named preprocess_image
       
        
        if self.preprocessing_enabled:
            cv2image = self.preprocess_image(img)
            cv2image = cv2.cvtColor(cv2image, cv2.COLOR_GRAY2RGB)
        else:
            
            cv2image=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            

        # Create a copy of the RGB frame
        cv2image2=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        cv2image1=cv2.cvtColor(cv2image2,cv2.COLOR_BGR2RGB)
        
        # Use MediaPipe Hands library to detect landmarks on the hands in the frame
        results =self.hands.process(cv2image)
        # Create an empty list to store the landmark information
        landmarkList = []
        fingers = []
        finger=[]
        scaled_landmarks = {}
       
        # If there are multiple hands detected in the frame, loop through them
        if results.multi_hand_landmarks and self.st==1:
        
            for hand in results.multi_hand_landmarks:
                scaled_landmarks = {}
                for index, landmark in enumerate(hand.landmark):
                    mp_drawing.draw_landmarks(
                        cv2image,
                        hand,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2),
                        mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=1),
                    )
                    
                    mp_drawing.draw_landmarks(
                        cv2image1,
                        hand,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2),
                        mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=1),
                    )
                    
                 
                    
                    h, w, c = cv2image.shape  
                    # Calculate the center of the landmark in the image
                    centerX, centerY = int(landmark.x * w), int(landmark.y * h) 
                    scaled_landmarks[index]= (int(landmark.x * w), int(landmark.y * h) )
                    # Append the landmark information to the landmark list
                    landmarkList.append([index, centerX, centerY])
                
        lmList=landmarkList
        lm=scaled_landmarks
        #print('scale:',lm)
        if(scaled_landmarks!={}) and self.custom :
                    
                    point4 = scaled_landmarks[KEY_POINTS[1]]
                    point8 = scaled_landmarks[KEY_POINTS[3]]
                    point0 = scaled_landmarks[KEY_POINTS[0]]
                    point5 = scaled_landmarks[KEY_POINTS[2]]
                    point6 = scaled_landmarks[KEY_POINTS[9]]
                    point3 = scaled_landmarks[KEY_POINTS[7]]
                    point9 = scaled_landmarks[KEY_POINTS[8]]
                    point12 = scaled_landmarks[KEY_POINTS[4]]
                    point10 = scaled_landmarks[KEY_POINTS[10]]
                    point16 = scaled_landmarks[KEY_POINTS[5]]
                    point14 = scaled_landmarks[KEY_POINTS[11]]
                    point20 = scaled_landmarks[KEY_POINTS[6]]
                    point18 = scaled_landmarks[KEY_POINTS[12]]

                    distance_0_8 = math.sqrt((point0[0] - point8[0]) ** 2 + (point0[1] - point8[1]) ** 2)
                    distance_0_6 = math.sqrt((point0[0] - point6[0]) ** 2 + (point0[1] - point6[1]) ** 2)

                    distance_4_8 = math.sqrt((point4[0] - point8[0]) ** 2 + (point4[1] - point8[1]) ** 2)

                    distance_0_3 = math.sqrt((point0[0] - point3[0]) ** 2 + (point0[1] - point3[1]) ** 2)
                    distance_0_4 = math.sqrt((point0[0] - point4[0]) ** 2 + (point0[1] - point4[1]) ** 2)

                    distance_4_5 = math.sqrt((point4[0] - point5[0]) ** 2 + (point4[1] - point5[1]) ** 2)
                    distance_5_9 = math.sqrt((point5[0] - point9[0]) ** 2 + (point5[1] - point9[1]) ** 2)

                    distance_0_12 = math.sqrt((point0[0] - point12[0]) ** 2 + (point0[1] - point12[1]) ** 2)
                    distance_0_10 = math.sqrt((point0[0] - point10[0]) ** 2 + (point0[1] - point10[1]) ** 2)

                    distance_0_16 = math.sqrt((point0[0] - point16[0]) ** 2 + (point0[1] - point16[1]) ** 2)
                    distance_0_14 = math.sqrt((point0[0] - point14[0]) ** 2 + (point0[1] - point14[1]) ** 2)

                    distance_0_20 = math.sqrt((point0[0] - point20[0]) ** 2 + (point0[1] - point20[1]) ** 2)
                    distance_0_18 = math.sqrt((point0[0] - point18[0]) ** 2 + (point0[1] - point18[1]) ** 2)
                    
                    
                    angle = 0
                    angle = math.atan2(point0[1] - point12[1], point0[0] - point12[0]) 
                    angle = np.degrees(angle) - 90

                    angle = str(angle)
                    finger=[str(distance_0_4/distance_0_3),str(distance_4_5/distance_5_9),str(distance_0_8/distance_0_6)
                            ,str(distance_0_12/distance_0_10),str(distance_0_16/distance_0_14),
                            str(distance_0_20/distance_0_18),angle
                            ]  
                   
                   
                    # Use the loaded model to make predictions on the new data
                    y_pred = model.predict([finger])

                    # Print the predicted results
                    #print(y_pred)
                    mode= 'Gesture'+str(y_pred)
                    putText(mode, loc=(200, 70), color=(0, 100,255))
                    #action=[md.volume2(cv2image, lmList, fingers, color, volume, volRange, minVol, maxVol)]
                    gestt=[self.gest1,self.gest2,self.gest3,self.gest4,self.gest5,self.gest6,self.gest7,
                          self.gest8,self.gest9,self.gest10,self.gest11,self.gest12,self.gest13,self.gest14,
                          self.gest15,self.gest16,self.gest17,self.gest18,self.gest19,self.gest20]
                    for i in range (1,20):
                        
                        if gestt[i-1] == 'volume' and y_pred  == [i-1]:
                            md.volume2(cv2image, lmList, fingers, color, volume, volRange, minVol, maxVol)
                        
                        if gestt[i-1] == 'VLC' and y_pred == [i-1]:
                            # Replace the path with the actual path to VLC executable file on your computer
                            vlc_path = "C:/Program Files/VideoLAN/VLC/vlc.exe"
                            # Open VLC media player
                            os.startfile(vlc_path)
                            time.sleep(0.5)
                            
                        if gestt[i-1] == 'Chrome' and y_pred == [i-1]:
                            # Replace the path with the actual path to VLC executable file on your computer
                            Chrome_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"
                            # Open VLC media player
                            os.startfile(Chrome_path)  
                            time.sleep(0.5)
                            
                        if gestt[i-1] == 'Telegram' and y_pred == [i-1]:
                            # Replace the path with the actual path to VLC executable file on your computer
                            Telegram_path = "C:/Users/win10/AppData/Roaming/Telegram Desktop/Telegram.exe"
                            # Open Telegram
                            os.startfile(Telegram_path)  
                            time.sleep(0.5)
                            
                        if gestt[i-1] == 'window file' and y_pred == [i-1]:
                            os.startfile(os.getcwd())
                            time.sleep(0.5)
                            
                        if gestt[i-1] == 'scroll_up' and y_pred == [i-1]:
                            def simulate_hotkey():
                                pyautogui.hotkey('up')
                            thread = threading.Thread(target=simulate_hotkey)
                            thread.start()
                            time.sleep(0.5)
                            
                        if gestt[i-1] == 'scroll_down' and y_pred == [i-1]:
                            def simulate_hotkey():
                                pyautogui.hotkey('down')
                            thread = threading.Thread(target=simulate_hotkey)
                            thread.start()
                            
                        if gestt[i-1] == 'brightness_up' and y_pred == [i-1]:
                            def simulate_hotkey():
                                pyautogui.hotkey('win', 'up')
                            thread = threading.Thread(target=simulate_hotkey)
                            thread.start()
                        
                        if gestt[i-1] == 'brightness_down' and y_pred == [i-1]:
                            def simulate_hotkey():
                                pyautogui.hotkey('win', 'down')
                            thread = threading.Thread(target=simulate_hotkey)
                            thread.start()
                        
                        if gestt[i-1] == 'right' and y_pred == [i-1]:
                            def simulate_hotkey():
                                pyautogui.hotkey( 'right')
                            thread = threading.Thread(target=simulate_hotkey)
                            thread.start()
                        
                        if gestt[i-1] == 'left' and y_pred == [i-1]:
                            def simulate_hotkey():
                                pyautogui.hotkey( 'left')
                            thread = threading.Thread(target=simulate_hotkey)
                            thread.start()
                            
                        if gestt[i-1] == 'screenshot' and y_pred == [i-1]:
                            thread = threading.Thread(target=md.take_screenshots(cv2image, lmList, fingers))
                            thread.start()
                            time.sleep(0.5)
                            
                        if gestt[i-1] == 'switch_onglet' and y_pred == [i-1]:
                            def simulate_hotkey():
                                pyautogui.hotkey('ctrl', 'tab')
                            thread = threading.Thread(target=simulate_hotkey)
                            thread.start()
                            time.sleep(0.5)
                            
                        if gestt[i-1] == 'switch_tab' and y_pred == [i-1]:
                            def simulate_hotkey():
                                pyautogui.hotkey('Alt', 'tab')
                            thread = threading.Thread(target=simulate_hotkey)
                            thread.start()
                            time.sleep(0.5)
                            
                        if gestt[i-1] == 'media_pause' and y_pred == [i-1]:
                            def simulate_hotkey():
                                pyautogui.hotkey('space')
                            thread = threading.Thread(target=simulate_hotkey)
                            thread.start()
                            time.sleep(0.5)
                            
                        if gestt[i-1] == 'copy' and y_pred == [i-1]:
                            def simulate_hotkey():
                                pyautogui.hotkey('ctrl', 'c')
                            thread = threading.Thread(target=simulate_hotkey)
                            thread.start()   
                            time.sleep(0.5)
                            
                        if gestt[i-1] == 'paste' and y_pred == [i-1]:
                            def simulate_hotkey():
                                pyautogui.hotkey('ctrl', 'v')
                            thread = threading.Thread(target=simulate_hotkey)
                            thread.start()
                            time.sleep(0.5)
                            
                        if gestt[i-1] == 'undo' and y_pred == [i-1]:
                            def simulate_hotkey():
                                pyautogui.hotkey('ctrl', 'z')
                            thread = threading.Thread(target=simulate_hotkey)
                            thread.start()
                            time.sleep(0.5)
                            
                        if gestt[i-1] == 'ondo' and y_pred == [i-1]:
                            def simulate_hotkey():
                                pyautogui.hotkey('ctrl', 'y')
                            thread = threading.Thread(target=simulate_hotkey)
                            thread.start()
                        
                        if gestt[i-1] == 'save' and y_pred == [i-1]:
                            def simulate_hotkey():
                                pyautogui.hotkey('ctrl', 's')
                            thread = threading.Thread(target=simulate_hotkey)
                            thread.start()
                            time.sleep(0.5)
                            
                        if gestt[i-1] == 'select_all' and y_pred == [i-1]:
                            def simulate_hotkey():
                                pyautogui.hotkey('ctrl', 'a')
                            thread = threading.Thread(target=simulate_hotkey)
                            thread.start()
                            time.sleep(0.5)
                            
                        if gestt[i-1] == 'zoom_in' and y_pred == [i-1]:
                            def simulate_hotkey():
                                pyautogui.hotkey('ctrl', '+')
                            thread = threading.Thread(target=simulate_hotkey)
                            thread.start()
                            time.sleep(0.5)
                            
                        if gestt[i-1] == 'zoom_out' and y_pred == [i-1]:
                            def simulate_hotkey():
                                pyautogui.hotkey('ctrl', '-')
                            thread = threading.Thread(target=simulate_hotkey)
                            thread.start()
                            time.sleep(0.5)
                            
        if len(lmList) != 0 and not(self.custom):
            if not notification_shown:
            
                def show_notification():
                    title = 'Hand Detection'
                    message = 'Your hand is detected'

                    notification.notify(
                        title=title,
                        message=message,
                        app_name='APP',
                        timeout=0
                    )
                thread = threading.Thread(target=show_notification)
                thread.start()
                # set the flag to True
                notification_shown = True
                notif = False
            
            point4 = lmList[4]
            point8 = lmList[8]
            point0 = lmList[0]
            point5 = lmList[5]
            point6 = lmList[6]
            point3 = lmList[3]
            point9 = lmList[9]
            point12 = lmList[12]
            point10 = lmList[10]
            point16 = lmList[16]
            point14 = lmList[14]
            point20 = lmList[20]
            point18 = lmList[18]
          
            distance_0_3 = math.sqrt((point0[1] - point3[1]) ** 2 + (point0[2] - point3[2]) ** 2)
            distance_0_4 = math.sqrt((point0[1] - point4[1]) ** 2 + (point0[2] - point4[2]) ** 2)

            distance_4_5 = math.sqrt((point4[1] - point5[1]) ** 2 + (point4[2] - point5[2]) ** 2)
            distance_5_9 = math.sqrt((point5[1] - point9[1]) ** 2 + (point5[2] - point9[2]) ** 2)
            if(distance_0_3 != 0) and (distance_5_9 != 0)   :
                if(distance_0_4/distance_0_3)<=1 or (distance_4_5/distance_5_9)<=1:
                    fingers.append(0)
                elif (distance_0_4/distance_0_3)>1 or (distance_4_5/distance_5_9)>1:
                    fingers.append(1)
            
            distance_0_8 = math.sqrt((point0[1] - point8[1]) ** 2 + (point0[2] - point8[2]) ** 2)
            distance_0_6 = math.sqrt((point0[1] - point6[1]) ** 2 + (point0[2] - point6[2]) ** 2)
            if(distance_0_6 != 0)  :
                if(distance_0_8/distance_0_6)<1:
                    fingers.append(0)
                else:
                    fingers.append(1)
                    
            distance_0_12 = math.sqrt((point0[1] - point12[1]) ** 2 + (point0[2] - point12[2]) ** 2)
            distance_0_10 = math.sqrt((point0[1] - point10[1]) ** 2 + (point0[2] - point10[2]) ** 2)
            if(distance_0_10 != 0)  :
                if(distance_0_12/distance_0_10)<1:
                    fingers.append(0)
                else:
                    fingers.append(1)
                    
            distance_0_16 = math.sqrt((point0[1] - point16[1]) ** 2 + (point0[2] - point16[2]) ** 2)
            distance_0_14 = math.sqrt((point0[1] - point14[1]) ** 2 + (point0[2] - point14[2]) ** 2)
            if(distance_0_14 != 0)  :
                if(distance_0_16/distance_0_14)<1:
                    fingers.append(0)
                else:
                    fingers.append(1)
                    
            distance_0_20 = math.sqrt((point0[1] - point20[1]) ** 2 + (point0[2] - point20[2]) ** 2)
            distance_0_18 = math.sqrt((point0[1] - point18[1]) ** 2 + (point0[2] - point18[2]) ** 2)            
            if(distance_0_18 != 0)  :
                if(distance_0_20/distance_0_18)<1:
                    fingers.append(0)
                else:
                    fingers.append(1)
            
            palm_center = np.array([l[1:] for l in lmList if l[0] == 0][0])
            middle_finger = np.array([l[1:] for l in lmList if l[0] == 9][0])
            # Calculate the angle between the palm center and the middle finger
            angle = np.arctan2(palm_center[1] - middle_finger[1], palm_center[0] - middle_finger[0])
            angle = np.degrees(angle) - 90
            # Draw the virtual x-axis
            length = 100
            end_point_x = int(palm_center[0] + length * np.cos(np.radians(angle)))
            end_point_y = int(palm_center[1] + length * np.sin(np.radians(angle)))
            #cv2.line(cv2image, (palm_center[0], palm_center[1]), (end_point_x, end_point_y), (0, 255, 255), 2)
            # Draw the virtual y-axis
            end_point_x = int(palm_center[0] + length * np.sin(np.radians(angle)))
            end_point_y = int(palm_center[1] - length * np.cos(np.radians(angle)))
            #cv2.line(cv2image, (palm_center[0], palm_center[1]), (end_point_x, end_point_y), (0, 255,255), 2)
            screen_center = (cv2image.shape[1]//2, cv2image.shape[0]//2)
            #cv2.line(cv2image, (screen_center[0], 0), (screen_center[0], cv2image.shape[0]), (0, 255, 0), 2)
            #cv2.line(cv2image, (0, screen_center[1]), (cv2image.shape[1], screen_center[1]), (0, 255, 0), 2)  
            # Draw the angle on the frame
            #cv2.putText(cv2image, f'Angle: {angle:.2f}', (40, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)           
            if (fingers == [0, 0, 0, 0, 0]) :    
                mode = 'None'
                putText(mode)
                putText1(mode)
            elif (fingers == [0, 1, 0, 0, 0] or fingers == [0, 1, 1, 0, 0]) and (active == 0) and (cl==0):
                # Set mode to 'Scroll'
                mode = 'Scroll'
                putText(mode)
                putText1(mode)
            elif (fingers == [1, 1, 1, 1, 1]) and (active == 0) and (cl==0) :      
                mode='Cursor' 
                putText(mode)
                putText1(mode)
            elif (fingers == [1, 1, 0, 0, 0]) and (active == 0) and (cl==0):
                # Set mode to 'Volume'
                mode = 'volume' 
                putText(mode)
                putText1(mode)
            elif (fingers == [1, 0, 0, 0, 1]) and (active == 0) and (cl==0) and (self.ac):
                # Set mode to 'Brightness'
                mode = 'brightness'
                putText('brightness')
                putText1(mode)
            elif (fingers == [0, 0, 0, 0, 1]) and (active == 0) and (cl==0):
                # Set mode to 'Screenshot'
                mode = 'Screenshot'
                putText('Screenshot')
                putText1(mode)
            elif (fingers == [1, 0,1,1,1]) and (active == 0) and (cl==0)   :
                # Set mode to 'close'
                mode = 'close'
                putText1(mode)
            elif (fingers == [1, 1, 1, 0, 0]) and (active == 0) and (cl==0):
                # Set mode to 'maxmin'
                mode = 'maxmin'
                putText1(mode)
            elif (fingers == [1, 1, 0, 0, 1]) and (active == 0) and (cl==0) and (self.close_pro):
                # Set mode to 'program'
                mode = 'program'
                putText1(mode)
            elif (fingers == [0, 1, 0, 0, 1] ) :
                # Set mode to 'pause'
                mode='pause'
                putText1(mode)
            elif (fingers == [1, 0, 0, 0, 0] ) :
                # Set mode to resume
                mode='resume'
                putText1(mode)
            elif (fingers == [1, 1, 1, 0, 1] ) :
                # Set mode to full screen
                mode='screen'
                putText1(mode)
        else:
            if not notif:
                def show_notification():
                    title = 'Hand Detection'
                    message = 'Your hand is not detected'

                    notification.notify(
                        title=title,
                        message=message,
                        app_name='APP',
                        timeout=0
                    )
                thread = threading.Thread(target=show_notification)
                thread.start()
                notif=True
                notification_shown = False       
        #cv2.rectangle(cv2image, (20, 40), (620, 400), (0,255,0), 3) 
        cv2.rectangle(cv2image, (20, 30), (620, 450), (128, 128, 128), 1)
        
        self.mod=mode
        if mode == 'None' :
            n=time.time()
            b=0
            #thread = threading.Thread(target=self.game)
            #thread.start()
            #t = threading.Thread(target=self.show_cube)
            #t.start()
            pausenotif=False
            resumenotif=False
        if mode == 'screen':
            putText(mode)
            time.sleep(0.3)
            def simulate_hotkey():
                pyautogui.hotkey('F5')

            thread = threading.Thread(target=simulate_hotkey)
            thread.start()
            n=time.time()
            b=0
            pausenotif=False
            resumenotif=False
        if mode == 'resume':
            #time.sleep(0.2)
            putText(mode)
            cl=0   
            print
            n=time.time()
            b=0
            if not resumenotif:
                def show_notification():
                            title = 'Resume Mode'
                            message = 'Resume mode is now active'

                            notification.notify(
                                title=title,
                                message=message,
                                app_name='APP',
                                timeout=1
                            )
                thread1 = threading.Thread(target=show_notification)
                thread1.start()
                resumenotif=True
            
            def simulate_hotkey():
                pyautogui.hotkey('left')

            thread = threading.Thread(target=simulate_hotkey)
            if self.ch==True:
                thread.start()
            self.ch=False
            pausenotif=False
        if mode == 'pause':
            time.sleep(0.2)
            putText(mode)
            cl=1  
            n=time.time()
            b=0
            
            if not pausenotif:
                def show_notification():
                       
                            title = 'Pause Mode'
                            message = 'Pause mode is now active'

                            notification.notify(
                                title=title,
                                message=message,
                                app_name='APP',
                                timeout=1
                            )
                    
                thread1 = threading.Thread(target=show_notification)
                thread1.start()
                pausenotif=True

                def simulate_hotkey():
                    pyautogui.hotkey('right')

                thread = threading.Thread(target=simulate_hotkey)
                thread.start()
            self.ch=True
            resumenotif=False
        if mode == 'program':
            time.sleep(0.3)
            putText(mode)
            pid = os.getpid()
            # Perform a task kill command to close the OpenCV process
            os.system(f"taskkill /pid {pid} /f")
            n=time.time()
            b=0
            
        if mode == 'maxmin':
            # Function to detect if two fingers are opening or closing
            if len(lmList) >= 5:
                L_prev =md.detect_finger_gesture(L_prev,lmList)
                putText(L_prev)
            n=time.time()
            b=0
            pausenotif=False
            resumenotif=False
        timing=time.time()
        if timing-time1>2:
            close_mode_active = False
            
        if mode == 'close' :
            putText(mode)
            time.sleep(0.3)
            time1=time.time()
            
            if  close_mode_active== False:
                def show_notification():
                    title = 'close mode'
                    message = 'show the gesture again to close the window'

                    notification.notify(
                                title=title,
                                message=message,
                                app_name='APP',
                                timeout=1
                            )
                thread1 = threading.Thread(target=show_notification)
                thread1.start()
            
                close_mode_active = not close_mode_active
            
            elif close_mode_active==True and timing-n<=2:
                close_mode_active = not close_mode_active
                def simulate_hotkey():
                    pyautogui.hotkey('Alt', 'F4')
                thread = threading.Thread(target=simulate_hotkey)

                thread.start()
           
            n=time.time()          
            b=0 
            pausenotif=False
            resumenotif=False
        if mode =='Screenshot':
            time.sleep(0.2)
            def show_notification():
                title = 'Screenshot'
                message = 'Screenshot is taken'

                notification.notify(
                                title=title,
                                message=message,
                                app_name='APP',
                                timeout=1
                            )
            thread = threading.Thread(target=show_notification)
            thread.start()
            
            screenshot_thread = threading.Thread(target=md.take_screenshots(cv2image, lmList, fingers))
            # Start the thread
            screenshot_thread.start()
            n=time.time()
            b=0
            pausenotif=False
            resumenotif=False
        if mode =='brightness':
            md.brightness(cv2image, lmList) 
            md.brightness(cv2image1, lmList)
            #print(k)
            n=time.time()
            b=0
            pausenotif=False
            resumenotif=False
        if mode =='volume':
            md.volume2(cv2image, lmList, fingers, color, volume, volRange, minVol, maxVol)
            md.volume2(cv2image1, lmList, fingers, color, volume, volRange, minVol, maxVol)
            n=time.time()
            b=0
            pausenotif=False
            resumenotif=False
        if mode=='Scroll':
            
            timing=time.time()
            print(timing-n)
          
            if  timing-n<1 and b==0:
                b=1
                thread = threading.Thread(target=md.scrollone(cv2image, lmList,fingers) )
                thread.start()
            elif timing-n>=1:
                thread = threading.Thread(target=md.scrollone(cv2image, lmList,fingers) )
                thread.start()
            pausenotif=False
            resumenotif=False
        if mode=='Cursor':
            
            
            b=0
            pausenotif=False
            resumenotif=False
            n=time.time()
            if fingers[1:] == [0,0,0,0]:
                # Set active flag to 0 and mode to 'N'
                active =0
                # Print the mode
                print(mode)
            else:
                # Check if there are any landmarks
                
                    if len(lmList) != 0:
                        
                        # Get x and y coordinate of the landmark
                        x1, y1 = lmList[8][1], lmList[8][2]
                        
                        # Get screen width and height
                        w, h = autopy.screen.size()
                        # Interpolate the x and y coordinate
                        x3 = np.interp(x1,( 100, 640 - 100), (0, wScr)) 
                        y3 = np.interp(y1, (100, 480 - 100), (0, hScr))  

                        # Calculate the current x and y coordinate
                        cX = pX + (x3 - pX) / (self.smooth)
                        cY = pY + (y3 - pY) / (self.smooth)
                        a=wScr-cX
                        if wScr - cX < 0:
                            cX = wScr
                        elif wScr - cX > wScr:
                            a= 0
                        if cY < 0:
                            cY = 0
                        elif cY > hScr:
                            cY = hScr
                        
                        # Move the mouse to the calculated coordinate
                        autopy.mouse.move(a, cY)  
                        
                        # Update previous x and y coordinate
                        pX, pY = cX, cY 
                        
                        
                        # Check if the thumb is not present
                        if len(fingers)==5:
                            
                            if fingers[0] == 0:
                                
                                # Draw a filled circle on the image
                                cv2.circle(cv2image, (lmList[4][1], lmList[4][2]), 10, (0, 0, 255), cv2.FILLED)
                                cv2.circle(cv2image1, (lmList[4][1], lmList[4][2]), 10, (0, 0, 255), cv2.FILLED)  
                                # Perform left click
                                mouse.click() 
                                #mouse.click() 
                                putText("Left click")
                                cv2.putText(cv2image1, "Left click", (20,430), cv2.FONT_HERSHEY_COMPLEX_SMALL, 5, (0,255,255), 3)
                            # Check if the little finger is not present
                            if fingers[4] == 0 :  
                                cv2.circle(cv2image, (lmList[20][1], lmList[20][2]), 10, (0, 0, 255), cv2.FILLED)
                                cv2.circle(cv2image1, (lmList[20][1], lmList[20][2]), 10, (0, 0, 255), cv2.FILLED)
                                # Perform right click
                                mouse.right_click()
                                putText("Right click")
                                cv2.putText(cv2image1, "Right click", (40,430), cv2.FONT_HERSHEY_COMPLEX_SMALL, 4, (0,255,255), 3)
                        else:
                            print("out of range 4")
                                
        resized = cv2.resize(cv2image, (0, 0), fx=0.5, fy=0.5)
        image = Image.fromarray(cv2image)
        image=image.resize((900,688))
        image = ImageTk.PhotoImage(image)
        
        x,y=autopy.screen.size() 
        cv2.namedWindow("Webcam Feed", cv2.WINDOW_NORMAL)  # Create a resizable window to show the webcam feed
        cv2.setWindowProperty("Webcam Feed", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN) # Set the window to fullscreen
        cv2.setWindowProperty("Webcam Feed", cv2.WND_PROP_AUTOSIZE, cv2.WINDOW_NORMAL) # Set the window to not resize automatically
        cv2.resizeWindow("Webcam Feed", 180, 100) # Set the window size to 180x100
        cv2.setWindowProperty("Webcam Feed", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN) # Set the window to fullscreen
        cv2.moveWindow("Webcam Feed", 0, int(y)-140) # Set the window position to (0, 500)
        #cv2.setWindowProperty("Webcam Feed", cv2.WND_PROP_TOPMOST, 1) # Set the window always on top
        cv2.imshow("Webcam Feed", cv2image1)  # Show the frame in the window
        
        # update video label with new image
        self.video_label.configure(image=image)
        self.video_label.image = image
        #print(mode)
        self.after(self.acc,self.update_video_feed)
        
        #print(self.mod)

    def star(self):
        self.st=1
    def stop(self):
        self.st=0
        
    def custom_enabled(self, option):
        if option == "enable":
            self.custom =  True
        elif option == "disable":
            self.custom =  False
            
    def update_gesture(self,option):
        self.ges = str(option)
    def update_gesture1(self,option):
        self.gest1 = str(option)    
    def update_gesture2(self,option):
        self.gest2 = str(option) 
    def update_gesture3(self,option):
        self.gest3 = str(option) 
    def update_gesture4(self,option):
        self.gest4 = str(option) 
    def update_gesture5(self,option):
        self.gest5 = str(option)
    def update_gesture6(self,option):
        self.gest6 = str(option)    
    def update_gesture7(self,option):
        self.gest7 = str(option) 
    def update_gesture8(self,option):
        self.gest8 = str(option) 
    def update_gesture9(self,option):
        self.gest9 = str(option) 
    def update_gesture10(self,option):
        self.gest10 = str(option)
    def update_gesture11(self,option):
        self.gest11 = str(option)       
    def update_gesture12(self,option):
        self.gest12 = str(option) 
    def update_gesture13(self,option):
        self.gest13 = str(option) 
    def update_gesture14(self,option):
        self.gest14 = str(option) 
    def update_gesture15(self,option):
        self.gest15 = str(option)
    def update_gesture16(self,option):
        self.gest16 = str(option)    
    def update_gesture17(self,option):
        self.gest17 = str(option) 
    def update_gesture18(self,option):
        self.gest18 = str(option) 
    def update_gesture19(self,option):
        self.gest19 = str(option) 
    def update_gesture20(self,option):
        self.ges20 = str(option)
          
       
        
    def update_preprocessing_enabled(self, option):
        if option == "enable":
            self.preprocessing_enabled = True
        elif option == "disable":
            self.preprocessing_enabled = False
       
    def preprocess_image(self,img):
        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Calculate the Laplacian and standard deviation of the grayscale image
        lap = cv2.Laplacian(gray, cv2.CV_64F)
        std = lap.std()
        # Check the standard deviation value
        if std < 50:
            # Apply histogram equalization to the grayscale image
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            equ = clahe.apply(gray)
        else:
            # Apply histogram stretching to the grayscale image
            min = np.min(gray)
            max = np.max(gray)
            equ = (gray - min) * 255 / (max - min)
        # Convert the equalized image back to color for display
        equ = cv2.cvtColor(equ, cv2.COLOR_GRAY2RGB)
        return gray
    
    def update_brightness(self, option):
        if option == "enable":
            self.ac = True
        elif option == "disable":
            self.ac = False
            
    def update_close(self, option):
        if option == "enable":
            self.close_pro = True
        elif option == "disable":
            self.close_pro = False   
    
    def update_accelerator(self, value):
        # update the smooth value to the selected value in the option menu
        self.acc = int(value)
        
    def update_smooth(self, value):
        # update the smooth value to the selected value in the option menu
        self.smooth = float(value)
        
    # define the different clicked methods for the menu       
    def clicked(self):
        
        # toggle the visibility of the picture frame
        self.picture_frame_visible = not self.picture_frame_visible
        # if the picture frame is hidden, show the video label and hide the sidebar frame
        if not(self.picture_frame_visible):
            self.video_label.grid(row=0, column=1, padx=50, pady=(10,70), sticky="nsew")
            self.sidebar_button1.place(x=550, y=650)
            self.sidebar_button2.place(x=850, y=650)
            self.sidebar_frame1.grid_forget()
        # if the picture frame is visible, show the sidebar frame and hide the video label
        else:
            self.sidebar_frame1.grid(row=0, column=1, rowspan=4, sticky="nsew")
            self.video_label.grid_forget()
            self.sidebar_button1.place_forget()
            self.sidebar_button2.place_forget()
        # hide all the picture labels, text boxes and other widgets that are not relevant when the picture frame is hidden
        self.picture_label.place_forget()
        self.picture_label1.place_forget()
        self.picture_label2.place_forget()
        self.picture_label3.place_forget()
        self.picture_label4.place_forget()
        self.picture_label5.place_forget()
        self.picture_label6.place_forget()
        self.picture_label7.place_forget()
        self.picture_label8.place_forget()
        self.picture_label9.place_forget()
        self.textbox.place_forget()
        self.smoothing_label.place_forget()
        self.accelerator.place_forget()
        self.accelerator1.place_forget()
        self.smoothing.place_forget()
        self.im1.place_forget()
        self.im0.place_forget()
        self.contrast.place_forget()
        self.contrast1.place_forget()
        self.brightness.place_forget()
        self.brightness1.place_forget()
        self.close1.place_forget()
        self.close.place_forget()
        self.custom1.place_forget()
        self.custom_button.place_forget()
        self.custom1.place_forget()
        self.custom_button.place_forget()
        self.picges1_label1.place_forget()
        self.opges1.place_forget()
        self.picges2_label1.place_forget()
        self.opges2.place_forget()
        self.picges3_label1.place_forget()
        self.opges3.place_forget()
        self.picges4_label1.place_forget()
        self.opges4.place_forget()
        self.picges5_label1.place_forget()
        self.opges5.place_forget()
        self.picges6_label1.place_forget()
        self.opges6.place_forget()
        self.picges7_label1.place_forget()
        self.opges7.place_forget()
        self.picges8_label1.place_forget()
        self.opges8.place_forget()
        self.picges9_label1.place_forget()
        self.opges9.place_forget()
        self.picges10_label1.place_forget()
        self.opges10.place_forget()
        self.picges11_label1.place_forget()
        self.opges11.place_forget()
        self.picges12_label1.place_forget()
        self.opges12.place_forget()
        self.picges13_label1.place_forget()
        self.opges13.place_forget()
        self.picges14_label1.place_forget()
        self.opges14.place_forget()
        self.picges15_label1.place_forget()
        self.opges15.place_forget()
        self.picges16_label1.place_forget()
        self.opges16.place_forget()
        self.picges17_label1.place_forget()
        self.opges17.place_forget()
        self.picges18_label1.place_forget()
        self.opges18.place_forget()
        self.picges19_label1.place_forget()
        self.opges19.place_forget()
        self.picges20_label1.place_forget()
        self.opges20.place_forget()  
    def clicked1(self):
       
            self.picture_label3.place_forget()
            self.picture_label1.place_forget()
            self.picture_label2.place_forget() 
            self.picture_label4.place_forget()
            self.picture_label5.place_forget()
            self.picture_label6.place_forget()
            self.picture_label7.place_forget()
            self.picture_label8.place_forget()
            self.picture_label9.place_forget()
            self.picture_label.place(x=250, y=80)
        
    def clicked2(self):
        
            self.picture_label3.place_forget()
            self.picture_label.place_forget()
            self.picture_label2.place_forget() 
            self.picture_label4.place_forget()
            self.picture_label5.place_forget()
            self.picture_label6.place_forget()
            self.picture_label7.place_forget()
            self.picture_label8.place_forget()
            self.picture_label9.place_forget()
            self.picture_label1.place(x=250, y=80)
       
    def clicked3(self):
        
            self.picture_label.place_forget()
            self.picture_label1.place_forget()
            self.picture_label3.place_forget()
            self.picture_label4.place_forget()
            self.picture_label5.place_forget()
            self.picture_label6.place_forget()
            self.picture_label7.place_forget()
            self.picture_label8.place_forget()
            self.picture_label9.place_forget()
            self.picture_label2.place(x=250, y=80)
            
    def clicked4(self):
        
            self.picture_label.place_forget()
            self.picture_label1.place_forget()
            self.picture_label2.place_forget()
            self.picture_label4.place_forget()
            self.picture_label5.place_forget()
            self.picture_label6.place_forget()
            self.picture_label7.place_forget()
            self.picture_label8.place_forget()
            self.picture_label9.place_forget()
            self.picture_label3.place(x=250, y=80)
            
    def clicked5(self):
        
            self.picture_label.place_forget()
            self.picture_label1.place_forget()
            self.picture_label2.place_forget() 
            self.picture_label3.place_forget()
            self.picture_label4.place(x=250, y=80) 
            self.picture_label5.place_forget()
            self.picture_label6.place_forget()
            self.picture_label7.place_forget()
            self.picture_label8.place_forget()
            self.picture_label9.place_forget()
    
    def clicked6(self):
        
            self.picture_label.place_forget()
            self.picture_label1.place_forget()
            self.picture_label2.place_forget() 
            self.picture_label3.place_forget()
            self.picture_label4.place_forget()
            self.picture_label6.place_forget()
            self.picture_label7.place_forget()
            self.picture_label8.place_forget()
            self.picture_label9.place_forget()
            self.picture_label5.place(x=250, y=80)
    
    def clicked7(self):
        
            self.picture_label.place_forget()
            self.picture_label1.place_forget()
            self.picture_label2.place_forget() 
            self.picture_label3.place_forget()
            self.picture_label4.place_forget()
            self.picture_label5.place_forget()
            self.picture_label7.place_forget()
            self.picture_label8.place_forget()
            self.picture_label9.place_forget()
            self.picture_label6.place(x=250, y=80)
    
    def clicked8(self):
        
            self.picture_label.place_forget()
            self.picture_label1.place_forget()
            self.picture_label2.place_forget() 
            self.picture_label3.place_forget()
            self.picture_label4.place_forget()
            self.picture_label5.place_forget()
            self.picture_label6.place_forget()
            self.picture_label8.place_forget()
            self.picture_label9.place_forget()
            self.picture_label7.place(x=250, y=80)
            
    def clicked9(self):
        
            self.picture_label.place_forget()
            self.picture_label1.place_forget()
            self.picture_label2.place_forget() 
            self.picture_label3.place_forget()
            self.picture_label4.place_forget()
            self.picture_label5.place_forget()
            self.picture_label6.place_forget()
            self.picture_label7.place_forget()
            self.picture_label9.place_forget()
            self.picture_label8.place(x=250, y=80)
            
    def clicked10(self):
        
            self.picture_label.place_forget()
            self.picture_label1.place_forget()
            self.picture_label2.place_forget() 
            self.picture_label3.place_forget()
            self.picture_label4.place_forget()
            self.picture_label5.place_forget()
            self.picture_label6.place_forget()
            self.picture_label7.place_forget()
            self.picture_label8.place_forget()
            self.picture_label9.place(x=250, y=80)
    
    def option(self): 
        
        self.visible = not self.visible
        if not(self.visible):
            self.video_label.grid(row=0, column=1, padx=50, pady=(10,70), sticky="nsew")
            self.sidebar_button1.place(x=550, y=650)
            self.sidebar_button2.place(x=850, y=650)
            self.picges1_label1.place_forget()
            self.opges1.place_forget()
            self.picges2_label1.place_forget()
            self.opges2.place_forget()
            self.picges3_label1.place_forget()
            self.opges3.place_forget()
            self.picges4_label1.place_forget()
            self.opges4.place_forget()
            self.picges5_label1.place_forget()
            self.opges5.place_forget()
            self.picges6_label1.place_forget()
            self.opges6.place_forget()
            self.picges7_label1.place_forget()
            self.opges7.place_forget()
            self.picges8_label1.place_forget()
            self.opges8.place_forget()
            self.picges9_label1.place_forget()
            self.opges9.place_forget()
            self.picges10_label1.place_forget()
            self.opges10.place_forget()
            self.picges11_label1.place_forget()
            self.opges11.place_forget()
            self.picges12_label1.place_forget()
            self.opges12.place_forget()
            self.picges13_label1.place_forget()
            self.opges13.place_forget()
            self.picges14_label1.place_forget()
            self.opges14.place_forget()
            self.picges15_label1.place_forget()
            self.opges15.place_forget()
            self.picges16_label1.place_forget()
            self.opges16.place_forget()
            self.picges17_label1.place_forget()
            self.opges17.place_forget()
            self.picges18_label1.place_forget()
            self.opges18.place_forget()
            self.picges19_label1.place_forget()
            self.opges19.place_forget()
            self.picges20_label1.place_forget()
            self.opges20.place_forget()
        else:
            self.video_label.grid_forget()
            self.sidebar_button1.place_forget()
            self.sidebar_button2.place_forget()
            self.picges1_label1.place(x=450, y=10)
            self.opges1.place(x=430, y=110)
            self.picges2_label1.place(x=630, y=35)
            self.opges2.place(x=610, y=110)
            self.picges3_label1.place(x=810, y=15)
            self.opges3.place(x=790, y=110)
            self.picges4_label1.place(x=990, y=12)
            self.opges4.place(x=970, y=110)
            self.picges5_label1.place(x=1170, y=10)
            self.opges5.place(x=1150, y=110)
            self.picges6_label1.place(x=450, y=170)
            self.opges6.place(x=430, y=250)
            self.picges7_label1.place(x=630, y=160)
            self.opges7.place(x=610, y=250)
            self.picges8_label1.place(x=810, y=143)
            self.opges8.place(x=790, y=250)
            self.picges9_label1.place(x=990, y=143)
            self.opges9.place(x=970, y=250)
            self.picges10_label1.place(x=1170, y=160)
            self.opges10.place(x=1150, y=250)
            self.picges11_label1.place(x=450, y=300)
            self.opges11.place(x=430, y=390)
            self.picges12_label1.place(x=630, y=290)
            self.opges12.place(x=610, y=390)
            self.picges13_label1.place(x=810, y=295)
            self.opges13.place(x=790, y=390)
            self.picges14_label1.place(x=990, y=295)
            self.opges14.place(x=970, y=390)
            self.picges15_label1.place(x=1170, y=290)
            self.opges15.place(x=1150, y=390)
            self.picges16_label1.place(x=450, y=430)
            self.opges16.place(x=430, y=530)
            self.picges17_label1.place(x=630, y=438)
            self.opges17.place(x=610, y=530)
            self.picges18_label1.place(x=810, y=455)
            self.opges18.place(x=790, y=530)
            self.picges19_label1.place(x=990, y=440)
            self.opges19.place(x=970, y=530)
            self.picges20_label1.place(x=1170, y=440)
            self.opges20.place(x=1150, y=530)
            
        self.smoothing_label.place(x=230, y=20) if (self.visible) else self.smoothing_label.place_forget()
        self.smoothing.place(x=230, y=50) if (self.visible) else self.smoothing.place_forget()
        self.accelerator.place(x=230, y=80) if (self.visible) else self.accelerator.place_forget()
        self.accelerator1.place(x=230, y=110) if (self.visible) else self.accelerator1.place_forget()
        self.custom1.place(x=230, y=320) if (self.visible) else self.custom1.place_forget()
        self.custom_button.place(x=230, y=350) if (self.visible) else self.custom_button.place_forget()
        self.picture_label1.place_forget()
        self.picture_label2.place_forget() 
        self.picture_label.place_forget()
        self.picture_label3.place_forget()
        self.picture_label4.place_forget()
        self.picture_label5.place_forget()
        self.picture_label6.place_forget()
        self.picture_label7.place_forget()
        self.picture_label8.place_forget()
        self.picture_label9.place_forget()
        self.sidebar_frame1.grid_forget()
        self.textbox.place_forget()
        self.im1.place_forget()
        self.im0.place_forget()
        self.contrast.place(x=230, y=140) if (self.visible) else self.contrast.place_forget()
        self.contrast1.place(x=230, y=170) if (self.visible) else self.contrast1.place_forget()
        self.brightness1.place(x=230, y=200) if (self.visible) else self.brightness1.place_forget()
        self.brightness.place(x=230, y=230) if (self.visible) else self.brightness.place_forget()
        self.close1.place(x=230, y=260) if (self.visible) else self.close1.place_forget()
        self.close.place(x=230, y=290) if (self.visible) else self.close.place_forget()
        
        
        
    def about(self): 
        
        self.visible1 = not self.visible1
        if self.visible1:
            self.textbox.place(x=230, y=30)
            self.im1.place(x=840, y=30)
            self.im0.place(x=840, y=270)
            self.video_label.grid_forget()
            self.sidebar_button1.place_forget()
            self.sidebar_button2.place_forget()
        else:
            self.textbox.place_forget()
            self.im1.place_forget()
            self.im0.place_forget()
            self.video_label.grid(row=0, column=1, padx=50, pady=(10,70), sticky="nsew")
            self.sidebar_button1.place(x=550, y=650)
            self.sidebar_button2.place(x=850, y=650)
        self.sidebar_frame1.grid_forget()
        self.accelerator.place_forget()
        self.picture_label1.place_forget()
        self.picture_label2.place_forget() 
        self.picture_label.place_forget()       
        self.picture_label3.place_forget()
        self.picture_label4.place_forget()
        self.picture_label5.place_forget()
        self.picture_label6.place_forget()
        self.picture_label7.place_forget()
        self.picture_label8.place_forget()
        self.picture_label9.place_forget()
        self.smoothing_label.place_forget()
        self.smoothing.place_forget()
        self.accelerator1.place_forget()
        self.contrast.place_forget()
        self.contrast1.place_forget()
        self.brightness.place_forget()
        self.brightness1.place_forget()
        self.close1.place_forget()
        self.close.place_forget()
        self.custom1.place_forget()
        self.custom_button.place_forget()
        self.picges1_label1.place_forget()
        self.opges1.place_forget()
        self.picges2_label1.place_forget()
        self.opges2.place_forget()
        self.picges3_label1.place_forget()
        self.opges3.place_forget()
        self.picges4_label1.place_forget()
        self.opges4.place_forget()
        self.picges5_label1.place_forget()
        self.opges5.place_forget()
        self.picges6_label1.place_forget()
        self.opges6.place_forget()
        self.picges7_label1.place_forget()
        self.opges7.place_forget()
        self.picges8_label1.place_forget()
        self.opges8.place_forget()
        self.picges9_label1.place_forget()
        self.opges9.place_forget()
        self.picges10_label1.place_forget()
        self.opges10.place_forget()
        self.picges11_label1.place_forget()
        self.opges11.place_forget()
        self.picges12_label1.place_forget()
        self.opges12.place_forget()
        self.picges13_label1.place_forget()
        self.opges13.place_forget()
        self.picges14_label1.place_forget()
        self.opges14.place_forget()
        self.picges15_label1.place_forget()
        self.opges15.place_forget()
        self.picges16_label1.place_forget()
        self.opges16.place_forget()
        self.picges17_label1.place_forget()
        self.opges17.place_forget()
        self.picges18_label1.place_forget()
        self.opges18.place_forget()
        self.picges19_label1.place_forget()
        self.opges19.place_forget()
        self.picges20_label1.place_forget()
        self.opges20.place_forget()                    
    def sidebar_button_event(self):
        print("sidebar_button click")
        
    # This function changes the appearance mode of the customtkinter library based on the new_appearance_mode input    
    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)
        if new_appearance_mode == "Dark" :
            self.textc='white'
            self.hoverc=''#005e80'
        elif new_appearance_mode == "Light" :
            self.textc='black'
            self.hoverc='#e5e5ff'
        self.sidebar_button_1.configure(text_color=self.textc)
        self.sidebar_button_2.configure(text_color=self.textc)
        self.sidebar_button_3.configure(text_color=self.textc)
        self.sidebar_button_4.configure(text_color=self.textc)
        self.sidebar_button_5.configure(text_color=self.textc)
        self.sidebar_button_6.configure(text_color=self.textc)
        self.sidebar_button_7.configure(text_color=self.textc)
        self.sidebar_button_8.configure(text_color=self.textc)
        self.sidebar_button_9.configure(text_color=self.textc)
        self.sidebar_button_10.configure(text_color=self.textc)
        
        
        
    # This function changes the scaling of the widgets in the customtkinter library based on the new_scaling input
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
        
    # This function starts the game process
    def start_process(self):
        game_path = "game.exe"

        # Open VLC media player
        os.startfile(game_path)
        

# Instantiate an App object from the tkinter library
app = App() 
# Run the application mainloop to start the GUI
app.mainloop()
