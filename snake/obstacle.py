import pygame
from block import *
from random import randint, choice

class OBS(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()

        self.image = pygame.Surface((30, 30))
        self.image.fill((115, 115, 115))    # grey
        self.rect = self.image.get_rect(center=position)
    
        # random direction
        self.direct_choose = choice(['horizontal', 'vertical'])
        self.horizontal_choose = choice(['right', 'left'])
        self.vertical_choose = choice(['up', 'down'])

        # moving
        self.speed = 2
        self.x_move = 0
        self.y_move = 0
        
        # time change direction
        self.time_change = randint(2 * 60, 4 * 60)
        
    def AI_obstacles(self):
        if self.direct_choose == 'horizontal':
            self.y_move = 0   

            if self.horizontal_choose == 'right':     
                self.x_move = +self.speed
            if self.horizontal_choose == 'left':
                self.x_move = -self.speed
          
        if self.direct_choose == 'vertical':
            self.x_move = 0

            if self.vertical_choose == 'up':
                self.y_move = -self.speed
            if self.vertical_choose == 'down':
                self.y_move = +self.speed
    

        self.rect.x += self.x_move
        self.rect.y += self.y_move

    def change_direction(self):
        self.time_change -= 1

        if self.time_change <= 0:
            self.direct_choose = choice(['horizontal', 'vertical'])
            self.horizontal_choose = choice(['right', 'left'])
            self.vertical_choose = choice(['up', 'down'])

            self.time_change = randint(2 * 60, 4 * 60)

    def obs_limitation(self):
    # vertical
        if self.x_move == 0:
            if self.y_move > 0 and self.rect.bottom >= scr_height:
                self.rect.bottom = scr_height
                self.direct_choose = choice(['horizontal', 'vertical', 'vertical'])  

                if self.direct_choose == 'vertical':
                    self.vertical_choose == 'up'
                

            if self.y_move < 0 and self.rect.top <= 0:
                self.rect.top = 0
                self.direct_choose = choice(['horizontal', 'vertical', 'vertical'])  

                if self.direct_choose == 'vertical':
                    self.vertical_choose == 'down'
                 
    # horizontal
        if self.y_move == 0:
            if self.x_move > 0 and self.rect.right >= scr_width:
                self.rect.right = scr_width
                self.direct_choose = choice(['horizontal', 'horizontal', 'vertical'])  

                if self.direct_choose == 'horizontal':
                    self.horizontal_choose == 'left'
                   

            if self.x_move < 0 and self.rect.left <= 0:
                self.rect.left = 0
                self.direct_choose = choice(['horizontal', 'horizontal', 'vertical'])  

                if self.direct_choose == 'horizontal':
                    self.horizontal_choose == 'right'
                          
    # collide with angles
        if self.rect.top <= 0: 
            self.rect.top = 0
        # top left
            if self.rect.left <= 0:
                self.rect.left = 0
                self.direct_choose = choice(['horizontal', 'vertical'])

                if self.direct_choose == 'horizontal':
                    self.y_move = 0
                    self.horizontal_choose = 'right'

                if self.direct_choose == 'vertical':
                    self.x_move = 0
                    self.vertical_choose = 'down'
        # top right
            if self.rect.right >= scr_height:
                self.rect.right = scr_height
                self.direct_choose = choice(['horizontal', 'vertical'])

                if self.direct_choose == 'horizontal':
                    self.y_move = 0
                    self.horizontal_choose = 'left'

                if self.direct_choose == 'vertical':
                    self.x_move = 0
                    self.vertical_choose = 'down'
                 

        if self.rect.bottom >= scr_height:
            self.rect.bottom = scr_height
        # bottom left
            if self.rect.left <= 0:
                self.rect.left = 0
                self.direct_choose = choice(['horizontal', 'vertical'])

                if self.direct_choose == 'horizontal':
                    self.y_move = 0
                    self.horizontal_choose = 'right'
              
                if self.direct_choose == 'vertical':
                    self.x_move = 0
                    self.vertical_choose = 'up'
        # bottom right
            if self.rect.right >= scr_height:
                self.rect.right = scr_height
                self.direct_choose = choice(['horizontal', 'vertical'])

                if self.direct_choose == 'horizontal':
                    self.y_move = 0
                    self.horizontal_choose = 'left'
             
                if self.direct_choose == 'vertical':
                    self.x_move = 0
                    self.vertical_choose = 'up'
            
                 
    def update(self):
        self.obs_limitation()
        self.change_direction()
        self.AI_obstacles()
        
      





