import pygame
import sys
import random
import settings
import engine

def start():
    spaceship_group = pygame.sprite.Group()
    spaceship = engine.Spaceship("assets/spaceship/ship", 4, settings.screen_width/2, settings.screen_height/2, 1, 4, 0.10)
    spaceship_group.add(spaceship)

    laser_group = pygame.sprite.Group()

    enemy_group = pygame.sprite.Group()
    enemy = engine.Enemy("assets/enemies/enemy", 6, settings.screen_width, random.randint(50, settings.screen_height - 50), 0.8)
    enemy_group.add(enemy)

    background_group = pygame.sprite.Group()
    farback = engine.Background("assets/backgrounds/farback.png", 0, 0, 3)
    stars = engine.Background("assets/backgrounds/stars.png", 0, 0, 1)
    background_group.add(farback)
    background_group.add(stars)

    game_manager = engine.GameManager(spaceship_group, background_group, laser_group, enemy_group)

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
                if event.key == pygame.K_SPACE:
                    if(len(laser_group.sprites()) < 3):
                        pygame.mixer.Sound.play(settings.laser_sound)
                        new_laser = engine.Laser(
                            "assets/Laser.png", spaceship.rect.centerx + 50, spaceship.rect.centery, 5, enemy_group)
                        laser_group.add(new_laser)

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