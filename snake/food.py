import pygame
from block import *
from random import randint, choice


class FOOD(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((20, 20))
        self.image.fill((140, 255, 26)) # green
        self.rect = self.image.get_rect(center=(randint(20, scr_width - 20), randint(20, scr_height - 20)))

class ELEMENTS(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        # multi-color rare food
        self.green_1 = (204, 255, 153)
        self.green_2 =  (191, 255, 128)
        self.green_3 = (179, 255, 102)
        self.green_4 = (166, 255, 77)
        self.green_5 = (153, 255, 51)
        self.green_6 = (140, 255, 26)
     
        self.color_animation = [self.green_1, self.green_2, self.green_3, self.green_4, self.green_5, self.green_6]
        self.color_index = 0

        self.image = pygame.Surface((20, 20))
        self.image.fill(self.color_animation[self.color_index])
        self.rect = self.image.get_rect(center=(randint(20, scr_width - 20), randint(20, scr_height - 20)))

        # random elements
        self.element_kind = choice(['rare_food', 'rare_food', 'big_slow', 'small_fast', 'small_fast'])
        # self.element_kind = 'big_slow'
        self.time_spawn = 0

    def rare_food(self):
        self.color_index += 0.1
        if self.color_index >= len(self.color_animation):
            self.color_index = 0
    
        self.image.fill(self.color_animation[int(self.color_index)])
    
    def random_element(self):
      
        if self.element_kind == 'rare_food':    self.rare_food()    # multi-color
        if self.element_kind == 'big_slow':    self.image.fill((204, 51, 0))   # red
        if self.element_kind == 'small_fast':   self.image.fill((255, 255, 0))  # yellow
              
    def update(self):
        self.random_element()

class SOUL(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()

        # colors - sky blue
        self.blue_1 = (0, 179, 179)
        self.blue_2 = (0, 204, 204)
        self.blue_3 = (0, 230, 230)
        self.blue_4 = (0, 255, 255)
        self.blue_5 = (26, 255, 255)

        self.color_animation = [self.blue_1, self.blue_2, self.blue_3, self.blue_4, self.blue_5]
        self.color_index = 0

        self.image = pygame.Surface((20, 20))
        self.image.fill(self.color_animation[self.color_index]) 
        self.rect = self.image.get_rect(center=position)

    def multi_color(self):
        self.color_index += 0.1

        if self.color_index >= len(self.color_animation):
            self.color_index = 0
        self.image.fill(self.color_animation[int(self.color_index)]) 

    def limitation(self):
    # right-left
        if self.rect.right >= scr_width: self.rect.right = scr_width
        if self.rect.left <= 0: self.rect.left = 0
    # top_bottom
        if self.rect.top <= 0:  self.rect.top = 0 
        if self.rect.bottom >= scr_height:  self.rect.bottom = scr_height

    def update(self):
        self.limitation()
        self.multi_color()