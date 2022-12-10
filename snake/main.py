import pygame
import sys
from block import *
from player import PLAYER
from food import FOOD, ELEMENTS, SOUL
from path import path
from obstacle import OBS
from random import randint, choice
from sounds import *


class GAME():
    def __init__(self, play_mode):
        super().__init__()

        # player
        self.play_mode = play_mode
        self.player_group = pygame.sprite.Group()

        if self.play_mode == 'single':
            self.player_group.add(PLAYER((scr_width/2, scr_height/2), 1))

        elif self.play_mode == 'team up':
            self.player_group.add(PLAYER((scr_width/2-100, scr_height/2), 2))
            self.player_group.add(PLAYER((scr_width/2+100, scr_height/2), 1))

            # soul
            self.player1_died = False
            self.player2_died = False


        self.soul_group = pygame.sprite.GroupSingle()
      
        # score
        self.pixel_font = pygame.font.Font(path + "\Pixeled.ttf", 15)
        self.score_count = 0

        # food
        self.food_group = pygame.sprite.GroupSingle(FOOD())

        # element
        self.elements_group = pygame.sprite.GroupSingle(ELEMENTS())
        self.time_spawn_element = 10 * 60    # 10 seconds
 
        # AI obstacle
        self.obstacles_group = pygame.sprite.Group(
            OBS((choice([scr_width+20, -20]), choice([-20, scr_height+20]))))
        self.obs_spawn_available = 0

         
    def spawn_obstacle(self):
        for obstacle in self.obstacles_group:
            if self.obs_spawn_available >= 2:
                obs_spawn_sound.play()
                self.obstacles_group.add(
                    OBS((obstacle.rect.centerx, obstacle.rect.centery)))

                self.obs_spawn_available = 0

        else:
            if self.obs_spawn_available >= 2:
                obs_spawn_sound.play()
                self.obstacles_group.add(
                OBS((choice([scr_width+20, -20]), choice([-20, scr_height+20]))))
                self.obs_spawn_available = 0

    def score_display(self):
        score_surf = self.pixel_font.render(
            "SCORE: " + str(self.score_count), True, 'white')
        score_rect = score_surf.get_rect(topleft=(0, -10))
        screen.blit(score_surf, score_rect)

    def collision_check(self):
        global play_scr, lose_scr
        for self.player in self.player_group:
            # with food
            if pygame.sprite.spritecollide(self.player, self.food_group, True):
                eat_sound.play()
                self.obs_spawn_available += 1
                self.score_count += 1
                self.food_group.add(FOOD())

            # with obs
            obs_hit = pygame.sprite.spritecollide(self.player, self.obstacles_group, False)
            if obs_hit:
                if self.player.obs_eat_disability == False:

                    if self.play_mode == 'team up':
                        died_sound.stop()
                        died_sound.play()

                        if self.player.player == 1:
                            self.player1_died = True
                            
                        if self.player.player == 2:
                            self.player2_died = True
                        
                        self.player.kill()
                        self.soul_group.add(SOUL(self.player.rect.center))

                        if self.player1_died == self.player2_died == True:
                            gameplay_sound2.stop()
                            lose_sound.play()
                            lose_scr = True
                            play_scr = False
    

                    if self.play_mode == 'single':
                        gameplay_sound2.stop()
                        lose_sound.play()
                        lose_scr = True
                        play_scr = False
    

                elif self.player.obs_eat_disability == True:
                    for obs in obs_hit:
                        obs_kill_sound.play()
                        obs.kill()

            # with soul - revive
            if pygame.sprite.spritecollide(self.player, self.soul_group, False):
       
                if self.player1_died == True and self.player.player == 2 and self.player2_died == False:
                            self.player_group.add(PLAYER(self.soul_group.sprite.rect.center, 1))
                            self.soul_group.empty()
                            revive_sound.stop()
                            revive_sound.play() 
                            self.player1_died = False
                            
                if self.player2_died == True and self.player.player == 1 and self.player1_died == False:
                            self.player_group.add(PLAYER(self.soul_group.sprite.rect.center, 2))
                            self.soul_group.empty()
                            revive_sound.stop()
                            revive_sound.play() 
                            self.player2_died = False
                        
                    
            # with elements
            element_hit = pygame.sprite.spritecollide(self.player, self.elements_group, True)
            if element_hit:
                eat_sound.play()
                for self.element in element_hit:

                    if self.element.element_kind == 'rare_food':
                        self.obs_spawn_available += 1
                        self.score_count += 3

                    if self.element.element_kind == 'big_slow':
                        element1_sound.play()
                        self.player.player_boost('big_slow')

                    if self.element.element_kind == 'small_fast':
                        element2_sound.play()
                        self.player.player_boost('small_fast')

                         
    def spawn_elements(self):
        self.time_spawn_element -= 1

        if self.time_spawn_element <= 0:
            self.elements_group.add(ELEMENTS())
            self.time_spawn_element = 10 * 60


    def run(self):
        # player
        self.player_group.draw(screen)
        self.player_group.update()
        
        # identify player
        for player in self.player_group:
            screen.blit(player.text_surf, player.text_rect)

        # soul player
        self.soul_group.draw(screen)
        self.soul_group.update()

        # food
        self.food_group.draw(screen)

        # elements
        self.spawn_elements()
        self.elements_group.draw(screen)
        self.elements_group.update()

        # obstacles
        self.spawn_obstacle()
        self.obstacles_group.draw(screen)
        self.obstacles_group.update()

        # score
        self.score_display()

        # collision
        self.collision_check()

    def reset(self):
        self.obstacles_group.empty()
        self.player_group.empty()
        
        self.player.obs_eat_disability = False
        self.player.player_boosting = False
        self.time_element_available = 0
        self.score_count = 0
        self.obs_spawn_available = 0

        self.obstacles_group.add(OBS((choice([20, scr_width-20]), randint(0, scr_height))))
        self.elements_group.add(ELEMENTS())
        self.food_group.add(FOOD())

        if self.play_mode == 'single':
            self.player_group.add(PLAYER((scr_width/2, scr_height/2), 1))

        elif self.play_mode == 'team up':
            self.player_group.add(PLAYER((scr_width/2-100, scr_height/2), 2))
            self.player_group.add(PLAYER((scr_width/2+100, scr_height/2), 1))

            self.player1_died = False
            self.player2_died = False


class CRT:
    def __init__(self):
        self.tv = pygame.image.load(path + '/tv.png').convert_alpha()
        self.tv = pygame.transform.scale(self.tv, (scr_width, scr_height))

    def create_crt_lines(self):
        line_height = 3
        line_amount = int(scr_height / line_height)
        for line in range(line_amount):
            y_pos = line * line_height
            pygame.draw.line(self.tv, 'black', (0, y_pos),
                             (scr_width, y_pos), 1)

    def draw(self):
        self.tv.set_alpha(randint(75, 90))
        self.create_crt_lines()
        screen.blit(self.tv, (0, 0))

# -----------------------------------------------------------------------------------------
if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Strange snake by TD")
    pygame.display.set_icon(pygame.image.load(path + "/icon.ico"))
    screen = pygame.display.set_mode((scr_width, scr_height))
    clock = pygame.time.Clock()

    gameplay_sound1.play(-1)    # replay when music is off

    game = GAME('single')   # default one player
    crt_scr = CRT()

# midtop
    def message(msg, position, size=15):
        pixel_font = pygame.font.Font(path + "\Pixeled.ttf", size)
        text_surf = pixel_font.render(msg, True, 'white')
        text_rect = text_surf.get_rect(midtop=(position))
        screen.blit(text_surf, text_rect)
#topleft
    def message_2(msg, position, size=15):
        pixel_font = pygame.font.Font(path + "\Pixeled.ttf", size)
        text_surf = pixel_font.render(msg, True, 'white')
        text_rect = text_surf.get_rect(topleft=(position))
        screen.blit(text_surf, text_rect)
    
    def logo(color, position, size=40):
        logo_surf = pygame.Surface((size,size))
        logo_surf.fill(color)
        logo_rect = logo_surf.get_rect(midtop=position)
        screen.blit(logo_surf, logo_rect)

    def screen_display(screen_display):
    # screen start
        if screen_display == 'screen start':
            # setting icon
            setting_surface = pygame.image.load(path + "/setting_icon.png").convert_alpha()
            setting_surface = pygame.transform.scale(setting_surface, (90, 90))
            setting_rect = setting_surface.get_rect(topleft=(0, 0))
            screen.blit(setting_surface, setting_rect)
            message_2("-s- SETTING", (90, 30), 10)

            
            logo('red', (scr_width/2-60, scr_height/2-20))
            logo('green', (scr_width/2, scr_height/2-20))
            logo('blue', (scr_width/2+60, scr_height/2-20))

            message('STRANGE SNAKE', (scr_width/2, scr_height/2+30))
            message('PRESS -SPACE- TO PLAY', (scr_width/2, scr_height/2+100))

    # screen lose
        elif screen_display == 'screen lose':
            message('YOUR SCORE: ' + str(game.score_count),
                    (scr_width/2, scr_height/2-50))
            message('LOSE -SPACE- PLAY AGAIN', (scr_width/2, scr_height/2))
            message("-ESC- BACK TO MAIN", (scr_width/2,scr_height/2+50))

    def upload_image(link_image, position):
        image = pygame.image.load(path + "/" + link_image).convert_alpha()
        image_rect = image.get_rect(midtop=position)
        screen.blit(image, image_rect)

    list_option = ["SINGLE", "TEAM UP"]
    list_index = 0

    def setting_screen():
    # control
        message("--HOW TO PLAY--", (scr_width/2, 0))
        # P2 - right
        message("-P2-", (scr_width/2-200, scr_height/10-10))
        upload_image("p2_control.png", (scr_width/2-200, scr_height/5))

        # P1 - left
        message("-P1-(DEFAULT)", (scr_width/2+200, scr_height/10-10))
        upload_image("p1_control.png", (scr_width/2+200, scr_height/5))

        # info elements, obs, point
        logo('grey', (scr_width/6, scr_height/2-60), 30)
        message_2("OBSTACLE", (scr_width/6+25,scr_height/2-70))

        logo('red', (scr_width/6, scr_height/2-20), 30)
        message_2("BIGGER-SLOWER-EAT OBSTACLE", (scr_width/6+25,scr_height/2-30))

        logo('yellow', (scr_width/6, scr_height/2+20), 30)
        message_2("SMALLER-FASTER", (scr_width/6+25,scr_height/2+10))

        logo('green', (scr_width/6, scr_height/2+60), 30)
        message_2("POINT", (scr_width/6+25,scr_height/2+50))

        # option
        global list_index, game
        if list_index == 1:
            game = GAME("team up")

        # info soul-revive
            logo((0, 255, 255), (scr_width/6, scr_height/2+100), 30)
            message_2("REVIVE YOUR MATE", (scr_width/6+25,scr_height/2+90))

        elif list_index > 1:
            list_index = 0
            game = GAME("single")

        message("-SPACE- PLAY MODE: " + str(list_option[list_index]), (scr_width/2, scr_height/2+200))
        message('-ENTER- SELECTED', (scr_width/2, scr_height-100))


    start_scr = True
    setting_scr = False
    play_scr = False
    lose_scr = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
            # to play screen
                if event.key == pygame.K_SPACE and start_scr == True:
                    gameplay_sound1.stop()
                    start_sound.play()
                    gameplay_sound2.play(-1)
                    play_scr = True
                    start_scr = False

                # to setting screen
                elif event.key == pygame.K_s and start_scr == True:
                    eat_sound.play()
                    setting_scr = True
                    start_scr = False

                # back to start screen
                elif event.key == pygame.K_RETURN and setting_scr == True: 
                    eat_sound.play()
                    start_scr = True     
                    setting_scr = False

                # play again
                elif event.key == pygame.K_SPACE and lose_scr == True and play_scr == False:
                    start_sound.play()
                    gameplay_sound2.play(-1)
                    game.reset() 
                    play_scr = True
                    lose_scr = False

                # back to main screen
                elif event.key == pygame.K_ESCAPE and play_scr == False and lose_scr == True:
                    eat_sound.play()
                    gameplay_sound2.stop()
                    gameplay_sound1.play(-1)
                    game.reset()
                    start_scr = True
                    lose_scr = False

                # select play mode
                elif event.key == pygame.K_SPACE and setting_scr == True:
                    eat_sound.play()
                    list_index += 1

        if start_scr == True:
            screen.fill((64, 64, 64))
            screen_display('screen start')
            crt_scr.draw()

        elif play_scr == True:
            screen.fill((64, 64, 64))
            game.run()
            crt_scr.draw()

        elif setting_scr == True:
            screen.fill((64, 64, 64))
            setting_screen()
            crt_scr.draw()

        elif lose_scr == True:
            screen_display('screen lose')
            

        pygame.display.update()
        clock.tick(60)
