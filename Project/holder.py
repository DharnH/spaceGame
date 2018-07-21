import pygame as pg, random as r, sys, buttons as bt, classes as cls
from PIL import ImageFont





pg.init()

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
gray = (128, 128, 128)
menuBlack = (16,16,16)
optionsBlack = (33, 33, 33)



available_characters = list(map(chr, range(33, 126)))

askName = False

if askName:
    ship_name = input('What is the name of your ship?')
else:
    ship_name = 'name_holder'



display_width = 1600
display_height = 900
gameDisplay = pg.display.set_mode((display_width, display_height))
pg.display.set_caption("spaceGame")
clock = pg.time.Clock()







shipInsideImg = pg.image.load('images/holderSpaceshipIn1.png')
shipOutsideImg = pg.image.load('images/holderSpaceshipOutSide1.png')

shipInsideW, shipInsideH = shipInsideImg.get_rect().size
shipOutsideW, shipOutsideH = shipOutsideImg.get_rect().size











def shipInside():
    gameDisplay.fill(gray)
    gameDisplay.blit(shipInsideImg, shipInsideImg_rect)

def shipOutside():
    gameDisplay.fill(gray)
    gameDisplay.blit(shipOutsideImg, shipOutsideImg_rect)

def showMenu():
    pg.draw.rect(gameDisplay, menuBlack, menuLeft_rect)
    pg.draw.rect(gameDisplay, menuBlack, menuBot_rect)


    name_label_custom.draw()
    menu_radar_btn.draw()
    menu_planet_btn.draw()

    menu_crew_btn.draw()
    menu_options_btn.draw()



def showOptions():
    pg.draw.rect(gameDisplay, optionsBlack, options_rect)
    options_quit_btn.draw()




 #  create menu items
xIn = ((display_width - shipInsideW) / 2)
yIn = ((display_height - shipInsideH) / 2)

xOut = ((display_width - shipOutsideW) / 2)
yOut = ((display_height - shipOutsideH) / 2)

menuWidth = display_width / 6
menuHeight = display_height / 5
menuLeftX = 0
menuLeftY = 0
menuBotX = 0
menuBotY = (display_height - menuHeight)

menuShipX = (display_width / 18) * .1
menuShipY = display_height / 30
menuRadarX = (display_width / 18) * .1
menuRadarY = display_height / 30 * 10
menuPlanetsX = (display_width / 18) * .1
menuPlanetsY = display_height / 30 * 19

menuStorageX = (display_width / 18) * 1
menuStorageY = display_height - ((display_height / 30) * 4)
menuCrewX = (display_width / 18) * 7
menuCrewY = display_height - ((display_height / 30) * 4)
menuOptionsX = (display_width / 50) * .5
menuOptionsY = display_height - (display_height / 30) * 2

optionsWidth = display_width / 5
optionsHeight = (display_height / 5) * 3
optionsX = ((display_width - optionsWidth) / 2)
optionsY = ((display_height - optionsHeight) / 2)
optionsQuitX = optionsX + ((optionsWidth / 10) * 1.15)
optionsQuitY = optionsY + ((optionsHeight / 10) * 7.5)



menuLeft_rect = pg.Rect(menuLeftX, menuLeftY, menuWidth, display_height)
menuBot_rect = pg.Rect(menuBotX, menuBotY, display_width, menuHeight)
options_rect = pg.Rect(optionsX, optionsY, optionsWidth, optionsHeight)




name_label_custom = cls.custom_label(gameDisplay, menuShipX, menuShipY, 240, 50, white, 'name_hold', menuBlack, 'Arial', 25, True, False)

menu_radar_btn = cls.buttons(gameDisplay, menuRadarX, menuRadarY, 250, 90, white, 'Radar', menuBlack, 'Arial', 60, True, False)
menu_planet_btn = cls.buttons(gameDisplay, menuPlanetsX, menuPlanetsY, 250, 90, white, 'Planets', menuBlack, 'Arial', 60, True, False)


menu_crew_btn = cls.buttons(gameDisplay, menuCrewX, menuCrewY, 400, 90, white, '"Crew"', menuBlack, 'Arial', 60, True, False)
menu_options_btn = cls.buttons(gameDisplay, menuOptionsX, menuOptionsY, 200, 45, white, 'Options', menuBlack, 'Arial', 30, True, False)

options_quit_btn = cls.buttons(gameDisplay, optionsQuitX, optionsQuitY, 250, 100, white, 'Quit', menuBlack, 'Arial', 70, True, False)


shipInsideImg_rect = shipInsideImg.get_rect(topleft=(xIn,yIn))
shipOutsideImg_rect = shipOutsideImg.get_rect(topleft=(xOut,yOut))




def startGame():

    end_game = False
    keep_options = False






    shipInside()
    mainLoop(end_game, gameDisplay, clock, keep_options, ship_name)



def mainLoop(end_game, gameDisplay, clock, keep_options, ship_name):

    while not end_game:
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                end_game = True

            elif ev.type == pg.MOUSEBUTTONUP:
                if ev.button == 1:
                    mX, mY = pg.mouse.get_pos()
                    if keep_options:
                        if options_quit_btn.rect.collidepoint(mX, mY):
                            end_game = True
                        elif not options_rect.collidepoint(mX, mY):
                            keep_options = False

                    elif menu_options_btn.rect.collidepoint(mX, mY):
                        keep_options = True
                        print("yes")

                    elif name_label_custom.rect.collidepoint(mX, mY):
                        input_name_done = False
                        new_ship_name = ''
                        while not input_name_done:
                            for ev in pg.event.get():
                                if ev.type == pg.QUIT:
                                    input_name_done= True
                                    end_game = True
                                elif ev.type == pg.KEYDOWN:
                                    if ev.key == pg.K_RETURN:
                                        print('Actually Enter')
                                        input_name_done = True
                                    elif ev.key == pg.K_BACKSPACE:
                                        if len(new_ship_name) > 0:
                                            new_ship_name = new_ship_name[:-1]
                                    else:
                                        #text_font = ImageFont.truetype(name_label_custom.font, name_label_custom.size)
                                        text_font = ImageFont.truetype('Arial', 25)
                                        if (text_font.getsize(new_ship_name) + text_font.getsize(ev.unicode)) < (name_label_custom.rectW - 20):
                                            new_ship_name += ev.unicode

                                    name_label_custom.change_text(new_ship_name)
                                    update(keep_options)





                print(pg.mouse.get_pos())
            update(keep_options)








def update(keep_options):
    shipInside()
    showMenu()
    if keep_options:
        showOptions()

    pg.display.update()
    clock.tick(60)



startGame()
pg.quit()

