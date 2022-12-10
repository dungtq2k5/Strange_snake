from path import path
import pygame
pygame.init()

obs_spawn_sound = pygame.mixer.Sound(path + "/obs_spawn.wav")
obs_kill_sound = pygame.mixer.Sound(path + "/eat_obs.wav")
eat_sound = pygame.mixer.Sound(path + "/eat_sound.wav")
element1_sound = pygame.mixer.Sound(path + "/get_big.wav")
element2_sound = pygame.mixer.Sound(path + "/get_small.wav")
element_unavailable_sound = pygame.mixer.Sound(path + "/ele_unavailable.wav")
gameplay_sound2 = pygame.mixer.Sound(path + "/gameplay1.mp3")
gameplay_sound1 = pygame.mixer.Sound(path + "/gamplay2.wav")
start_sound = pygame.mixer.Sound(path + "/start_game.wav")
revive_sound = pygame.mixer.Sound(path + "/revive.wav")
died_sound = pygame.mixer.Sound(path + "/died.wav")
lose_sound = pygame.mixer.Sound(path + "/lose_sound.wav")