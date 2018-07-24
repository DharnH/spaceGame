import pygame as pg
from PIL import ImageFont


pg.font.init()



 # Parent
class buttons_and_labels():

    def __init__(self, game_display, rectX, rectY, rectW, rectH, rectC, text, textC, font, size, bold, italic):
        self.game_display = game_display
        self.rectX = rectX
        self.rectY = rectY
        self.rectW = rectW
        self.rectH = rectH
        self.rectC = rectC
        self.text = text


        text_font = ImageFont.truetype(font.lower() + '.ttf', size)
        current_textW, current_textH = text_font.getsize(text)
        self.textX = rectX + ((rectW / 10) * 0.5)
        self.textY = rectY + ((rectH - current_textH) / 3.0)
        self.textY = rectY + ((rectH - size) / 2.5)
        self.textC = textC
        self.font = font
        self.size = size
        self.bold = bold
        self.italic = italic
        self.rect = pg.Rect(self.rectX, self.rectY, self.rectW, self.rectH)

    def draw(self):

        myfont = pg.font.SysFont(self.font, self.size, self.bold, self.italic)

        text_to_show = myfont.render(self.text, False, self.textC)

        pg.draw.rect(self.game_display, self.rectC, self.rect)

        self.game_display.blit(text_to_show, (self.textX, self.textY))

    def change_text(self, new_text):
        self.text = new_text




class buttons(buttons_and_labels):

    def __init__ (self, game_display, rectX, rectY, rectW, rectH, rectC, text, textC, font, size, bold, italic):
        super().__init__(game_display, rectX, rectY, rectW, rectH, rectC, text, textC, font, size, bold, italic)

        text_font = ImageFont.truetype(font.lower() + '.ttf', size)
        current_textW, current_textH = text_font.getsize(text)
        self.textX = rectX + ((rectW - current_textW) / 2.5)
        self.textY = rectY + ((rectH - current_textH) / 3.0)




class label(buttons_and_labels):

    def __init__ (self, game_display, rectX, rectY, rectW, rectH, rectC, text, textC, font, size, bold, italic):
        super().__init__(game_display, rectX, rectY, rectW, rectH, rectC, text, textC, font, size, bold, italic)



class custom_label_fix_pos_left(label):

    def __init__ (self, game_display, rectX, rectY, rectW, rectH, rectC, text, textC, font, size, bold, italic):
        super().__init__(game_display, rectX, rectY, rectW, rectH, rectC, text, textC, font, size, bold, italic)



class custom_label_fix_pos_center(buttons_and_labels):

    def __init__ (self, game_display, rectX, rectY, rectW, rectH, rectC, text, textC, font, size, bold, italic):
        super().__init__(game_display, rectX, rectY, rectW, rectH, rectC, text, textC, font, size, bold, italic)

        text_font = ImageFont.truetype(font.lower() + '.ttf', size)
        current_textW, current_textH = text_font.getsize(text)
        self.textX = rectX + ((rectW - current_textW) / 2.5)
        self.textY = rectY + ((rectH - current_textH) / 3.0)



class custom_label_custom_pos_left(label):

    def __init__ (self, game_display, rectX, rectY, rectW, rectH, rectC, text, textC, font, size, bold, italic):
        super().__init__(game_display, rectX, rectY, rectW, rectH, rectC, text, textC, font, size, bold, italic)



class custom_label_custom_pos_center(label):

    def __init__ (self, game_display, rectX, rectY, rectW, rectH, rectC, text, textC, font, size, bold, italic):
        super().__init__(game_display, rectX, rectY, rectW, rectH, rectC, text, textC, font, size, bold, italic)

        text_font = ImageFont.truetype(font.lower() + '.ttf', size)
        current_textW, current_textH = text_font.getsize(text)
        self.textX = rectX + ((rectW - current_textW) / 2.5)
        self.textY = rectY + ((rectH - current_textH) / 3.0)



class custom_label_custom_pos_custom_text_pos(label):

    def __init__ (self, game_display, rectX, rectY, rectW, rectH, rectC, text, textC, textX, textY, font, size, bold, italic):
        super().__init__(game_display, rectX, rectY, rectW, rectH, rectC, text, textC, font, size, bold, italic)


        text_font = ImageFont.truetype(font.lower() + '.ttf', size)
        current_textW, current_textH = text_font.getsize(text)

        if textX != 'center':
            self.textX = textX
        else:
            self.textX = rectX + ((rectW - current_textW) / 2.5)


        if textY != 'center':
            self.textY = textY
        else:
            self.textY = rectY + ((rectH - current_textH) / 3.0)





class menu_bar(label):

    def __init__(self, game_display, rectX, rectY, rectW, rectH, rectC, barC, max_nr, current_nr, text, textC, font, size, bold, italic):
        super().__init__(game_display, rectX, rectY, rectW, rectH, rectC, text, textC, font, size, bold, italic)

        self.front_barC = barC
        self.max_nr = max_nr
        self.current_nr = current_nr

        self.background_barC = rectC


        self.background_barX = rectX
        self.background_barY = rectY
        self.background_barW = rectW
        self.background_barH = rectH


        self.front_barX = rectX
        self.front_barY = rectY
        if rectW * (current_nr / max_nr) > self.background_barW:
            self.front_barW = self.background_barW
        else:
            self.front_barW = rectW * (current_nr / max_nr)
        self.front_barH = rectH



        self.background_bar = pg.Rect(self.background_barX, self.background_barY, self.background_barW, self.background_barH)
        self.front_bar = pg.Rect(self.front_barX, self.front_barY, self.front_barW, self.front_barH)

    def change_current_max(self):
        self.current_nr = self.max_nr

    def change_current_set(self, set_nr):
        self.current_nr = set_nr

    def change_current_sub(self, sub_nr):
        if self.current_nr - sub_nr < 0:
            self.current_nr = 0
        else:
            self.current_nr -= sub_nr



class menu_bar_max(menu_bar):


    def __init__(self, game_display, rectX, rectY, rectW, rectH, rectC, barC, max_nr, current_nr, text, textC, font, size, bold, italic):
        super().__init__(game_display, rectX, rectY, rectW, rectH, rectC, barC, max_nr, current_nr, text, textC, font, size, bold, italic)

    def change_current_add(self, add_nr):
        if self.current_nr + add_nr > self.max_nr:
            self.current_nr = self.max_nr
        else:
            self.current_nr += add_nr




    def draw(self):

        myfont = pg.font.SysFont(self.font, self.size, self.bold, self.italic)

        self.text_with_nr = self.text + '   ' + str(self.current_nr) + ' / ' + str(self.max_nr)

        self.text_to_show = myfont.render(self.text_with_nr, False, self.textC)

        if self.background_barW * (self.current_nr / self.max_nr) > self.background_barW:
            self.front_barW = self.background_barW
        else:
            self.front_barW = self.background_barW * (self.current_nr / self.max_nr)
        self.front_bar = pg.Rect(self.front_barX, self.front_barY, self.front_barW, self.front_barH)


        pg.draw.rect(self.game_display, self.background_barC, self.background_bar)
        pg.draw.rect(self.game_display, self.front_barC, self.front_bar)
        self.game_display.blit(self.text_to_show, (self.textX, self.textY))



class menu_bar_no_lim(menu_bar):


    def __init__(self, game_display, rectX, rectY, rectW, rectH, rectC, barC, max_nr, current_nr, over_max_text, text, textC, font, size, bold, italic):
        super().__init__(game_display, rectX, rectY, rectW, rectH, rectC, barC, max_nr, current_nr, text, textC, font, size, bold, italic)

        self.over_max_text = over_max_text


    def change_current_add(self, add_nr):
        self.current_nr += add_nr




    def draw(self):

        myfont = pg.font.SysFont(self.font, self.size, self.bold, self.italic)


        if self.current_nr >= self.max_nr:
            self.text_with_nr = self.text + '   ' + str(self.current_nr) + ' / ' + str(self.max_nr) + '  ' + self.over_max_text

        else:
            self.text_with_nr = self.text + '   ' + str(self.current_nr) + ' / ' + str(self.max_nr)

        self.text_to_show = myfont.render(self.text_with_nr, False, self.textC)

        if self.background_barW * (self.current_nr / self.max_nr) > self.background_barW:
            self.front_barW = self.background_barW
        else:
            self.front_barW = self.background_barW * (self.current_nr / self.max_nr)
        self.front_bar = pg.Rect(self.front_barX, self.front_barY, self.front_barW, self.front_barH)


        pg.draw.rect(self.game_display, self.background_barC, self.background_bar)
        pg.draw.rect(self.game_display, self.front_barC, self.front_bar)
        self.game_display.blit(self.text_to_show, (self.textX, self.textY))


class global_var():

    def __init__(self, state):
        self.state = state

    def change_state(self, new_state):
        self.state = new_state









class combat_enemy():

    def __init__(self, game_display, name, health_max, health_current, level):
        self.game_display = game_display
        self.name = name
        self.health_max = health_max
        self.health_current = health_current
        self.level = level



    def draw(self):
        myfont = pg.font.SysFont('Arial', 20, False, True)



    def change_current_add(self, add_nr):
        self.health_current += add_nr

    def change_current_max(self):
        self.health_current = self.health_max

    def change_current_set(self, set_nr):
        self.health_current = set_nr

    def change_current_sub(self, sub_nr):
        if self.health_current - sub_nr < 0:
            self.health_current = 0
        else:
            self.health_current -= sub_nr
