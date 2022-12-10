import pygame
from block import *
from sounds import  element_unavailable_sound, element1_sound, element2_sound
from path import path



class PLAYER(pygame.sprite.Sprite):
    def __init__(self, position, player):
        super().__init__()

        self.player = player

        self.size = 30
        self.size_update = 0
        self.speed_update = 0
        self.speed = 4
        self.x_move = 0
        self.y_move = 0

        self.image = pygame.Surface((self.size, self.size))
        self.image.fill('white')
        self.rect = self.image.get_rect(center=position)

        self.player_boosting = False
        self.obs_eat_disability = False
        self.time_element_available = 0

        self.pixel_font = pygame.font.Font(path + "\Pixeled.ttf", 15)

# update player after eat element
    def player_information(self):
        self.image = pygame.Surface((self.size,self.size))
        self.image.fill('white')
        self.rect = self.image.get_rect(center=(self.rect.centerx,self.rect.centery))

        if self.y_move == 0:
            if self.x_move > 0:
                self.x_move = +self.speed
            if self.x_move < 0:
                self.x_move = -self.speed

        if self.x_move == 0:
            if self.y_move > 0:
                self.y_move = +self.speed
            if self.y_move < 0:
                self.y_move = -self.speed

    def player_update(self, size_update, speed_update):
    
        self.size_update = size_update # keep info  
        self.speed_update = speed_update

        self.size += self.size_update   # update player
        self.speed += self.speed_update

        self.player_information()
       
# reset player back 
    def player_reset(self):
        self.size -= self.size_update
        self.speed -= self.speed_update
        
        self.player_information()
       
    def player_controller(self, player):
        keys = pygame.key.get_pressed()

        if player == 1:
            if keys[pygame.K_RIGHT]:
                self.x_move = +self.speed
                self.y_move = 0
            if keys[pygame.K_LEFT]:
                self.x_move = -self.speed
                self.y_move = 0
            if keys[pygame.K_UP]:
                self.y_move = -self.speed
                self.x_move = 0
            if keys[pygame.K_DOWN]:
                self.y_move = +self.speed
                self.x_move = 0

        if player == 2:
            if keys[pygame.K_d]:
                self.x_move = +self.speed
                self.y_move = 0
            if keys[pygame.K_a]:
                self.x_move = -self.speed
                self.y_move = 0
            if keys[pygame.K_w]:
                self.y_move = -self.speed
                self.x_move = 0
            if keys[pygame.K_s]:
                self.y_move = +self.speed
                self.x_move = 0
            
        self.rect.x += self.x_move
        self.rect.y += self.y_move

    def player_limitation(self):
        if self.y_move == 0:
            if self.x_move > 0 and self.rect.left >= scr_width:
                self.rect.right = 0
            if self.x_move < 0 and self.rect.right <= 0:
                self.rect.left = scr_width

        if self.x_move == 0:
            if self.y_move > 0 and self.rect.top >= scr_height:
                self.rect.bottom = 0
            if self.y_move < 0 and self.rect.bottom <= 0:
                self.rect.top = scr_height

# collide with elements
    def player_boost(self, element_kind):
        self.element_kind = element_kind

        if self.element_kind == 'big_slow':
            self.time_element_available = 5 * 60

            if self.player_boosting == False:
                self.player_update(+10, -1)
            self.obs_eat_disability = True
            self.player_boosting = True
        
        if self.element_kind == 'small_fast':
            self.time_element_available = 5 * 60

            if self.player_boosting == False:
                self.player_update(-10, +2)
            self.player_boosting = True

    def player_boost_remain(self):
        if self.player_boosting == True:
            self.time_element_available -= 1
     

            if self.element_kind == 'big_slow':  # red color down
                if 4 * 60 < self.time_element_available <= 6 * 60:
                    self.image.fill((153, 38, 0))    
                elif 2 * 60 < self.time_element_available <= 4 * 60:
                    self.image.fill((230, 57, 0))
                elif 0 < self.time_element_available <= 2 * 60:
                    self.image.fill((255, 102, 51))

            if self.element_kind == 'small_fast':  # yellow color down
                if 4 * 60 < self.time_element_available <= 6 * 60:
                    self.image.fill((204, 204, 0))
                elif 2 * 60 < self.time_element_available <= 4 * 60:
                    self.image.fill((255, 255, 26))
                elif 0 < self.time_element_available <= 2 * 60:
                    self.image.fill((255, 255, 102))

            if self.time_element_available <= 0:
                element_unavailable_sound.play()
                element1_sound.stop()
                element2_sound.stop()
                self.player_reset()
                self.obs_eat_disability = False
                self.player_boosting = False

    def player_id(self, player_id):
        self.text_surf = self.pixel_font.render(player_id, True, 'white')
        self.text_rect = self.text_surf.get_rect(midbottom=self.rect.midtop)

    def update(self):
        if self.player == 1:
            self.player_controller(1)
            self.player_id('P1')

        if self.player == 2:
            self.player_controller(2)
            self.player_id('P2')

        self.player_limitation()
        self.player_boost_remain() 
    


        
       

        
            