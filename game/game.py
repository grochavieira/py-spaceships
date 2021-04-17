import pygame
import sys
import random
import settings
import engine

class GameState():
    def __init__(self):
        self.state = "menu"
        self.is_running = True
        self.rocket_group = pygame.sprite.Group()
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
                        if collision_button.bottom <= 500:
                            settings.button_sound.play()
                            print("singleplayer")
                            self.state = "singleplayer"
                            self.is_running = False
                        elif collision_button.bottom <= 800:
                            settings.button_sound.play()
                            print("multiplayer")
                            self.state = "multiplayer"
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
    
    def lost_level(self):
        self.is_running = True

        lost_level_text = settings.basic_font.render(
            "Your total score is " + str(settings.score), True, settings.font_color)
        lost_level_text_rect = lost_level_text.get_rect(
            center=(settings.screen_width/2, settings.screen_height/2 - 50))

        press_space_text = settings.basic_font.render(
            "Press space to return to the menu", True, settings.font_color)
        press_space_text_rect = press_space_text.get_rect(
            center=(settings.screen_width/2, settings.screen_height/2 + 50))

        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        settings.score = 0
                        self.state = "menu"
                        self.is_running = False

            self.background_group.draw(settings.screen)
            self.background_group.update()

            settings.screen.blit(lost_level_text, lost_level_text_rect)
            settings.screen.blit(press_space_text, press_space_text_rect)
            pygame.display.update()
            settings.clock.tick(120)

    def singleplayer(self):
        self.is_running = True
        settings.score = 0

        self.game_manager.reset_game()
        rocket = engine.Rocket("assets/rocket/ship", 4, 100, settings.screen_height/2, 1, 4, 0.10)
        self.rocket_group.add(rocket)

        slow_time_text = settings.basic_font.render(
            "press enter to slow time", True, settings.font_color)
        slow_time_text_rect = slow_time_text.get_rect(
            center=(settings.screen_width/2 + 100, 10))

        spawn_enemy_timer = pygame.time.get_ticks()

        while self.is_running:
            if (rocket.life <= 0):
                self.state = "lost_level"
                self.game_manager.reset_game()
                self.is_running = False

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

                    if event.key == pygame.K_RETURN:
                        if(not self.game_manager.can_slow_time and settings.score - self.game_manager.score_before_slow_time >= 5000):
                            self.game_manager.can_slow_time = True
                            self.game_manager.slowed_time = pygame.time.get_ticks()
                            self.game_manager.slow_time()
                        
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
                enemy = engine.Enemy("assets/enemies/enemy", 6, settings.screen_width, random.randint(120, settings.screen_height - 50), random.uniform(0.8, 1.3), self.rocket_group)
                self.enemy_group.add(enemy)
                spawn_enemy_timer = pygame.time.get_ticks()

            self.game_manager.run_game()

            if(not self.game_manager.can_slow_time and settings.score - self.game_manager.score_before_slow_time >= 5000):
                settings.screen.blit(slow_time_text, slow_time_text_rect)

            pygame.display.update()
            settings.clock.tick(120)
    
    def multiplayer(self):
        self.is_running = True
        settings.score = 0

        rocket_player1 = engine.Rocket("assets/rocket/ship", 4, 100, settings.screen_height/2 - 100, 1, 4, 0.10)
        rocket_player2 = engine.Rocket("assets/rocket/ship", 4, 100, settings.screen_height/2 + 100, 1, 4, 0.10)
        self.rocket_group.add(rocket_player1)
        self.rocket_group.add(rocket_player2)

        slow_time_text = settings.basic_font.render(
            "press enter to slow time", True, settings.font_color)
        slow_time_text_rect = slow_time_text.get_rect(
            center=(settings.screen_width/2 + 200, 50))

        spawn_enemy_timer = pygame.time.get_ticks()

        while self.is_running:
            if (rocket_player1.life <= 0 or rocket_player2.life <= 0):
                self.state = "lost_level"
                self.game_manager.reset_game()
                self.is_running = False

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

                    if event.key == pygame.K_RETURN:
                        if(not self.game_manager.can_slow_time and settings.score - self.game_manager.score_before_slow_time >= 5000):
                            self.game_manager.can_slow_time = True
                            self.game_manager.slowed_time = pygame.time.get_ticks()
                            self.game_manager.slow_time()
                        
                    if event.key == pygame.K_UP:
                        rocket_player1.movement_y -= rocket_player1.speed
                    if event.key == pygame.K_DOWN:
                        rocket_player1.movement_y += rocket_player1.speed
                    if event.key == pygame.K_LEFT:
                        rocket_player1.movement_x -= rocket_player1.speed
                    if event.key == pygame.K_RIGHT:
                        rocket_player1.movement_x += rocket_player1.speed
                    if event.key == pygame.K_SPACE:
                        if(len(self.laser_group.sprites()) < 3):
                            pygame.mixer.Sound.play(settings.laser_sound)
                            new_laser = engine.Laser(
                                "assets/Laser.png", rocket_player1.rect.centerx + 50, rocket_player1.rect.centery, 5, self.enemy_group)
                            self.laser_group.add(new_laser)

                    if event.key == pygame.K_w:
                        rocket_player2.movement_y -= rocket_player2.speed
                    if event.key == pygame.K_s:
                        rocket_player2.movement_y += rocket_player2.speed
                    if event.key == pygame.K_a:
                        rocket_player2.movement_x -= rocket_player2.speed
                    if event.key == pygame.K_d:
                        rocket_player2.movement_x += rocket_player2.speed
                    if event.key == pygame.K_LSHIFT:
                        if(len(self.laser_group.sprites()) < 3):
                            pygame.mixer.Sound.play(settings.laser_sound)
                            new_laser = engine.Laser(
                                "assets/Laser.png", rocket_player2.rect.centerx + 50, rocket_player2.rect.centery, 5, self.enemy_group)
                            self.laser_group.add(new_laser)

                # se soltou alguma tecla
                if event.type == pygame.KEYUP:
                    # movimentação do player 1
                    if event.key == pygame.K_UP:
                        rocket_player1.movement_y += rocket_player1.speed
                    if event.key == pygame.K_DOWN:
                        rocket_player1.movement_y -= rocket_player1.speed
                    if event.key == pygame.K_LEFT:
                        rocket_player1.movement_x += rocket_player1.speed
                    if event.key == pygame.K_RIGHT:
                        rocket_player1.movement_x -= rocket_player1.speed
                    
                    # movimentação do player 2
                    if event.key == pygame.K_w:
                        rocket_player2.movement_y += rocket_player2.speed
                    if event.key == pygame.K_s:
                        rocket_player2.movement_y -= rocket_player2.speed
                    if event.key == pygame.K_a:
                        rocket_player2.movement_x += rocket_player2.speed
                    if event.key == pygame.K_d:
                        rocket_player2.movement_x -= rocket_player2.speed
                    
            current_time = pygame.time.get_ticks()

            if(current_time - spawn_enemy_timer >= 950):
                enemy = engine.Enemy("assets/enemies/enemy", 6, settings.screen_width, random.randint(120, settings.screen_height - 50), random.uniform(0.8, 1.3), self.rocket_group)
                self.enemy_group.add(enemy)
                spawn_enemy_timer = pygame.time.get_ticks()

            self.game_manager.run_game()
            
            if(not self.game_manager.can_slow_time and settings.score - self.game_manager.score_before_slow_time >= 5000):
                settings.screen.blit(slow_time_text, slow_time_text_rect)

            pygame.display.update()
            settings.clock.tick(120)