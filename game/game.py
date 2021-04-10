import pygame
import sys
import random
import settings
import engine

def start():
    rocket_group = pygame.sprite.Group()
    rocket = engine.Rocket("assets/rocket/ship", 4, settings.screen_width/2, settings.screen_height/2, 1, 4, 0.10)
    rocket_group.add(rocket)

    laser_group = pygame.sprite.Group()

    enemy_group = pygame.sprite.Group()

    background_group = pygame.sprite.Group()
    farback = engine.Background("assets/backgrounds/farback.png", 0, 0, 3)
    stars = engine.Background("assets/backgrounds/stars.png", 0, 0, 1)
    background_group.add(farback)
    background_group.add(stars)

    game_manager = engine.GameManager(rocket_group, background_group, laser_group, enemy_group)

    spawn_enemy_timer = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # se apertou alguma tecla
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    rocket.movement_y -= rocket.speed
                if event.key == pygame.K_DOWN:
                    rocket.movement_y += rocket.speed
                if event.key == pygame.K_LEFT:
                    rocket.movement_x -= rocket.speed
                if event.key == pygame.K_RIGHT:
                    rocket.movement_x += rocket.speed
                if event.key == pygame.K_SPACE:
                    if(len(laser_group.sprites()) < 3):
                        pygame.mixer.Sound.play(settings.laser_sound)
                        new_laser = engine.Laser(
                            "assets/Laser.png", rocket.rect.centerx + 50, rocket.rect.centery, 5, enemy_group)
                        laser_group.add(new_laser)

            # se soltou alguma tecla
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    rocket.movement_y += rocket.speed
                if event.key == pygame.K_DOWN:
                    rocket.movement_y -= rocket.speed
                if event.key == pygame.K_LEFT:
                    rocket.movement_x += rocket.speed
                if event.key == pygame.K_RIGHT:
                    rocket.movement_x -= rocket.speed
                
        current_time = pygame.time.get_ticks()

        if(current_time - spawn_enemy_timer >= 1400):
            enemy = engine.Enemy("assets/enemies/enemy", 6, settings.screen_width, random.randint(50, settings.screen_height - 50), random.uniform(0.8, 1.3))
            enemy_group.add(enemy)
            spawn_enemy_timer = pygame.time.get_ticks()


        settings.screen.fill(settings.bg_color)

        game_manager.run_game()
        pygame.display.update()
        settings.clock.tick(120)