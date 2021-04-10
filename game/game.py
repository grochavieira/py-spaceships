import pygame
import sys
import random
import settings
import engine

def start():
    spaceship = engine.Spaceship("assets/spaceship/ship", 4, settings.screen_width/2, settings.screen_height/2, 5, 0.10)

    spaceship_group = pygame.sprite.Group()
    spaceship_group.add(spaceship)

    

    farback = engine.Background("assets/backgrounds/farback.png", 0, 0, 3)
    stars = engine.Background("assets/backgrounds/stars.png", 0, 0, 1)
    background_group = pygame.sprite.Group()
    background_group.add(farback)
    background_group.add(stars)

    game_manager = engine.GameManager(spaceship_group, background_group)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # se apertou alguma tecla
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    spaceship.movement_y -= spaceship.speed
                if event.key == pygame.K_DOWN:
                    spaceship.movement_y += spaceship.speed
                if event.key == pygame.K_LEFT:
                    spaceship.movement_x -= spaceship.speed
                if event.key == pygame.K_RIGHT:
                    spaceship.movement_x += spaceship.speed

            # se soltou alguma tecla
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    spaceship.movement_y += spaceship.speed
                if event.key == pygame.K_DOWN:
                    spaceship.movement_y -= spaceship.speed
                if event.key == pygame.K_LEFT:
                    spaceship.movement_x += spaceship.speed
                if event.key == pygame.K_RIGHT:
                    spaceship.movement_x -= spaceship.speed
                

        settings.screen.fill(settings.bg_color)

        game_manager.run_game()
        pygame.display.update()
        settings.clock.tick(120)