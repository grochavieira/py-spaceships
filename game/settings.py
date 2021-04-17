import pygame
import sys
import random

# Setup padrão
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

# Janela principal
screen_width = 960  # largura
screen_height = 720  # altura

# cria a janela do jogo
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ships")  # titulo

bg_color = pygame.Color("#333333")  # cor de fundo
font_color = pygame.Color("#ffffff") # cor da fonte
basic_font = pygame.font.Font("fonts/8-BIT-WONDER.ttf", 20)  # carrega a fonte

# sons de efeito
laser_sound = pygame.mixer.Sound(
    "audio/laser.wav")
destroy_sound = pygame.mixer.Sound("audio/destroy.wav")
hit_sound = pygame.mixer.Sound("audio/hit.wav")
button_sound = pygame.mixer.Sound("audio/button.wav") 

# score do jogo
score = 0