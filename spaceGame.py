import pygame as pg, random as r, sys, buttons as bt, classes as cls, time as t
from PIL import ImageFont
import global_var as gv, weapons as wp, menu, ship_state as ship, character_state as char, math_functions as mf



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





def return_center(start_point, rect_size, object_size):
    return start_point + ((rect_size - object_size) / 2)






def shipInside():
    game_display.blit(shipInsideImg, shipInsideImg_rect)

def shipOutside():
    game_display.blit(shipOutsideImg, shipOutsideImg_rect)


def showMenuTemplate():
    game_display.fill(gray)
    pg.draw.rect(game_display, menu_black, menuLeft_rect) # left bar
    pg.draw.rect(game_display, menu_black, menuBot_rect) # bottom bar


def showMenuBasics():
    showSidebarMenu()
    menu_travel_btn.draw()
    menu_combat_btn.draw()
    menu_options_btn.draw()




def changeBar(bar_to_show):

    if bar_to_show == 'combat_bar':
        showCombatBar()
    elif bar_to_show == 'travel_bar':
        pass


def showCombatBar():
    menu_combat_bar_run.draw()
    menu_combat_bar_attack.draw()




def changeMenu(menu_to_show):

    if menu_to_show == 'combat_menu':
        initCombat()
    elif menu_to_show == 'travel_menu':
        showTravelPlanetMenu()
    elif menu_to_show == 'change_name':
        showChangeNameMenu()
    elif menu_to_show == 'keep_options':
        showOptions()

    else:
        #shipInside()
        pass


def showSidebarMenu():
    name_label_custom.draw()
    menu_hp_bar.draw()
    menu_xp_bar.change_current_set(char.xp_current)
    menu_xp_bar.draw()

def showTravelBar():
    menu_planet_btn.draw()

    menu_crew_btn.draw()

def showChangeNameMenu():
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
                gv.end_game = True
            elif ev.type == pg.MOUSEBUTTONUP:
                mpos = pg.mouse.get_pos()
                if not input_name_rect.rect.collidepoint(mpos):
                    input_name_done = True
            elif ev.type == pg.KEYDOWN:
                if ev.key == pg.K_RETURN:
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




def showTravelPlanetMenu():

    planet_select_menuW = display_width - menuWidth
    planet_select_menuH = display_height - menuHeight
    planet_select_menuX = menuWidth
    planet_select_menuY = 0

    planet_select_menu_textY = 10


    planet_one_selectW = 210
    planet_one_selectH = 210
    planet_one_selectX = planet_select_menuX + 40
    planet_one_selectY = planet_select_menuY + 60

    planet_select_menu = cls.custom_label_custom_pos_custom_text_pos(game_display, planet_select_menuX, planet_select_menuY, planet_select_menuW, planet_select_menuH, options_black, 'Select planet', white, 'center', planet_select_menu_textY, 'Arial', 30, True, False)

    planet_one_select = cls.custom_label_custom_pos_custom_text_pos(game_display, planet_one_selectX, planet_one_selectY, planet_one_selectW, planet_one_selectH, white, 'Planet One', options_black, 'center', planet_select_menuY + 70, 'Arial', 30, True, False)
    planet_two_select = cls.custom_label_custom_pos_custom_text_pos(game_display, planet_one_selectX + 250, planet_one_selectY, planet_one_selectW, planet_one_selectH, white, 'Planet Two', options_black, 'center', planet_select_menuY + 70, 'Arial', 30, True, False)
    planet_three_select = cls.custom_label_custom_pos_custom_text_pos(game_display, planet_one_selectX + 500, planet_one_selectY, planet_one_selectW, planet_one_selectH, white, 'Planet Three', options_black, 'center', planet_select_menuY + 70, 'Arial', 30, True, False)
    planet_four_select = cls.custom_label_custom_pos_custom_text_pos(game_display, planet_one_selectX + 750, planet_one_selectY, planet_one_selectW, planet_one_selectH, white, 'Planet Four', options_black, 'center', planet_select_menuY + 70, 'Arial', 30, True, False)
    planet_five_select = cls.custom_label_custom_pos_custom_text_pos(game_display, planet_one_selectX + 1000, planet_one_selectY, planet_one_selectW, planet_one_selectH, white, 'Planet Five', options_black, 'center', planet_select_menuY + 70, 'Arial', 30, True, False)


    planet_selected = False


    while not planet_selected and not gv.end_game:
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                gv.end_game = True
                planet_selected = True

            elif ev.type == pg.MOUSEBUTTONUP:
                mpos = pg.mouse.get_pos()
                if ev.button == 1:
                    if menu_options_btn.rect.collidepoint(mpos):
                        changeMenu('keep_options')
                        planet_selected = True

                    elif menu_travel_btn.rect.collidepoint(mpos):
                        planet_selected = True
                        
                    elif planet_one_select.rect.collidepoint(mpos):
                        showTravelStationMenu(cls.planet_one_stations)

                    elif planet_two_select.rect.collidepoint(mpos):
                        ship.health_max += 10
                        menu_hp_bar.change_max_set(ship.health_max)

                    elif planet_three_select.rect.collidepoint(mpos):
                        ship.health_current -= 10
                        menu_hp_bar.change_current_set(ship.health_current)

                    elif planet_four_select.rect.collidepoint(mpos):
                        ship.test_run()
                        
                        

        planet_select_menu.draw()
        planet_one_select.draw()
        planet_two_select.draw()
        planet_three_select.draw()
        planet_four_select.draw()
        planet_five_select.draw()
        update()




test_station1 = cls.planet_one_stations(1)
test_station2 = cls.planet_one_stations(2)
test_station3 = cls.planet_one_stations(3)



def showTravelStationMenu(current_planet):



    station_select_menuW = display_width - menuWidth
    station_select_menuH = display_height - menuHeight
    station_select_menuX = menuWidth
    station_select_menuY = 0

    station_select_menu_textY = 10


    station_one_selectW = 210
    station_one_selectH = 210
    station_one_selectX = station_select_menuX + 40
    station_one_selectY = station_select_menuY + 60


    station_select_menu = cls.custom_label_custom_pos_custom_text_pos(game_display, station_select_menuX, station_select_menuY, station_select_menuW, station_select_menuH, options_black, 'Select station', white, 'center', station_select_menu_textY, 'Arial', 30, True, False)

    station_one_select = cls.custom_label_custom_pos_custom_text_pos(game_display, station_one_selectX, station_one_selectY, station_one_selectW, station_one_selectH, white, 'station One', options_black, 'center', station_select_menuY + 70, 'Arial', 30, True, False)
    station_two_select = cls.custom_label_custom_pos_custom_text_pos(game_display, station_one_selectX + 250, station_one_selectY, station_one_selectW, station_one_selectH, white, 'station Two', options_black, 'center', station_select_menuY + 70, 'Arial', 30, True, False)
    station_three_select = cls.custom_label_custom_pos_custom_text_pos(game_display, station_one_selectX + 500, station_one_selectY, station_one_selectW, station_one_selectH, white, 'station Three', options_black, 'center', station_select_menuY + 70, 'Arial', 30, True, False)
    station_four_select = cls.custom_label_custom_pos_custom_text_pos(game_display, station_one_selectX + 750, station_one_selectY, station_one_selectW, station_one_selectH, white, 'station Four', options_black, 'center', station_select_menuY + 70, 'Arial', 30, True, False)
    station_five_select = cls.custom_label_custom_pos_custom_text_pos(game_display, station_one_selectX + 1000, station_one_selectY, station_one_selectW, station_one_selectH, white, 'station Five', options_black, 'center', station_select_menuY + 70, 'Arial', 30, True, False)



    station_selected = False

    while not station_selected:
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                gv.end_game = True
                station_selected = True

            elif ev.type == pg.MOUSEBUTTONUP:
                mpos = pg.mouse.get_pos()
                if ev.button == 1:
                    pass

        station_select_menu.draw()
        station_one_select.draw()
        station_two_select.draw()
        station_three_select.draw()
        station_four_select.draw()
        station_five_select.draw()

        update()




'''
if current_planet == cls.planet_one_stations:
        for station_nr in range(0, cls.planet_one_stations.return_amount_stations()):
            cls.planet_one_stations.return_list_of_stations_index(station_nr).nr


        update()
'''


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
                gv.end_game = True
                keep_options = True

            elif ev.type == pg.MOUSEBUTTONUP:
                mpos = pg.mouse.get_pos()
                if ev.button == 1:
                    if options_quit_btn.rect.collidepoint(mpos):
                        gv.end_game = True
                        keep_options = False
                    elif not options_rect.collidepoint(mpos):
                        keep_options = False

def nextBar(prev_bar_x, prev_bar_W):
    next_bar_x = prev_bar_x + prev_bar_W + 80
    return next_bar_x



def initCombat():

    enemy_names = ['ISS Succubus', 'Tentacruiser', 'Cummunicator']
    enemy_name = r.choice(enemy_names)
    enemy_health_max = r.randrange(100, 140, 2) + 10 * char.level

    if char.level == 1:
        enemy_level = r.randrange(1, char.level + 2)
    else:
        enemy_level = r.randrange(char.level - 1, char.level + 2)

    enemy_hull = 'standard metal'

    test_enemy = cls.combat_enemy(game_display, enemy_name, enemy_health_max, enemy_health_max, enemy_level, enemy_hull)

    test_rectW = 200
    test_rectH = 500
    test_rectX = display_width / 18 * 15
    test_rectY = display_height / 9

    test_combat_rect = cls.custom_label_custom_pos_custom_text_pos(game_display, test_rectX, test_rectY, test_rectW, test_rectH, menu_black, test_enemy.name, white, 'center', test_rectY + 20, 'Arial', 25, True, True)


    test_barW = 170
    test_barH = 50
    test_barX = return_center(test_rectX, test_rectW, test_barW)
    test_barY = test_rectY + 100

    test_combat_health_bar = cls.menu_bar_max(game_display, test_barX, test_barY, test_barW, test_barH, options_black, red, test_enemy.health_max, test_enemy.health_current, 'Health', white, 'Arial', 20, False, True)


    combat_done = False

    current_enemy = test_enemy

    while not combat_done:
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                gv.end_game = True
                combat_done = True

            elif ev.type == pg.MOUSEBUTTONUP:
                mpos = pg.mouse.get_pos()
                if ev.button == 1:
                    if menu_options_btn.rect.collidepoint(mpos):
                        changeMenu('keep_options')

                    elif menu_combat_bar_attack.rect.collidepoint(mpos):
                        ship.health_current -= int(r.randint(10, 20) * (1 - (mf.hull_reduction(ship.hull) / 100)))
                        menu_hp_bar.change_current_set(ship.health_current)
                        wp.energy_weapon_test1.fire(current_enemy)

                        if current_enemy.health_current == 0:
                            showCombatBar()
                            test_combat_rect.draw()
                            test_combat_health_bar.draw()
                            update()
                            showSidebarMenu()
                            #t.sleep(0.1)
                            menu_xp_bar.change_current_add(25)
                            combat_done = True

                        elif current_enemy.health_current == 0:
                            showCombatBar()
                            test_combat_rect.draw()
                            test_combat_health_bar.draw()
                            update()
                            showSidebarMenu()
                            t.sleep(0.5)
                            combat_done = True




                    elif menu_combat_bar_run.rect.collidepoint(mpos):
                        combat_done = True

                    elif menu_combat_btn.rect.collidepoint(mpos):
                        combat_done = True




        showCombatBar()
        test_combat_rect.draw()
        test_combat_health_bar.change_current_set(current_enemy.health_current)
        test_combat_health_bar.draw()
        update()








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




menu_travel_btn = cls.buttons(game_display, menuOptionsX, menuOptionsY - 140, 200, 45, white, 'Travel', menu_black, 'Arial', 30, True, False)
menu_combat_btn = cls.buttons(game_display, menuOptionsX, menuOptionsY - 70, 200, 45, white, 'Attack', menu_black, 'Arial', 30, True, False)







shipInsideImg_rect = shipInsideImg.get_rect(topleft=(xIn,yIn))
shipOutsideImg_rect = shipOutsideImg.get_rect(topleft=(xOut,yOut))

prev_bar_y = menuShipY

menu_hp_bar = cls.menu_bar_max(game_display, menuShipX, menuShipY + 130, 240, 50, options_black, red, ship.health_max, ship.health_current, 'Health', white, 'Arial', 20, False, True)

menu_xp_bar = cls.menu_bar_no_lim(game_display, (menuShipX+ 0), menu_hp_bar.rectY + 130, 240, 50, options_black, green, 200, 100, 'Level Up!', 'XP', white, 'Arial', 20, False, True)



menu_combat_bar_attackW = 400
menu_combat_bar_attackH = menuHeight / 2
menu_combat_bar_attackX = display_width / 30 * 8
menu_combat_bar_attackY = menuBotY + ((menuHeight - menu_combat_bar_attackH) / 2)


menu_combat_bar_runW = 400
menu_combat_bar_runH = menuHeight / 2
menu_combat_bar_runX = display_width / 30 * 20
menu_combat_bar_runY = menuBotY + ((menuHeight - menu_combat_bar_runH) / 2)


menu_combat_bar_attack = cls.custom_label_custom_pos_center(game_display, menu_combat_bar_attackX, menu_combat_bar_attackY, menu_combat_bar_attackW, menu_combat_bar_attackH, white, 'Attack', menu_black, 'Arial', 50, True, False)
menu_combat_bar_run = cls.custom_label_custom_pos_center(game_display, menu_combat_bar_runX, menu_combat_bar_runY, menu_combat_bar_runW, menu_combat_bar_runH, white, 'Run', menu_black, 'Arial', 50, True, False)










def startGame():
    shipInside()
    mainLoop()



def mainLoop():

    menu_to_show = ''



    showMenuTemplate()
    showMenuBasics()


    while not gv.end_game:
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                gv.end_game = True

            elif ev.type == pg.MOUSEBUTTONUP:
                mpos = pg.mouse.get_pos()
                if ev.button == 1:
                    if menu_options_btn.rect.collidepoint(mpos):
                        changeMenu('keep_options')

                    elif name_label_custom.rect.collidepoint(mpos):
                        changeMenu('change_name')

                    elif menu_combat_btn.rect.collidepoint(mpos): #TODO: CHANGE THE FUNCTIONS TO DRAW MENUS/BARS
                        changeMenu('combat_menu')

                    elif menu_travel_btn.rect.collidepoint(mpos):
                        changeMenu('travel_menu')

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

            showMenuTemplate()
            showMenuBasics()
        update()



def update():
    pg.display.update()
    clock.tick(60)

    showMenuBasics()
    


startGame()
pg.quit()

