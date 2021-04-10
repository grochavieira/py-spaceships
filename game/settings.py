import pygame
import sys
import random

# Setup padrão
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

# Janela principal
screen_width = 1280  # largura
screen_height = 720  # altura

# cria a janela do jogo
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ships")  # titulo

bg_color = pygame.Color("#333333")  # cor de fundo