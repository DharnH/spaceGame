import pygame, sys #import libraries
mainClock = pygame.time.Clock() #setup clock for fps control
from pygame.locals import * #more pygame setup
pygame.init() #even more pygame setup
screen = pygame.display.set_mode((100,100),0,32) #define your display
Button_Img = pygame.image.load('images/holderSpaceshipIn1.png') #load button image
Click = False #set the click state to false
while True: #game loop
    mx,my = pygame.mouse.get_pos() #get mouse position
    MouseRect = pygame.Rect(mx,my,2,2) #set up mouse rect for collision
    screen.fill((0,0,0)) #reset display by filling with black
    ButtonRect = pygame.Rect(5,5,20,20) #set up the button rect for collision
    if MouseRect.colliderect(ButtonRect): #test for mouse collision with button
        if Click == True: #check if the user just click
            print('Somebody clicked me! :D') #some sort of response to the click
    screen.blit(Button_Img,(5,5)) #display the button image
    Click = False #reset click value so the button response isn't spammed
    for event in pygame.event.get(): #loop through current input events
        if event.type == QUIT: #check if the user closed the window
            pygame.quit() #close pygame
            sys.exit() #close python process
        if event.type == MOUSEBUTTONDOWN: #check for mouse activity
            if event.button == 1: #check for left click
                Click = True #set click to true
    pygame.display.update() #update display
    mainClock.tick(40) #set the framerate to 40
