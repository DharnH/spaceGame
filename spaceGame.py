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
yellow = (255,255,0)
dark_yellow = (204,204,0)
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

    weapon_bars = [menu_combat_bar_weapon1, menu_combat_bar_weapon2, menu_combat_bar_weapon3, menu_combat_bar_weapon4, menu_combat_bar_weapon5, menu_combat_bar_weapon6]

    for k in range(5, len(ship.equipped_weapons)-1, -1):
        weapon_bars[k].change_text('')
        weapon_bars[k].change_rectC(gray)



    menu_combat_bar_weapon1.draw()
    menu_combat_bar_weapon2.draw()
    menu_combat_bar_weapon3.draw()
    menu_combat_bar_weapon4.draw()
    menu_combat_bar_weapon5.draw()
    menu_combat_bar_weapon6.draw()
    menu_combat_cancel_attack.draw()





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
                        pg.event.set_blocked(pg.MOUSEMOTION)
                        t.sleep(0.5)
                        pg.event.set_allowed(pg.MOUSEMOTION)
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

    combat_your_action.change_text('')
    combat_enemy_action.change_text('')

    weapon_bars = [menu_combat_bar_weapon1, menu_combat_bar_weapon2, menu_combat_bar_weapon3, menu_combat_bar_weapon4, menu_combat_bar_weapon5, menu_combat_bar_weapon6]

    available_enemy_names = ['ISS Succubus', 'Tentacruiser', 'Cummunicator']
    enemy_name = r.choice(available_enemy_names)

    if char.level == 1:
        enemy_level = r.randrange(1, char.level + 2)
    else:
        enemy_level = r.randrange(char.level - 1, char.level + 2)

    enemy_health_max = r.randrange(100, 140, 2) + 10 * enemy_level

    if char.level <= 5:
        available_enemy_hulls = ['standard metal']
        available_enemy_weapons = [wp.energy_weapon_10, wp.energy_weapon_30]

    elif char.level <= 10:
        available_enemy_hulls = ['standard metal', 'hardened metal']
        available_enemy_weapons = [wp.energy_weapon_30, wp.energy_weapon_50]

    elif char.level <= 15:
        available_enemy_hulls = ['standard metal', 'hardened metal']
        available_enemy_weapons = [wp.energy_weapon_30, wp.energy_weapon_50]

    elif char.level <= 20:
        available_enemy_hulls = ['standard metal', 'hardened metal']
        available_enemy_weapons = [wp.energy_weapon_30, wp.energy_weapon_50]

    else:
        available_enemy_hulls = ['cheater hull']
        available_enemy_weapons = [wp.cheater_weapon]

    enemy_hull = r.choice(available_enemy_hulls)
    enemy_weapon = r.choice(available_enemy_weapons)

    test_enemy = cls.combat_enemy(game_display, enemy_name, enemy_health_max, enemy_health_max, enemy_level, enemy_hull, enemy_weapon)

    test_rectW = 200
    test_rectH = 500
    test_rectX = display_width / 18 * 15
    test_rectY = display_height / 9

    test_combat_rect = cls.custom_label_custom_pos_custom_text_pos(game_display, test_rectX, test_rectY, test_rectW, test_rectH, menu_black, test_enemy.name, white, 'center', test_rectY + 20, 'Arial', 25, True, True)


    test_barW = 170
    test_barH = 50
    test_barX = return_center(test_rectX, test_rectW, test_barW)
    test_barY = test_rectY + 160

    test_combat_health_bar = cls.menu_bar_max(game_display, test_barX, test_barY, test_barW, test_barH, options_black, red, test_enemy.health_max, test_enemy.health_current, 'Health', white, 'Arial', 20, False, True)

    current_enemy = test_enemy


    combat_level_text = cls.just_text(game_display, test_rectX, test_rectY, test_rectW, test_rectH, 'Lvl. ' + str(current_enemy.level), 'center', test_rectY + 60, white, 'Arial', 20, False, True)
    combat_hull_text = cls.just_text(game_display, test_rectX, test_rectY, test_rectW, test_rectH, current_enemy.ship_hull.capitalize(), 'center', test_rectY + 100, white, 'Arial', 20, False, True)


    combat_done = False

    while not combat_done and not gv.end_game:
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
                        combat_attack(current_enemy, test_combat_rect, combat_level_text, combat_hull_text, test_combat_health_bar, weapon_bars)

                    elif menu_combat_bar_run.rect.collidepoint(mpos):
                        if r.randint(0, 100) <= char.stat_run:
                            combat_run_win(current_enemy, test_combat_rect, combat_level_text, combat_hull_text, test_combat_health_bar)
                            combat_done = True
                        else:
                            combat_run_lose(current_enemy, test_combat_rect, combat_level_text, combat_hull_text, test_combat_health_bar)

                    elif menu_combat_bar_wait.rect.collidepoint(mpos):
                        combat_wait(current_enemy, test_combat_rect, combat_level_text, combat_hull_text, test_combat_health_bar, weapon_bars)

                    elif menu_combat_btn.rect.collidepoint(mpos):
                        combat_done = True

                if current_enemy.health_current <= 0:
                    showCombatBar()
                    test_combat_rect.draw()
                    test_combat_health_bar.draw()
                    update()
                    showSidebarMenu()
                    char.xp_current += 25
                    menu_xp_bar.change_current_set(char.xp_current)
                    combat_win(current_enemy, test_combat_rect, combat_level_text, combat_hull_text, test_combat_health_bar)
                    combat_done = True

                elif current_enemy.health_current <= 0:
                    showCombatBar()
                    test_combat_rect.draw()
                    test_combat_health_bar.draw()
                    update()
                    showSidebarMenu()
                    t.sleep(0.5)
                    combat_lose(current_enemy, test_combat_rect, combat_level_text, combat_hull_text, test_combat_health_bar)
                    combat_done = True


        showMenuTemplate()
        showMenuBasics()
        combat_your_action.draw()
        combat_enemy_action.draw()
        menu_combat_bar_attack.draw()
        menu_combat_bar_wait.draw()
        menu_combat_bar_run.draw()
        test_combat_rect.draw()
        test_combat_health_bar.change_current_set(current_enemy.health_current)
        test_combat_health_bar.draw()
        combat_level_text.draw()
        combat_hull_text.draw()
        update()


    for l in range(0, len(ship.equipped_weapons)):
        weapon_to_reduce = ship.equipped_weapons[l]
        if weapon_to_reduce.recharge_current != 0:
            weapon_to_reduce.recharge_current = 0
            weapon_bars[l].change_rectC(white)



def combat_attack(current_enemy, test_combat_rect, combat_level_text, combat_hull_text, test_combat_health_bar, weapon_bars):
    has_attacked = False
    draw_tooltip = []

    weapon_tooltip_damage_and_rect = cls.custom_label_custom_pos_custom_text_pos(game_display, 0, 0, 0, 0, options_black, 'Damage: 50', white, 0 + 10, 0 + 10, 'Arial', 20, True, False)
    weapon_tooltip_hit_chance = cls.just_text(game_display, 0, 0, 0, 0, 'Hit Change: 100', 0 + 35, 0 + 10, white, 'Arial', 20, True, False)

    weapon_tooltip_type = cls.just_text(game_display, 0, 0, 0, 0, 'Type : ' + str(ship.equipped_weapons[0].type), 0 + 10, 0 + 60, white, 'Arial', 20, True, False)
    weapon_tooltip_recharge_time = cls.just_text(game_display, 0, 0, 0, 0, 'Recharge time : ' + str(ship.equipped_weapons[0].recharge_delay), 0 + 10, 0 + 85, white, 'Arial', 20, True, False)

    weapon_tooltip_recharge_left = cls.just_text(game_display, 0, 0, 0, 0, 'Recharge left : ' + str(ship.equipped_weapons[0].recharge_current), 0 + 10, 0 + 110, white, 'Arial', 20, True, False)




    while not has_attacked:
        for ev in pg.event.get():
            mpos = pg.mouse.get_pos()
            if ev.type == pg.QUIT:
                gv.end_game = True
                has_attacked = True

            elif ev.type == pg.MOUSEBUTTONUP:
                if ev.button == 1:
                    if menu_options_btn.rect.collidepoint(mpos):
                        changeMenu('keep_options')
                        has_attacked = True


                    elif menu_combat_cancel_attack.rect.collidepoint(mpos):
                        has_attacked = True

                    for k in range(0, len(ship.equipped_weapons)):
                        weapon = ship.equipped_weapons[k]

                        if weapon_bars[k].rect.collidepoint(mpos):
                            enemy_damage = current_enemy.fire(ship.hull)
                            if enemy_damage > 0:
                                ship.health_current -= enemy_damage
                                combat_enemy_action.change_text('He hit you for ' + str(enemy_damage) + '!')
                                menu_hp_bar.change_current_set(ship.health_current)
                            else:
                                combat_enemy_action.change_text('He missed!')

                            if weapon.recharge_current == 0:
                                your_damage = weapon.fire(current_enemy)
                                if your_damage > 0:
                                    current_enemy.health_current -= your_damage
                                    combat_your_action.change_text('You hit him for ' + str(your_damage) + '!')
                                else:
                                    combat_your_action.change_text('You missed!')

                                for l in range(0, len(ship.equipped_weapons)):
                                    weapon_to_reduce = ship.equipped_weapons[l]
                                    if weapon_to_reduce.recharge_current != 0:
                                        weapon_to_reduce.recharge_current -= 1
                                        if weapon_to_reduce.recharge_current == 0:
                                            weapon_bars[l].change_rectC(white)

                                if weapon.recharge_delay > 0:
                                    weapon.change_current_set(weapon.recharge_delay)
                                    weapon_bars[k].change_rectC(yellow)

                                has_attacked = True


            elif ev.type == pg.MOUSEMOTION:
                mX, mY = mpos
                draw_tooltip = []

                for k in range(0, len(ship.equipped_weapons)):

                    weapon_tooltipW = 300
                    if ship.equipped_weapons[k].recharge_current > 0:
                        weapon_tooltipH = 145
                    else:
                        weapon_tooltipH = 125
                    weapon_tooltipX = mX
                    weapon_tooltipY = mY - weapon_tooltipH

                    if weapon_bars[k].rect.collidepoint(mpos):
                        weapon_tooltip_damage_and_rect = cls.custom_label_custom_pos_custom_text_pos(game_display, weapon_tooltipX, weapon_tooltipY, weapon_tooltipW, weapon_tooltipH, options_black, 'Damage: ' + str(ship.equipped_weapons[k].damage), white, weapon_tooltipX + 10, weapon_tooltipY + 10, 'Arial', 20, True, False)
                        weapon_tooltip_hit_chance = cls.just_text(game_display, weapon_tooltipX, weapon_tooltipY, weapon_tooltipW, weapon_tooltipH, 'Hit Chance: ' + str(ship.equipped_weapons[k].hit_chance), weapon_tooltipX + 10, weapon_tooltipY + 35, white, 'Arial', 20, True, False)
                        weapon_tooltip_type = cls.just_text(game_display, weapon_tooltipX, weapon_tooltipY, weapon_tooltipW, weapon_tooltipH, 'Type : ' + str(ship.equipped_weapons[k].type), weapon_tooltipX + 10, weapon_tooltipY + 60, white, 'Arial', 20, True, False)
                        weapon_tooltip_recharge_time = cls.just_text(game_display, weapon_tooltipX, weapon_tooltipY, weapon_tooltipW, weapon_tooltipH, 'Recharge time : ' + str(ship.equipped_weapons[k].recharge_delay), weapon_tooltipX + 10, weapon_tooltipY + 85, white, 'Arial', 20, True, False)
                        if ship.equipped_weapons[k].recharge_current > 0:
                            weapon_tooltip_recharge_left = cls.just_text(game_display, weapon_tooltipX, weapon_tooltipY, weapon_tooltipW, weapon_tooltipH, 'Recharge left : ' + str(ship.equipped_weapons[k].recharge_current), weapon_tooltipX + 10, weapon_tooltipY + 110, white, 'Arial', 20, True, False)
                        else:
                            weapon_tooltip_recharge_left.change_text('')
                        draw_tooltip.append(True)


        showMenuTemplate()
        showMenuBasics()
        showCombatBar()
        combat_your_action.draw()
        combat_enemy_action.draw()
        if True in draw_tooltip:
            weapon_tooltip_damage_and_rect.draw()
            weapon_tooltip_hit_chance.draw()
            weapon_tooltip_type.draw()
            weapon_tooltip_recharge_time.draw()
            weapon_tooltip_recharge_left.draw()
        test_combat_rect.draw()
        test_combat_health_bar.change_current_set(current_enemy.health_current)
        test_combat_health_bar.draw()
        combat_level_text.draw()
        combat_hull_text.draw()
        update()


def combat_win(current_enemy, test_combat_rect, combat_level_text, combat_hull_text, test_combat_health_bar):
    continued = False

    while not continued:
        for ev in pg.event.get():
            mpos = pg.mouse.get_pos()
            if ev.type == pg.QUIT:
                gv.end_game = True
                continued = True

            elif ev.type == pg.MOUSEBUTTONUP:
                if ev.button == 1:
                    if menu_options_btn.rect.collidepoint(mpos):
                        changeMenu('keep_options')
                        continued = True

                    elif menu_combat_bar_continue.rect.collidepoint(mpos):
                        continued = True

        showMenuTemplate()
        showMenuBasics()
        menu_combat_bar_continue.draw()
        combat_your_action.draw()
        combat_enemy_action.draw()
        combat_you_win.draw()
        test_combat_rect.draw()
        test_combat_health_bar.change_current_set(current_enemy.health_current)
        test_combat_health_bar.draw()
        combat_level_text.draw()
        combat_hull_text.draw()
        update()


def combat_lose(current_enemy, test_combat_rect, combat_level_text, combat_hull_text, test_combat_health_bar):

    continued = False

    while not continued:
        for ev in pg.event.get():
            mpos = pg.mouse.get_pos()
            if ev.type == pg.QUIT:
                gv.end_game = True
                continued = True

            elif ev.type == pg.MOUSEBUTTONUP:
                if ev.button == 1:
                    if menu_options_btn.rect.collidepoint(mpos):
                        changeMenu('keep_options')
                        continued = True

                    elif menu_combat_bar_continue.rect.collidepoint(mpos):
                        continued = True

        showMenuTemplate()
        showMenuBasics()
        menu_combat_bar_continue.draw()
        combat_your_action.draw()
        combat_enemy_action.draw()
        combat_you_lose.draw()
        test_combat_rect.draw()
        test_combat_health_bar.change_current_set(current_enemy.health_current)
        test_combat_health_bar.draw()
        combat_level_text.draw()
        combat_hull_text.draw()
        update()




def combat_wait(current_enemy, test_combat_rect, combat_level_text, combat_hull_text, test_combat_health_bar, weapon_bars):

    continued = False

    combat_your_action.change_text('You wait.')
    combat_enemy_action.change_text('')

    enemy_damage = current_enemy.fire(ship.hull)
    if enemy_damage > 0:
        ship.health_current -= enemy_damage
        combat_enemy_action.change_text('He hit you for ' + str(enemy_damage) + '!')
        menu_hp_bar.change_current_set(ship.health_current)
    else:
        combat_enemy_action.change_text('He missed!')

    for l in range(0, len(ship.equipped_weapons)):
        weapon_to_reduce = ship.equipped_weapons[l]
        if weapon_to_reduce.recharge_current != 0:
            weapon_to_reduce.recharge_current -= 1
            if weapon_to_reduce.recharge_current == 0:
                weapon_bars[l].change_rectC(white)

    while not continued:
        for ev in pg.event.get():
            mpos = pg.mouse.get_pos()
            if ev.type == pg.QUIT:
                gv.end_game = True
                continued = True

            elif ev.type == pg.MOUSEBUTTONUP:
                if ev.button == 1:
                    if menu_options_btn.rect.collidepoint(mpos):
                        changeMenu('keep_options')
                        continued = True

                    elif menu_combat_bar_continue.rect.collidepoint(mpos):
                        continued = True

        showMenuTemplate()
        showMenuBasics()
        menu_combat_bar_continue.draw()
        combat_your_action.draw()
        combat_enemy_action.draw()
        test_combat_rect.draw()
        test_combat_health_bar.change_current_set(current_enemy.health_current)
        test_combat_health_bar.draw()
        combat_level_text.draw()
        combat_hull_text.draw()
        update()




def combat_run_win(current_enemy, test_combat_rect, combat_level_text, combat_hull_text, test_combat_health_bar):

    continued = False

    combat_your_action.change_text('You got away!')
    combat_enemy_action.change_text('')

    while not continued:
        for ev in pg.event.get():
            mpos = pg.mouse.get_pos()
            if ev.type == pg.QUIT:
                gv.end_game = True
                continued = True

            elif ev.type == pg.MOUSEBUTTONUP:
                if ev.button == 1:
                    if menu_options_btn.rect.collidepoint(mpos):
                        changeMenu('keep_options')
                        continued = True

                    elif menu_combat_bar_continue.rect.collidepoint(mpos):
                        continued = True

        showMenuTemplate()
        showMenuBasics()
        menu_combat_bar_continue.draw()
        combat_your_action.draw()
        test_combat_rect.draw()
        test_combat_health_bar.change_current_set(current_enemy.health_current)
        test_combat_health_bar.draw()
        combat_level_text.draw()
        combat_hull_text.draw()
        update()



def combat_run_lose(current_enemy, test_combat_rect, combat_level_text, combat_hull_text, test_combat_health_bar):

    continued = False

    combat_your_action.change_text('You failed to get away!')
    combat_enemy_action.change_text('')

    enemy_damage = current_enemy.fire(ship.hull)
    if enemy_damage > 0:
        ship.health_current -= enemy_damage
        combat_enemy_action.change_text('He hit you for ' + str(enemy_damage) + '!')
        menu_hp_bar.change_current_set(ship.health_current)
    else:
        combat_enemy_action.change_text('He missed!')

    while not continued:
        for ev in pg.event.get():
            mpos = pg.mouse.get_pos()
            if ev.type == pg.QUIT:
                gv.end_game = True
                continued = True

            elif ev.type == pg.MOUSEBUTTONUP:
                if ev.button == 1:
                    if menu_options_btn.rect.collidepoint(mpos):
                        changeMenu('keep_options')
                        continued = True

                    elif menu_combat_bar_continue.rect.collidepoint(mpos):
                        continued = True

        showMenuTemplate()
        showMenuBasics()
        menu_combat_bar_continue.draw()
        combat_your_action.draw()
        combat_enemy_action.draw()
        test_combat_rect.draw()
        test_combat_health_bar.change_current_set(current_enemy.health_current)
        test_combat_health_bar.draw()
        combat_level_text.draw()
        combat_hull_text.draw()
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

menu_xp_bar = cls.menu_bar_no_lim(game_display, (menuShipX+ 0), menu_hp_bar.rectY + 130, 240, 50, options_black, green, char.xp_max, char.xp_current, 'Level Up!', 'XP', white, 'Arial', 20, False, True)



menu_combat_bar_weaponW = 300
menu_combat_bar_weaponH = menuHeight / 3
menu_combat_bar_weaponX = display_width / 30 * 6
menu_combat_bar_weaponY = menuBotY + 20

'''
menu_combat_bar_runW = 200
menu_combat_bar_runH = menuHeight / 4
menu_combat_bar_runX = display_width / 30 * 20
menu_combat_bar_runY = menuBotY + 20
'''




if 0 in range(0, len(ship.equipped_weapons)):
    menu_combat_bar_weapon1 = cls.custom_label_custom_pos_center(game_display, menu_combat_bar_weaponX, menu_combat_bar_weaponY, menu_combat_bar_weaponW, menu_combat_bar_weaponH, white, ship.equipped_weapons[0].name, menu_black, 'Arial', 25, True, False)

else:
    menu_combat_bar_weapon1 = cls.custom_label_custom_pos_center(game_display, menu_combat_bar_weaponX, menu_combat_bar_weaponY, menu_combat_bar_weaponW, menu_combat_bar_weaponH, white, '', menu_black, 'Arial', 25, True, False)

if 1 in range(0, len(ship.equipped_weapons)):
    menu_combat_bar_weapon2 = cls.custom_label_custom_pos_center(game_display, menu_combat_bar_weaponX, menu_combat_bar_weaponY + menuHeight / 2.2, menu_combat_bar_weaponW, menu_combat_bar_weaponH, white, ship.equipped_weapons[1].name, menu_black, 'Arial', 25, True, False)

else:
    menu_combat_bar_weapon2 = cls.custom_label_custom_pos_center(game_display, menu_combat_bar_weaponX, menu_combat_bar_weaponY + menuHeight / 2.2, menu_combat_bar_weaponW, menu_combat_bar_weaponH, white, '', menu_black, 'Arial', 25, True, False)

if 2 in range(0, len(ship.equipped_weapons)):
    menu_combat_bar_weapon3 = cls.custom_label_custom_pos_center(game_display, menu_combat_bar_weaponX + 320, menu_combat_bar_weaponY, menu_combat_bar_weaponW, menu_combat_bar_weaponH, white, ship.equipped_weapons[2].name, menu_black, 'Arial', 25, True, False)

else:
    menu_combat_bar_weapon3 = cls.custom_label_custom_pos_center(game_display, menu_combat_bar_weaponX + 320, menu_combat_bar_weaponY, menu_combat_bar_weaponW, menu_combat_bar_weaponH, white, '', menu_black, 'Arial', 25, True, False)

if 3 in range(0, len(ship.equipped_weapons)):
    menu_combat_bar_weapon4 = cls.custom_label_custom_pos_center(game_display, menu_combat_bar_weaponX + 320, menu_combat_bar_weaponY + menuHeight / 2.2, menu_combat_bar_weaponW, menu_combat_bar_weaponH, white, ship.equipped_weapons[3].name, menu_black, 'Arial', 25, True, False)

else:
    menu_combat_bar_weapon4 = cls.custom_label_custom_pos_center(game_display, menu_combat_bar_weaponX + 320, menu_combat_bar_weaponY + menuHeight / 2.2, menu_combat_bar_weaponW, menu_combat_bar_weaponH, white, '', menu_black, 'Arial', 25, True, False)

if 4 in range(0, len(ship.equipped_weapons)):
    menu_combat_bar_weapon5 = cls.custom_label_custom_pos_center(game_display, menu_combat_bar_weaponX + 640, menu_combat_bar_weaponY, menu_combat_bar_weaponW, menu_combat_bar_weaponH, white, ship.equipped_weapons[4].name, menu_black, 'Arial', 25, True, False)

else:
    menu_combat_bar_weapon5 = cls.custom_label_custom_pos_center(game_display, menu_combat_bar_weaponX + 640, menu_combat_bar_weaponY, menu_combat_bar_weaponW, menu_combat_bar_weaponH, white, '', menu_black, 'Arial', 25, True, False)

if 5 in range(0, len(ship.equipped_weapons)):
    menu_combat_bar_weapon6 = cls.custom_label_custom_pos_center(game_display, menu_combat_bar_weaponX + 640, menu_combat_bar_weaponY + menuHeight / 2.2, menu_combat_bar_weaponW, menu_combat_bar_weaponH, white, ship.equipped_weapons[5].name, menu_black, 'Arial', 25, True, False)

else:
    menu_combat_bar_weapon6 = cls.custom_label_custom_pos_center(game_display, menu_combat_bar_weaponX + 640, menu_combat_bar_weaponY + menuHeight / 2.2, menu_combat_bar_weaponW, menu_combat_bar_weaponH, white, '', menu_black, 'Arial', 25, True, False)


menu_combat_cancel_attack = cls.custom_label_custom_pos_center(game_display, menu_combat_bar_weaponX + 960, menu_combat_bar_weaponY + menuHeight / 4, menu_combat_bar_weaponW, menu_combat_bar_weaponH, white, 'Cancel attack', menu_black, 'Arial', 30, True, False)




combat_your_action = cls.just_text(game_display, 0, 0, 0, 0, '', 300, 200, options_black, 'Arial', 90, True, False)

combat_enemy_action = cls.just_text(game_display, 0, 0, 0, 0, '', 300, 320, options_black, 'Arial', 90, True, False)

combat_you_win = cls.just_text(game_display, 0, 0, 0, 0, 'You Win!', 300, 440, options_black, 'Arial', 90, True, False)

combat_you_lose = cls.just_text(game_display, 0, 0, 0, 0, 'You Lose!', 300, 440, options_black, 'Arial', 90, True, False)

combat_you_run_win = cls.just_text(game_display, 0, 0, 0, 0, 'You got away!', 300, 200, options_black, 'Arial', 90, True, False)

combat_you_run_lose = cls.just_text(game_display, 0, 0, 0, 0, 'You failed to get away!', 300, 200, options_black, 'Arial', 90, True, False)











menu_combat_bar_attackW = 300
menu_combat_bar_attackH = menuHeight / 2.5
menu_combat_bar_attackX = display_width / 30 * 7
menu_combat_bar_attackY = menuBotY + ((menuHeight - menu_combat_bar_attackH) / 2)


menu_combat_bar_waitW = 300
menu_combat_bar_waitH = menuHeight / 2.5
menu_combat_bar_waitX = display_width / 30 * 14.5
menu_combat_bar_waitY = menuBotY + ((menuHeight - menu_combat_bar_attackH) / 2)


menu_combat_bar_runW = 300
menu_combat_bar_runH = menuHeight / 2.5
menu_combat_bar_runX = display_width / 30 * 22
menu_combat_bar_runY = menuBotY + ((menuHeight - menu_combat_bar_runH) / 2)




menu_combat_bar_attack = cls.custom_label_fix_pos_center(game_display, menu_combat_bar_attackX, menu_combat_bar_attackY, menu_combat_bar_attackW, menu_combat_bar_attackH, white, 'Attack', menu_black, 'Arial', 40, True, False)

menu_combat_bar_wait = cls.custom_label_custom_pos_center(game_display, menu_combat_bar_waitX, menu_combat_bar_waitY, menu_combat_bar_waitW, menu_combat_bar_waitH, white, 'Wait', menu_black, 'Arial', 40, True, False)

menu_combat_bar_run = cls.custom_label_custom_pos_center(game_display, menu_combat_bar_runX, menu_combat_bar_runY, menu_combat_bar_runW, menu_combat_bar_runH, white, 'Run', menu_black, 'Arial', 40, True, False)

menu_combat_bar_continue = cls.custom_label_fix_pos_center(game_display, menu_combat_bar_attackX, menu_combat_bar_attackY, menu_combat_bar_attackW, menu_combat_bar_attackH, white, 'Continue', menu_black, 'Arial', 50, True, False)








def startGame():
    shipInside()
    mainLoop()



def mainLoop():

    menu_to_show = ''



    showMenuTemplate()
    showMenuBasics()


    while not gv.end_game:
        for ev in pg.event.get():
            mpos = pg.mouse.get_pos()
            if ev.type == pg.QUIT:
                gv.end_game = True

            elif ev.type == pg.MOUSEBUTTONUP:
                if ev.button == 1:
                    if menu_options_btn.rect.collidepoint(mpos):
                        changeMenu('keep_options')

                    elif name_label_custom.rect.collidepoint(mpos):
                        changeMenu('change_name')

                    elif menu_combat_btn.rect.collidepoint(mpos):
                        changeMenu('combat_menu')

                    elif menu_travel_btn.rect.collidepoint(mpos):
                        changeMenu('travel_menu')

                    elif menu_xp_bar.rect.collidepoint(mpos):
                        if char.xp_current >= char.xp_max:
                            char.level += 1
                            char.xp_current -= char.xp_max
                            char.xp_max += 100
                            menu_xp_bar.change_max_set(char.xp_max)
                        else:
                            normal_text = menu_xp_bar.text
                            menu_xp_bar.change_text('Not enough xp!')
                            showMenuBasics()
                            update()
                            pg.event.set_blocked(pg.MOUSEMOTION)
                            t.sleep(0.5)
                            pg.event.set_allowed(pg.MOUSEMOTION)
                            menu_xp_bar.change_text(normal_text)

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
                        menu_hp_bar.change_current_add(25)
                    elif menu_xp_bar.background_bar.collidepoint(mpos):
                        char.xp_current += 25
                        menu_xp_bar.change_current_set(char.xp_current)

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

