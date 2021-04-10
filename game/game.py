import pygame
import sys
import random
import settings
import engine

def start():
    spaceship = engine.Spaceship("assets/spaceship/ship", 4, settings.screen_width/2, settings.screen_height/2, 5, 0.10)

    spaceship_group = pygame.sprite.Group()
    spaceship_group.add(spaceship)

    game_manager = engine.GameManager(spaceship_group)

    farback = engine.Background("assets/backgrounds/farback.png", 0, 0, 3)
    stars = engine.Background("assets/backgrounds/stars.png", 0, 0, 1)
    background_group = pygame.sprite.Group()
    background_group.add(farback)
    background_group.add(stars)

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

        background_group.draw(settings.screen)
        background_group.update()
        
        # ******* BACKGROUND ANIMATION

        # rel_x = bg_x % background.get_rect().width
        # rel_x2 = bg_x2 % background_stars.get_rect().width
        # settings.screen.blit(background, (rel_x - background.get_rect().width, 0))
        # settings.screen.blit(background_stars, (rel_x2 - background_stars.get_rect().width, 0))
        
        # if rel_x < settings.screen_width:
        #     settings.screen.blit(background, (rel_x, 0))
            
        # if rel_x2 < settings.screen_width:
        #     settings.screen.blit(background_stars, (rel_x2, 0))
        # bg_x -= 2
        # bg_x2 -= 1

        # ******* BACKGROUND ANIMATION

        game_manager.run_game()
        pygame.display.update()
        settings.clock.tick(120)