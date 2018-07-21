# Vul hier je naaam en de naam van je spel in
import pygame as pg
import random as r
import ctypes as ct
import time as t

# -------- Globale Variabelen --------

# bord afbeelding:
BORD = pg.image.load("myBoard.png")

# coordianten van de vakjes:
VAKJES = [[160, 683], [286, 683], [356, 683], [415, 683], [482, 683], [545, 683],
    [618, 683], [692, 683], [758, 683], [828, 643], [895, 598], [937, 549], [965, 489],
    [982, 430], [982, 353], [968, 283], [944, 220], [905, 167], [833, 111], [744, 66],
    [664, 62], [597, 62], [536, 62], [464, 62], [398, 62], [335, 62], [265, 66], [198, 94],
    [142, 129], [104, 174], [83, 227], [65, 283], [65, 367], [83, 435], [116, 491], [160, 535],
    [216, 570], [282, 587], [342, 587], [405, 587], [468, 587], [536, 587], [615, 587],
    [692, 587], [755, 578], [816, 528], [863, 458], [877, 402], [874, 335], [856, 283],
    [804, 202], [737, 160], [632, 157], [545, 157], [468, 157], [394, 157], [328, 157],
    [265, 167], [195, 223], [167, 325], [188, 403], [221, 454], [282, 482], [413, 456]]

# pion posities
posities = [0, 0, 0, 0]

# wie is er aan de beurt?
beurt = 0

# dobbelsteenworp

worp = 0


# --- Teken de graphics (nog buiten beeld) ---

def showScreen(screen, clock, amount_players, picked_colors, players_flags_array):

    screen.fill((255, 255, 255))  # begin met een witte achtergond

    bordrect = BORD.get_rect()  # vraag afmetingen (rectangle) van het bordplaatje op
    screen.blit(BORD, bordrect)  # reken het bord

    # teken pionnen als gekleurde cirkels op de coordinaten van de vakjes waar ze staan:

    if amount_players >= 2:
        speler1_x = VAKJES[posities[0]][0]
        speler1_y = VAKJES[posities[0]][1]
        speler1_kleur = picked_colors[0]
        pg.draw.circle(screen, speler1_kleur, (speler1_x, speler1_y), 10)

        speler2_x = VAKJES[posities[1]][0] + 3
        speler2_y = VAKJES[posities[1]][1] + 3
        speler2_kleur = picked_colors[1]
        pg.draw.circle(screen, speler2_kleur, (speler2_x, speler2_y), 10)

    if amount_players >= 3:
        speler3_x = VAKJES[posities[2]][0] + 6
        speler3_y = VAKJES[posities[2]][1] + 6
        speler3_kleur = picked_colors[2]
        pg.draw.circle(screen, speler3_kleur, (speler3_x, speler3_y), 10)

    if amount_players >= 4:
        speler4_x = VAKJES[posities[3]][0] + 9
        speler4_y = VAKJES[posities[3]][1] + 9
        speler4_kleur = picked_colors[3]
        pg.draw.circle(screen, speler4_kleur, (speler4_x, speler4_y), 10)

    clock.tick(60)  # Zet de limiet op 60 frames per seconde en

    pg.display.flip()  # ververs het beeldscherm met de bijgewerkte versie

    global worp
    global beurt
    # Kies een lettergrootte:
    myfont = pg.font.SysFont(None, 25)

    # teken de laatste worp op het scherm
    text1 = "Laatste worp: " + str(worp) + "   Beurt: speler " + str(beurt + 1)
    label1 = myfont.render(text1, 1, (0, 0, 0))
    screen.blit(label1, (415, 450))
    
    if players_flags_array[beurt][2]:
        status = "Vast tot een andere speler op dit vakje komt"
    elif players_flags_array[beurt][3]:
        status = "Goed"
    elif players_flags_array[beurt][1] > 0:
        if players_flags_array[beurt][1] == 1:
            beurt_en = "beurt"
        else:
            beurt_en = "beurten"
        status = "Vast voor " + str(players_flags_array[beurt][1]) + " " + beurt_en
    else:
        status = "Goed"

    text2 = "Status speler: " + status
    label2 = myfont.render(text2, 1, (0, 0, 0))
    screen.blit(label2, (415, 470))

    # --- Ververs het beeldscherm met de nieuwe graphics ---

    pg.display.flip()  # ververs het beeldscherm met de bijgewerkte versie


def moveDot(move_to_position, screen, clock, amount_players, picked_colors, players_flags_array):  # beweeg de stip, 1 vakje per 0.1 seconde.

    # beweeg de stip sneller als het helemaal terug naar vakje 0 moet
    if move_to_position == 0:
        sleep_time = 0.02
    else:
        sleep_time = 0.1

    if move_to_position >= posities[beurt]:
        while posities[beurt] != move_to_position:
            t.sleep(sleep_time)
            posities[beurt] += 1
            showScreen(screen, clock, amount_players, picked_colors, players_flags_array)
    else:
        while posities[beurt] != move_to_position:
            t.sleep(sleep_time)
            posities[beurt] -= 1
            showScreen(screen, clock, amount_players, picked_colors, players_flags_array)


def moveTo(players_flags_array, amount_players, screen, clock, picked_colors, alterd_two_player_rules):  # bereken waar de stip naartoe moet

    global worp
    goose_go_back = False
    last_position = 0  # Voor als je verder dan 63 gooit, om het aantal vakjes te berekenen die te ver zijn gegooid

    need_to_go = posities[beurt]  # Voor de berekening voordat de stip verzet wordt (tegen overflow van vakjes 63+)

    POSITION_GOOSES = [5, 9, 14, 18, 23, 27, 32, 36, 41, 45, 50, 54, 59]  # de vakjes van de ganzen

    # kijk of er een worp (1-6) gegooid moet worden. Zo ja, gooi een worp
    if(players_flags_array[beurt][1] == 0 or players_flags_array[beurt][3]) and not players_flags_array[beurt][2]:
        worp = r.randint(1, 6)
        last_position = posities[beurt]
        need_to_go += worp
        players_flags_array[beurt][3] = False
        players_flags_array[beurt][1] = 0

    # mag de speler de volgende beurt weer bewegen
    elif players_flags_array[beurt][1] == 1:
        players_flags_array[beurt][3] = True

    # verlaag de aantal beurten dat de speler vast zit
    if players_flags_array[beurt][1] != 0:
        players_flags_array[beurt][1] -= 1

    # als de speler over 63 heen gooit
    if need_to_go > 63:
        amount_to_far = worp - (63 - last_position)
        moveDot(63, screen, clock, amount_players, picked_colors, players_flags_array)
        need_to_go = 63 - amount_to_far
        moveDot(need_to_go, screen, clock, amount_players, picked_colors, players_flags_array)
        goose_go_back = True

    # als de speler op een gans komt (organje vakjes), ga de gegooide worp nog een keer vooruit (of achteruit als je terug komt van vakje 63)
    while need_to_go in POSITION_GOOSES:
        moveDot(need_to_go, screen, clock, amount_players, picked_colors, players_flags_array)
        t.sleep(0.2)

        if goose_go_back:
            need_to_go -= worp
            moveDot(need_to_go, screen, clock, amount_players, picked_colors, players_flags_array)

        elif not goose_go_back:
            last_position_after_goose = need_to_go
            need_to_go += worp

            if need_to_go > 63:
                amount_to_far = worp - (63 - last_position_after_goose)
                moveDot(63, screen, clock, amount_players, picked_colors, players_flags_array)
                need_to_go = 63 - amount_to_far
                moveDot(need_to_go, screen, clock, amount_players, picked_colors, players_flags_array)
                goose_go_back = True

            else:
                moveDot(need_to_go, screen, clock, amount_players, picked_colors, players_flags_array)

        if need_to_go == 63:
            return

    # vakje 6 (licht blauw), ga door naar 12
    if need_to_go == 6:
        moveDot(need_to_go, screen, clock, amount_players, picked_colors, players_flags_array)
        t.sleep(0.3)
        moveDot(12, screen, clock, amount_players, picked_colors, players_flags_array)

    # vakje 19 (paars), blijf 1 beurt vast zitten
    elif need_to_go == 19:
        moveDot(need_to_go, screen, clock, amount_players, picked_colors, players_flags_array)
        players_flags_array[beurt][1] = 1
        players_flags_array[beurt][2] = False

    # vakje 31 (rood), blijf vast zitten tot een andere speler op het vakeje komt en zet de andere speler dan vast
    elif need_to_go == 31:  # tenzij de aangepaste regels ingeschakelt zijn, bijf dan 3 beurten zitten of totdat een andere speler komt
        moveDot(need_to_go, screen, clock, amount_players, picked_colors, players_flags_array)
        for x in range(0, amount_players):
            if x != beurt and posities[x] == posities[beurt]:
                    players_flags_array[x][1] = 0
                    players_flags_array[x][2] = False

        if alterd_two_player_rules:
            if players_flags_array[beurt][1] == 0:
                players_flags_array[beurt][1] = 3
            players_flags_array[beurt][2] = False

        else:
            players_flags_array[beurt][1] = 1
            players_flags_array[beurt][2] = True

    # vakje 39 (donker blauw), ga terug naar vakje 39
    elif need_to_go == 42:
        moveDot(need_to_go, screen, clock, amount_players, picked_colors, players_flags_array)
        t.sleep(0.3)
        moveDot(39, screen, clock, amount_players, picked_colors, players_flags_array)

    # vakje 52 (rood), hetzelfde als vakje 31
    elif need_to_go == 52:
        moveDot(need_to_go, screen, clock, amount_players, picked_colors, players_flags_array)
        for x in range(0, amount_players):
            if x != beurt and posities[x] == posities[beurt]:
                    players_flags_array[x][1] = 0
                    players_flags_array[x][2] = False

        if alterd_two_player_rules:
            if players_flags_array[beurt][1] == 0:
                players_flags_array[beurt][1] = 3
            players_flags_array[beurt][2] = False

        else:
            players_flags_array[beurt][1] = 1
            players_flags_array[beurt][2] = True

    # vakje 58 (grijs), ga terug naar het begin, vakje 0
    elif need_to_go == 58:
        moveDot(need_to_go, screen, clock, amount_players, picked_colors, players_flags_array)
        t.sleep(0.3)
        moveDot(0, screen, clock, amount_players, picked_colors, players_flags_array)

    # vakje 63 (geel), je hebt gewonnen
    elif need_to_go == 63:
        moveDot(need_to_go, screen, clock, amount_players, picked_colors, players_flags_array)
        return

    # als je niet op een speciaal vakje komt, ga dan gewoon naar het vakje waar je naartoe moet
    else:
        moveDot(need_to_go, screen, clock, amount_players, picked_colors, players_flags_array)

    # update het scherm
    showScreen(screen, clock, amount_players, picked_colors, players_flags_array)


# -------- Hoofdloop van het programma --------
def playGame(end_game, screen, clock, amount_players, picked_colors, alterd_two_player_rules):

    global worp
    global beurt

    # Deze integers/flags beslissen of je wel mag gooien of dat je op hetzelfde vakje moet wachten.
    player_one_flags = [0, 0, False, False]  # [0] = het nummer van de speler
    player_two_flags = [1, 0, False, False]  # [1] = het aantal beurten dat de speler moet wachten
    player_three_flags = [2, 0, False, False]  # [2] = moet de speler voor een onzeker aantal beurten wachten
    player_four_flags = [3, 0, False, False]  # [3] = mag de speler de volgende beurt zeker weer verder

    players_flags_array = [player_one_flags, player_two_flags, player_three_flags, player_four_flags]

    showScreen(screen, clock, amount_players, picked_colors, players_flags_array)

    while not end_game:
        # --- Check gebeurtenissen (zoals muisklick e.d.) ---
        for event in pg.event.get():
            if event.type == pg.QUIT:  # Het kruisje is aangeklikt
                end_game = True  # Het spel moet eindigen dus we zetten end_game op True

            elif event.type == pg.KEYDOWN:
                # Er is een toets ingedrukt, we kijken welke en ondernemen actie

                if event.key == pg.K_SPACE:
                    print("Knop: Spatie")

                    moveTo(players_flags_array, amount_players, screen, clock, picked_colors, alterd_two_player_rules)

                    # als een speler heeft gewonnen, vraag of de speler nog een keer wilt spelen
                    if posities[beurt] == 63:  # de msg box staat hier zodat de end_game aangepast kan worden zoder 'global' of een return value
                        gebruikers_keuze = ct.windll.user32.MessageBoxW(0, "Je hebt gewonnen! Met worp " + str(worp) + "\nKlik 'OK' om nog een keer te spelen of klik op 'Annuleren' om te stoppen", "Einde", 1)
                        if gebruikers_keuze == 1:
                            restart(end_game, screen, clock, amount_players, picked_colors, alterd_two_player_rules, players_flags_array)

                        elif gebruikers_keuze == 2:
                            end_game = True

                    # geef de beurt aan de volgende speler
                    beurt += 1
                    if beurt >= amount_players:
                        beurt = 0
                    t.sleep(0.3)
                    showScreen(screen, clock, amount_players, picked_colors, players_flags_array)

                # als er op backspace wordt geklikt, restart het spel
                elif event.key == pg.K_BACKSPACE:
                    print("Knop: Backspace")
                    restart(end_game, screen, clock, amount_players, picked_colors, alterd_two_player_rules, players_flags_array)


# herstart het spel, reset alle globale variabelen terug naar 0
def restart(end_game, screen, clock, amount_players, picked_colors, alterd_two_player_rules, players_flags_array):

    global posities
    global beurt
    global worp

    # laat eerst iedereen terug lopen voordat de posities worden gereset
    for x in range(0, amount_players):
        beurt = x
        moveDot(0, screen, clock, amount_players, picked_colors, players_flags_array)

    posities = [0, 0, 0, 0]
    beurt = 0
    worp = 0

    print(end_game)

    # update het scherm en start de main loop
    showScreen(screen, clock, amount_players, picked_colors, players_flags_array)
    playGame(end_game, screen, clock, amount_players, picked_colors, alterd_two_player_rules)


# vraag het aantal spelers
def askAmountPlayers():
    amount_given = False
    player_amount_input = 0

    # zolang er nog geen goed antwoord is gegeven, vraag het opnieuw
    while not amount_given:
        already_said = False
        try:
            player_amount_input = int(input("How many players? (2-4)\n"))
        except ValueError:
            print("Not a number between 2 and 4")
            already_said = True
        if player_amount_input not in range(2, 5) and not already_said:
            print("Not a number between 2 and 4")
        elif player_amount_input in range(2, 5):
            amount_given = True
            return player_amount_input


# vraag de kleur van de spelers
def askColorPlayers(current_player, available_colors_name, available_colors_rgb):
    
    color_selected = False
    
    print("\nChoose a color and type the name of the color. Available preset colors: ")
    for y in range(0, len(available_colors_name)):
        print(available_colors_name[y])
    print("You can also type 'custom' to create your own RGB color")

    # zolang er nog geen goed antwoord is gegeven, vraag het weer opnieuw
    while not color_selected:  # return de gekozen kleur op return 'custom' als de speler zelf een kleur wilt maken
        picked_color = input("\nColor Player " + str(current_player + 1) + "\n")
        if picked_color in available_colors_name:
            color_selected = True
            return available_colors_rgb[available_colors_name.index(picked_color)], picked_color
        elif picked_color == "custom":
            color_selected = True
            return None, picked_color
        else:
            print("Not an available color. Please enter a color")


# vraag alles aan de spelers alles wat nodig is. (aantal, kleur, speciale regels)
def askPlayers():

    available_colors_name = ["light blue", "brown", "yellow", "black", "white"]
    available_colors_rgb = [(0, 255, 255), (210, 105, 30), (255, 255, 0), (0, 0, 0), (255, 255, 255)]
    game_picked_colors = []
    custom_rgb_red, custom_rgb_green, custom_rgb_blue = None, None, None

    game_alterd_two_player_rules = False

    # call de functie om het aantal spelers te vragen
    game_amount_players = askAmountPlayers()
    print(str(game_amount_players) + " players")

    for x in range(0, game_amount_players):
        picked_rgb_value, picked_color = askColorPlayers(x, available_colors_name, available_colors_rgb)

        # laat de speler een custom kleur maken met de RGB waardes
        if picked_color == "custom":
            rgb_red_given = False
            while not rgb_red_given:
                try:
                    if custom_rgb_red is None:
                        custom_rgb_red = int(input("enter RGB Red (0-255)\n"))
                        if custom_rgb_red not in range(0, 256):
                            print("Not a value between 0 and 255. Please re-enter")
                            custom_rgb_red = None
                        else:
                            rgb_red_given = True
                except ValueError:
                    print("Not a value between 0 and 255. Please re-enter")

            rgb_green_given = False
            while not rgb_green_given:
                try:
                    if custom_rgb_green is None:
                        custom_rgb_green = int(input("enter RGB Red (0-255)\n"))
                        if custom_rgb_green not in range(0, 256):
                            print("Not a value between 0 and 255. Please re-enter")
                            custom_rgb_green = None
                        else:
                            rgb_green_given = True
                except ValueError:
                    print("Not a value between 0 and 255. Please re-enter")

            rgb_blue_given = False
            while not rgb_blue_given:
                try:
                    if custom_rgb_blue is None:
                        custom_rgb_blue = int(input("enter RGB Red (0-255)\n"))
                        if custom_rgb_blue not in range(0, 256):
                            print("Not a value between 0 and 255. Please re-enter")
                            custom_rgb_blue = None
                        else:
                            rgb_blue_given = True
                except ValueError:
                    print("Not a value between 0 and 255. Please re-enter")

            game_picked_colors.append((custom_rgb_red, custom_rgb_green, custom_rgb_blue))

            custom_rgb_red, custom_rgb_green, custom_rgb_blue = None, None, None

        else:
            available_colors_rgb.remove(available_colors_rgb[available_colors_name.index(picked_color)])
            available_colors_name.remove(picked_color)
            game_picked_colors.append(picked_rgb_value)

    # vertel de kleuren
    print("\n")
    for x in range(0, game_amount_players):
        print("Player " + str(x + 1) + " has color " + str(game_picked_colors[x]))

    # vraag voor aangepaste regels voor 2 spelers
    if game_amount_players == 2:
        alterd_rules_not_set = False
        while not alterd_rules_not_set:
            alterd_two_player_rules_input = input("\nAltered rules for 2 players? The well/prison will only keep you for 3 turns or until someone else comes. (yes/no)\n")
            if alterd_two_player_rules_input == "yes" or alterd_two_player_rules_input == "y":
                game_alterd_two_player_rules = True
                alterd_rules_not_set = True
            elif alterd_two_player_rules_input == "no" or alterd_two_player_rules_input == "n":
                game_alterd_two_player_rules = False
                alterd_rules_not_set = True
            else:
                print("That wasn't 'yes' or 'no'\nPleane re-enter\n")

    startPygame(game_amount_players, game_picked_colors, game_alterd_two_player_rules)


# -------- Pygame Initialisatie --------
def startPygame(game_amount_players, game_picked_colors, game_alterd_two_player_rules):
    # Pygame initialiseren (is altijd nodig bij begin van gebruik pygame)
    pg.init()

    # Afmetingen van het spelscherm instellen (in pixels [breedte, hoogte])
    # En het spelscherm maken (en opslaan in een variabele screen)
    WINDOW_SIZE = [1050, 750]
    game_screen = pg.display.set_mode(WINDOW_SIZE)

    # Titel van het spelscherm instellen
    pg.display.set_caption("Daan's Goose Board")

    # We maken een pygame Clock object. Deze is nodig om de verversingsnelheid
    # (framerate) van het scherm te beheren
    game_clock = pg.time.Clock()

    # Deze boolean laat ons spel straks in een oneindige loop lopen, totdat er op
    # het kruisje wordt geklikt om af te sluiten (deze zet dan end_game op True)
    game_end_game = False

    playGame(game_end_game, game_screen, game_clock, game_amount_players, game_picked_colors, game_alterd_two_player_rules)


# -------- Start the game --------

askPlayers()

# -------- Afsluiting --------
pg.quit()
