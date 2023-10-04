#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pygame
import sys
import random
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import wmi
def gam():
    pygame.init()

    # Set screen dimensions
    screen_width = 640
    screen_height = 480

    # Create screen
    screen = pygame.display.set_mode((1366.0 ,700.0))

    # Set caption
    pygame.display.set_caption("Pygame Events Example")

    # Set game loop condition
    running = True
    background_image = pygame.image.load('space.png')

    background_image1 = pygame.image.load('space.png')
    background_image2 = pygame.image.load('space.png')


    # Set initial positions for both images
    background_x1 = 0
    background_x2 = background_image1.get_width()

    # Set cube color
    cube_color = (255, 0, 0)

    # Set cube size
    cube_size = 50

    # Set initial cube position
    cube_x = 320 - cube_size // 2
    cube_y = 240 - cube_size // 2
    plane_image = pygame.image.load('B1.png')
    plane_image.set_colorkey((255, 255, 255))
    
    b2 = pygame.image.load('b2.png')
    b1 = pygame.image.load('b1.png')
    b3 = pygame.image.load('b3.png')
    b4 = pygame.image.load('b44.png')
    b5 = pygame.image.load('b5.png')
    b9 = pygame.image.load('b13.png')
    b6 = pygame.image.load('b33.png')
    b12= pygame.image.load('b12.png')
    b66= pygame.image.load('b66.png')
    
    
    
    # Get default audio device
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    # Get initial volume
    initial_volume = volume.GetMasterVolumeLevelScalar()

    # Initialize WMI interface
    wmi_interface = wmi.WMI(namespace='wmi')

    # Get initial brightness
    initial_brightness = wmi_interface.WmiMonitorBrightness()[0].CurrentBrightness

    # Set font and size
    font = pygame.font.Font(None, 36)
    font1= pygame.font.Font(None, 70)
    # Set text color
    text_color = (255, 255, 255)

    # Set box color
    box_color = (255, 255, 255)

    # Set box position and size
    box_x = 50
    box_y = 50
    box_width = 200
    box_height = 50

    text=''
    
    # Start game loop
    while running:
        
        # Render text to surface
        text_surface  = font.render(text, True, text_color)
        text_surface0 = font1.render(text, True, text_color)
        text_surface1 = font.render("Gesture", True, text_color)
        text_surface2 = font.render("Left click", True, text_color)
        text_surface3 = font.render("Cursor", True, text_color)
        text_surface4 = font.render("Up", True, text_color)
        text_surface5 = font.render("down", True, text_color)
        text_surface6 = font.render("Brightness", True, text_color)
        text_surface7 = font.render("Right click", True, text_color)
        text_surface8 = font.render("Volume", True, text_color)
        text_surface9 = font.render("Pause", True, text_color)
        text_surface10= font.render("Resume", True, text_color)
        # Get text size
        text_width, text_height = text_surface.get_size()
        # Calculate text position
        text_x = box_x + (box_width - text_width) // 2
        text_y = box_y + (box_height - text_height) // 2

        # Get events
        current_volume = volume.GetMasterVolumeLevelScalar()
        
        # Check if volume has changed
        if current_volume != initial_volume:
            print("Volume has changed:",int(current_volume*100))
            initial_volume = current_volume
            text="Volume:"+str(int(current_volume*100))
            cube_x=700
            cube_y=250
            plane_image = pygame.image.load('b33.png')
            plane_image = pygame.transform.scale(plane_image, (300, 300))

        # Get current brightness
        current_brightness = wmi_interface.WmiMonitorBrightness()[0].CurrentBrightness

        # Check if brightness has changed
        if current_brightness != initial_brightness:
            print("Brightness has changed",current_brightness)
            initial_brightness = current_brightness
            text="Brightness:"+str(current_brightness)
            cube_x=700
            cube_y=250
            plane_image = pygame.image.load('b5.png')
            plane_image = pygame.transform.scale(plane_image, (300, 300))
        for event in pygame.event.get():
            # Check if user wants to quit
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                        # Get mouse position and update cube position accordingly
                        x, y = event.pos
                        cube_x = x - cube_size // 2
                        cube_y = y - cube_size // 2
                        text="cursor"
                        plane_image = pygame.image.load('b1.png')
                        plane_image = pygame.transform.scale(plane_image, (150, 192))
            # Check if a key is pressed
            elif event.type == pygame.KEYDOWN:
                # Check which key was pressed
                cube_x=40
                cube_y=40
                if event.key == pygame.K_PRINTSCREEN and pygame.key.get_mods() & pygame.KMOD_LMETA:
                    print("Screenshot taken")
                    text="Screenshot taken"
                    
                elif event.key == pygame.K_F4 and (pygame.key.get_mods() & pygame.KMOD_LALT):
                    print("close mode")
                    
                elif event.key == pygame.K_a:
                    print("pause")
                    text="pause"
                    
                elif event.key == pygame.K_b:
                    print("resume")
                    text="resume"
                    cube_x=40
                    cube_y=40
                    
                elif event.key == pygame.K_F5:
                    print("screen")
                    text="screen"
                    
                elif event.key == pygame.K_UP:
                    print("Up arrow key pressed")
                    text="up"
                    cube_x=660
                    cube_y=250
                    plane_image = pygame.image.load('b3-.png')
                    
                elif event.key == pygame.K_DOWN:
                    print("Down arrow key pressed")
                    text="  down"
                    cube_x=780
                    cube_y=250
                    plane_image = pygame.image.load('b4.png')
                    plane_image = pygame.transform.scale(plane_image, (168, 300))
                    
                elif event.key == pygame.K_LEFT:
                    print("Left arrow key pressed")
                    text="resume"
                    cube_x=700
                    cube_y=250
                    plane_image = pygame.image.load('b66.png')
                    plane_image = pygame.transform.scale(plane_image, (300, 300))
                    
                elif event.key == pygame.K_RIGHT:
                    print("Right arrow key pressed")
                    text="pause"
                    cube_x=680
                    cube_y=250
                    plane_image = pygame.image.load('b12.png')
                    plane_image = pygame.transform.scale(plane_image, (300, 300))

            # Check if a mouse button is clicked
            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                # Check which button was clicked
                if event.button == 1:
                    cube_x=700
                    cube_y=250
                    print("Left mouse button clicked")
                    text="left click"
                    plane_image = pygame.image.load('b2.png')
                    plane_image = pygame.transform.scale(plane_image, (300, 300))
                    
                elif event.button == 3:
                    cube_x=750
                    cube_y=250
                    print("Right mouse button clicked")
                    text="right click"
                    plane_image = pygame.image.load('b13.png')
                    plane_image = pygame.transform.scale(plane_image, (300, 300))

        background_x1 -= 0.3
        background_x2 -= 0.3
        # Reset position of first image if it goes off-screen
        if background_x1 < -background_image1.get_width():
            background_x1 = background_image2.get_width()

        # Reset position of second image if it goes off-screen
        if background_x2 < -background_image2.get_width():
            background_x2 = background_image1.get_width()

        # Draw both images on screen
        screen.blit(background_image1, (background_x1, 0))
        screen.blit(background_image2, (background_x2, 0))

        # Set rectangle position and size
        rect_x = 20
        rect_y = 20
        rect_width = 400
        rect_height = 650

        
        # Set line color
        line_color = (255, 255, 255) # white

        # Set line start and end positions
        line_start_pos = (rect_x , rect_y + 70)
        line_end_pos = (rect_x + rect_width-1, rect_y + 70)

        line_start_pos1 = (rect_x , rect_y + 260)
        line_end_pos1 = (rect_x + rect_width-1, rect_y + 260)
        
        line_start_pos2 = (rect_x , rect_y + 450)
        line_end_pos2= (rect_x + rect_width-1, rect_y + 450)
        
        # Set line width
        line_width = 2
        
        # Set rectangle color
        rect_color = (255, 255, 255)

        # Draw rectangle with white border and transparent interior
        pygame.draw.rect(screen, rect_color, (rect_x, rect_y, rect_width, rect_height), 1)
        
        # Draw line
        pygame.draw.line(screen, line_color, line_start_pos, line_end_pos, line_width)
        pygame.draw.line(screen, line_color, line_start_pos1, line_end_pos1, line_width)
        pygame.draw.line(screen, line_color, line_start_pos2, line_end_pos2, line_width)
        
        #show images
        screen.blit(b2, (30 , 90)  )
        screen.blit(b1, (180, 95)  )
        screen.blit(b3, (260, 85)  )
        screen.blit(b4, (20 ,290)  )
        screen.blit(b5, (160,280)  )
        screen.blit(b9, (305,285)  )
        screen.blit(b6, (30 ,480)  )
        screen.blit(b12,(150,480)  )
        screen.blit(b66,(280,480)  )
        screen.blit(plane_image, (cube_x, cube_y))  
        
        # Draw text on screen
        screen.blit(text_surface0, (text_x+650, text_y+500))
        screen.blit(text_surface1, (170, 50))
        screen.blit(text_surface2, (50 , 245))
        screen.blit(text_surface3, (190, 245))
        screen.blit(text_surface4, (320, 245))
        screen.blit(text_surface5, (60 , 425))
        screen.blit(text_surface6, (145, 425))
        screen.blit(text_surface7, (290, 425))
        screen.blit(text_surface8, (60,  630))
        screen.blit(text_surface9, (190, 630))
        screen.blit(text_surface10,(310, 630))
        
        # Update screen
        pygame.display.update()

    # Quit Pygame
    pygame.quit()
gam()



