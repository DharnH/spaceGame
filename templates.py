



def template():
    while not planet_selected:
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                gv.end_game = True
                planet_selected = True

            elif ev.type == pg.MOUSEBUTTONUP:
                mpos = pg.mouse.get_pos()
                if ev.button == 1:
                    pass

        #update()
