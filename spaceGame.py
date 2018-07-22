import pygame as pg, random as r, sys, buttons as bt, classes as cls, time as t
from PIL import ImageFont



pg.init()

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
gray = (128, 128, 128)
menu_black = (16,16,16)
options_black = (33, 33, 33)


available_characters = list(map(chr, range(33, 126)))


display_width = 1600
display_height = 900
game_display = pg.display.set_mode((display_width, display_height))
pg.display.set_caption("spaceGame")
clock = pg.time.Clock()



shipInsideImg = pg.image.load('images/holderSpaceshipIn1.png')
shipOutsideImg = pg.image.load('images/holderSpaceshipOutSide1.png')

shipInsideW, shipInsideH = shipInsideImg.get_rect().size
shipOutsideW, shipOutsideH = shipOutsideImg.get_rect().size





def shipInside():
    game_display.fill(gray)
    game_display.blit(shipInsideImg, shipInsideImg_rect)

def shipOutside():
    game_display.fill(gray)
    game_display.blit(shipOutsideImg, shipOutsideImg_rect)

def changeMenu(menu_to_show):
    shipInside()
    pg.draw.rect(game_display, menu_black, menuLeft_rect) # left bar
    pg.draw.rect(game_display, menu_black, menuBot_rect) # bottom bar
    menu_options_btn.draw()

    if(menu_to_show == 'combat_menu'):
        pass
    elif(menu_to_show == 'change_name'):
        showChangeNameMenu()
    elif(menu_to_show == 'keep_options'):
        showOptions()

    else:
        showSidebarMenu()


def showSidebarMenu():
    name_label_custom.draw()

    menu_hp_bar.draw()
    menu_xp_bar.draw()

def showTravelMenu():
    menu_planet_btn.draw()

    menu_crew_btn.draw()

def showChangeNameMenu():  #TODO: REFINE WHERE WHAT DOES
    showSidebarMenu()
    input_name_rect.draw()
    input_name_label.draw()

    update()

    input_name_done = False
    new_ship_name = ''
    changeShipName(new_ship_name)
    input_name_label.draw()
    name_label_custom.draw()
    while not input_name_done:
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                input_name_done= True
                end_game.change_state(True)
            elif ev.type == pg.MOUSEBUTTONUP:
                mpos = pg.mouse.get_pos()
                if not input_name_rect.rect.collidepoint(mpos):
                    input_name_done = True
            elif ev.type == pg.KEYDOWN:
                if ev.key == pg.K_RETURN:
                    print('Actually Enter')
                    input_name_done = True
                elif ev.key == pg.K_BACKSPACE:
                    if len(new_ship_name) > 0:
                        new_ship_name = new_ship_name[:-1]
                elif ev.key == pg.K_DELETE:
                    new_ship_name = ''
                else:
                    text_font = ImageFont.truetype('arial.ttf', name_label_custom.size)
                    current_textW, current_textH = text_font.getsize(new_ship_name)
                    letterW, letterH = text_font.getsize(ev.unicode)

                    if current_textW + letterW < name_label_custom.rectW - (name_label_custom.rectW / 10):
                        new_ship_name += ev.unicode
                    else:
                        too_long_name_text = 'Name is too long!'
                        changeShipName(too_long_name_text)
                        input_name_label.draw()
                        name_label_custom.draw()
                        update()
                        t.sleep(0.5)
            changeShipName(new_ship_name)
        input_name_label.draw()
        name_label_custom.draw()
        update()






def changeShipName(new_ship_name):
    name_label_custom.change_text(new_ship_name)
    input_name_label.change_text(new_ship_name)



def showOptions():
    showSidebarMenu()
    pg.draw.rect(game_display, options_black, options_rect)
    options_quit_btn.draw()
    update()

    keep_options = True

    while keep_options:
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                end_game.change_state(True)

            elif ev.type == pg.MOUSEBUTTONUP:
                mpos = pg.mouse.get_pos()
                if ev.button == 1:
                    if options_quit_btn.rect.collidepoint(mpos):
                        end_game.change_state(True)
                        keep_options = False
                    elif not options_rect.collidepoint(mpos):
                        keep_options = False

def nextBar(prev_bar_x, prev_bar_W):
    next_bar_x = prev_bar_x + prev_bar_W + 80
    return next_bar_x



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

name_input_rectW = display_width / 2
name_input_rectH = display_height / 2
name_input_rectX = ((display_width - name_input_rectW) / 2)
name_input_rectY = ((display_height - name_input_rectH) / 2)




name_input_labelW = 500
name_input_labelH = 100
name_input_labelX = ((display_width - name_input_labelW) / 2)
name_input_labelY = ((display_height - name_input_labelH) / 2) + 100


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




name_label_custom = cls.custom_label_fix_pos_left(game_display, menuShipX, menuShipY, 250, 50, white, 'name_hold', menu_black, 'Arial', 25, True, False)

input_name_label = cls.custom_label_custom_pos_left(game_display, name_input_labelX, name_input_labelY, name_input_labelW, name_input_labelH, white, 'name_hold', menu_black, 'Arial', 50, True, False)
input_name_rect = cls.custom_label_custom_pos_center(game_display, name_input_rectX, name_input_rectY, name_input_rectW, name_input_rectH, menu_black, 'Input name', white, 'Arial', 60, True, False)


menu_radar_btn = cls.buttons(game_display, menuRadarX, menuRadarY, 250, 90, white, 'Radar', menu_black, 'Arial', 60, True, False)
menu_planet_btn = cls.buttons(game_display, menuPlanetsX, menuPlanetsY, 250, 90, white, 'Planets', menu_black, 'Arial', 60, True, False)


menu_crew_btn = cls.buttons(game_display, menuCrewX, menuCrewY, 400, 90, white, '"Crew"', menu_black, 'Arial', 60, True, False)
menu_options_btn = cls.buttons(game_display, menuOptionsX, menuOptionsY, 200, 45, white, 'Options', menu_black, 'Arial', 30, True, False)

options_quit_btn = cls.buttons(game_display, optionsQuitX, optionsQuitY, 250, 100, white, 'Quit', menu_black, 'Arial', 70, True, False)


shipInsideImg_rect = shipInsideImg.get_rect(topleft=(xIn,yIn))
shipOutsideImg_rect = shipOutsideImg.get_rect(topleft=(xOut,yOut))

prev_bar_y = menuShipY

menu_hp_bar = cls.menu_bar_max(game_display, menuShipX, menuShipY + 130, 200, 50, options_black, red, 200, 100, 'Health', white, 'Arial', 20, False, True)

menu_xp_bar = cls.menu_bar_no_lim(game_display, (menuShipX+ 0), menu_hp_bar.rectY + 130, 200, 50, options_black, green, 200, 100, 'Level Up!', 'XP', white, 'Arial', 20, False, True)

end_game = cls.global_var(False)





def startGame():

    end_game = False
    keep_options = False
    ship_name = ''
    shipInside()
    mainLoop()



def mainLoop():

    menu_to_show = ''


    while not end_game.state:
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                end_game.change_state(True)

            elif ev.type == pg.MOUSEBUTTONUP:
                mpos = pg.mouse.get_pos()
                if ev.button == 1:
                    if menu_options_btn.rect.collidepoint(mpos):
                        menu_to_show = 'keep_options'

                    elif name_label_custom.rect.collidepoint(mpos):
                        menu_to_show = 'change_name'

                    elif menu_hp_bar.background_bar.collidepoint(mpos):
                        menu_hp_bar.change_current_add(15)
                    elif menu_xp_bar.background_bar.collidepoint(mpos):
                        menu_xp_bar.change_current_add(15)

                    print(pg.mouse.get_pos())

                elif ev.button == 2:
                    if menu_hp_bar.background_bar.collidepoint(mpos):
                        menu_hp_bar.change_current_max()
                    elif menu_xp_bar.background_bar.collidepoint(mpos):
                        menu_xp_bar.change_current_max()

                elif ev.button == 3:
                    if menu_hp_bar.background_bar.collidepoint(mpos):
                        menu_hp_bar.change_current_sub(20)
                    elif menu_xp_bar.background_bar.collidepoint(mpos):
                        menu_xp_bar.change_current_sub(20)

                elif ev.button == 4:
                    if menu_hp_bar.background_bar.collidepoint(mpos):
                        menu_hp_bar.change_current_add(1)
                    elif menu_xp_bar.background_bar.collidepoint(mpos):
                        menu_xp_bar.change_current_add(1)
                    update()

                elif ev.button == 5:
                    if menu_hp_bar.background_bar.collidepoint(mpos):
                        menu_hp_bar.change_current_sub(1)
                    elif menu_xp_bar.background_bar.collidepoint(mpos):
                        menu_xp_bar.change_current_sub(1)
            update()
            changeMenu(menu_to_show)
            menu_to_show = ''
            changeMenu(menu_to_show)
        update()


def update():
    pg.display.update()
    clock.tick(60)
    


startGame()
pg.quit()

