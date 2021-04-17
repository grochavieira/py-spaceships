import pygame
import sys
import random
import settings
import engine
import game

game_state = game.GameState()

while True:
    game_state.state_manager()