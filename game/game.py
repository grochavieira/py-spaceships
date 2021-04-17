import pygame
import sys
import random
import settings
import engine

class GameState():
    def __init__(self):
        self.state = "menu"
        self.is_running = True
        self.rocket_group = pygame.sprite.GroupSingle()
        self.laser_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.background_group = pygame.sprite.Group()
        self.game_manager = engine.GameManager(self.rocket_group, self.background_group, self.laser_group, self.enemy_group)

        farback = engine.Background("assets/backgrounds/farback.png", 0, 0, 3)
        stars = engine.Background("assets/backgrounds/stars.png", 0, 0, 1)
        self.background_group.add(farback)
        self.background_group.add(stars)

    def state_manager(self):
        if self.state == "menu":
            self.menu()
        elif self.state == "lost_level":
            self.lost_level()
        elif self.state == "singleplayer":
            self.singleplayer()
        elif self.state == "multiplayer":
            self.multiplayer()
    
    def menu(self):
        self.is_running = True
        title = engine.Text("assets/title/title", 4,
                            settings.screen_width/2, 100, 1, 0.07)

        text_group = pygame.sprite.Group()
        text_group.add(title)

        singleplayer_button = engine.Button(
            "assets/sg_btn/singleplayer", 13, settings.screen_width/2, 400, 0.6, 0.07)
        
        multiplayer_button = engine.Button(
            "assets/mp_btn/multiplayer", 12, settings.screen_width/2, 550, 0.6, 0.07)

        button_group = pygame.sprite.Group()
        button_group.add(singleplayer_button)
        button_group.add(multiplayer_button)

        mouse = engine.Mouse()
        mouse_group = pygame.sprite.Group()
        mouse_group.add(mouse)

        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # se apertou alguma tecla
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = "menu"
                        self.is_running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.sprite.spritecollide(mouse, button_group, False):
                        collision_button = pygame.sprite.spritecollide(
                            mouse, button_group, False)[0].rect
                        print(collision_button.bottom)
                        if collision_button.bottom <= 600:
                            settings.button_sound.play()
                            self.state = "singleplayer"
                            self.is_running = False
                        elif collision_button.bottom <= 800:
                            settings.button_sound.play()
                            self.state = "menu"
                            self.is_running = False
                        
            
            self.background_group.draw(settings.screen)
            self.background_group.update()

            button_group.draw(settings.screen)
            text_group.draw(settings.screen)
            mouse_group.draw(settings.screen)

            button_group.update()
            text_group.update()
            mouse_group.update()

            pygame.display.update()
            settings.clock.tick(120)

    def singleplayer(self):
        self.is_running = True
        rocket = engine.Rocket("assets/rocket/ship", 4, settings.screen_width/2, settings.screen_height/2, 1, 4, 0.10)
        self.rocket_group.add(rocket)

        spawn_enemy_timer = pygame.time.get_ticks()

        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # se apertou alguma tecla
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = "menu"
                        self.game_manager.reset_game()
                        self.is_running = False
                        
                    if event.key == pygame.K_UP:
                        rocket.movement_y -= rocket.speed
                    if event.key == pygame.K_DOWN:
                        rocket.movement_y += rocket.speed
                    if event.key == pygame.K_LEFT:
                        rocket.movement_x -= rocket.speed
                    if event.key == pygame.K_RIGHT:
                        rocket.movement_x += rocket.speed
                    if event.key == pygame.K_SPACE:
                        if(len(self.laser_group.sprites()) < 3):
                            pygame.mixer.Sound.play(settings.laser_sound)
                            new_laser = engine.Laser(
                                "assets/Laser.png", rocket.rect.centerx + 50, rocket.rect.centery, 5, self.enemy_group)
                            self.laser_group.add(new_laser)

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
                enemy = engine.Enemy("assets/enemies/enemy", 6, settings.screen_width, random.randint(50, settings.screen_height - 50), random.uniform(0.8, 1.3), self.rocket_group)
                self.enemy_group.add(enemy)
                spawn_enemy_timer = pygame.time.get_ticks()


            settings.screen.fill(settings.bg_color)

            self.game_manager.run_game()
            pygame.display.update()
            settings.clock.tick(120)