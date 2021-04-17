import pygame
import sys
import random
import settings

class Block(pygame.sprite.Sprite):
    def __init__(self, image_path, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()  # carrega o sprite
        self.rect = self.image.get_rect(center=(x_pos, y_pos)) # desenha o retangulo em volta da imagem

class AnimatedBlock(pygame.sprite.Sprite): # classe base
    def __init__(self, base_images_path, number_of_images, x_pos, y_pos, resize):
        super().__init__()
        self.sprites = []

        for i in range(number_of_images):
            image_path = base_images_path + str(i + 1) + ".png"
            image = pygame.image.load(image_path).convert_alpha()
            resized_image = pygame.transform.scale(image, (int(image.get_rect().width * resize), int(image.get_rect().height * resize)))
            self.sprites.append(resized_image)

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.center = [x_pos, y_pos]

# classe dos lasers que são atirados pela espaçonave
class Laser(Block):
    def __init__(self, image_path, x_pos, y_pos, shoot_speed, enemy_group):
        super().__init__(image_path, x_pos, y_pos)
        self.is_active = False
        self.shoot_speed = shoot_speed
        self.enemy_group = enemy_group

    def update(self):
        self.rect.x += self.shoot_speed
        self.collision()

    def collision(self):
        if self.rect.right >= settings.screen_width:
            self.kill()

        # definição da colisão
        if pygame.sprite.spritecollide(self, self.enemy_group, False):
            collided_enemies = pygame.sprite.spritecollide(
                self, self.enemy_group, False)

            settings.score += 100 * len(collided_enemies)
            pygame.mixer.Sound.play(settings.destroy_sound)

            for collided_enemy in collided_enemies:
                self.kill()
                if collided_enemy.life - 1 == 0:
                    settings.score += 100 * collided_enemy.initial_life

                collided_enemy.life -= 1


class Enemy(AnimatedBlock):
    def __init__(self, base_images_path, number_of_images, x_pos, y_pos, resize, rocket_group):
        super().__init__(base_images_path, number_of_images, x_pos, y_pos, resize)
        self.speed = random.uniform(0.8, 2) * settings.slow_time if resize <= 1.1  else random.uniform(0.5, 0.8) * settings.slow_time  # define a velocidade do inimigo
        self.sprite_speed = 0.07 * settings.slow_time # define a velocidade da troca de sprites
        self.initial_life = random.randint(1, 3) if resize <= 1.1  else random.randint(3, 6) # vida do inimigo
        self.life = self.initial_life
        self.rocket_group = rocket_group

    def update(self):
        self.rect.x -= self.speed  # movimenta a espaçonave no eixo x
        
        self.current_sprite += self.sprite_speed

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]

        if(self.life == 0):
            self.kill()
        
        self.collisions()
    
    def collisions(self):
        if self.rect.left <= 0:
            pygame.mixer.Sound.play(settings.hit_sound) # toca o som de hit
            for rocket in self.rocket_group.sprites():
                rocket.life -= 1
            self.kill()

        if pygame.sprite.spritecollide(self, self.rocket_group, False):
            pygame.mixer.Sound.play(settings.hit_sound) # toca o som de hit

            collided_rockets = pygame.sprite.spritecollide(self, self.rocket_group, False)

            for collided_rocket in collided_rockets:
                collided_rocket.life -= 1
            
            self.kill()


class Rocket(AnimatedBlock):
    def __init__(self, base_images_path, number_of_images, x_pos, y_pos, resize, speed, sprite_speed):
        super().__init__(base_images_path, number_of_images, x_pos, y_pos, resize)
        self.speed = speed  # define a velocidade da espaçonave
        self.sprite_speed = sprite_speed # define a velocidade da troca de sprites
        self.movement_y = 0  # define a movimentação da espaçonave no eixo y
        self.movement_x = 0  # define a movimentação da espaçonave no eixo x
        self.life = 3 # Define a quantidade de vidas do rocket

    # função para limitar até onde a espaçonave pode ir
    def screen_constrain(self):
        if self.rect.top <= 120:  
            self.rect.top = 120
        if self.rect.bottom >= settings.screen_height:
            self.rect.bottom = settings.screen_height 
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= settings.screen_width:
            self.rect.right = settings.screen_width
    
    def update(self):
        self.rect.y += self.movement_y  # movimenta a espaçonave np eixo y
        self.rect.x += self.movement_x  # movimenta a espaçonave no eixo x
        
        self.current_sprite += self.sprite_speed

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]
        
        self.screen_constrain() 

class Background(Block):
    def __init__(self, image_path, x_pos, y_pos, moving_speed):
        super().__init__(image_path, x_pos, y_pos)
        self.moving_speed = moving_speed
        self.moving_x = 0
        self.relative_x = 0
    
    def update(self):
        self.moving_x -= self.moving_speed
        self.relative_x = self.moving_x % self.rect.width
        settings.screen.blit(self.image, (self.relative_x - self.rect.width, 0))

        if self.relative_x < settings.screen_width:
            settings.screen.blit(self.image, (self.relative_x, 0))



class GameManager():
    def __init__(self, rocket_group, background_group, laser_group, enemy_group):
        self.rocket_group = rocket_group
        self.background_group = background_group
        self.laser_group = laser_group
        self.enemy_group = enemy_group
        self.can_slow_time = False
        self.slowed_time = 0
        self.score_before_slow_time = 0
    
    def run_game(self):
        self.background_group.draw(settings.screen)
        self.background_group.update()
        
        self.rocket_group.draw(settings.screen)
        self.laser_group.draw(settings.screen)
        self.enemy_group.draw(settings.screen)

        self.rocket_group.update()
        self.laser_group.update()
        self.enemy_group.update()

        self.draw_score()
        self.draw_life()

        if(self.can_slow_time):
            self.restart_slow_timer()
        
    def slow_time(self):
        pygame.mixer.Sound.play(settings.slow_time_sound)

        for background in self.background_group.sprites():
            background.moving_speed *= 0.5
        
        for enemy in self.enemy_group.sprites():
            enemy.speed *= 0.5
            enemy.sprite_speed *= 0.5
        
        settings.slow_time = 0.5
    
    def reset_time(self):
        pygame.mixer.Sound.play(settings.time_resume_sound)

        for background in self.background_group.sprites():
            background.moving_speed *= 2
        
        for enemy in self.enemy_group.sprites():
            enemy.speed *= 2
            enemy.sprite_speed *= 2
        
        settings.slow_time = 1
        self.score_before_slow_time = settings.score
    
    def restart_slow_timer(self):
        current_time = pygame.time.get_ticks()  
        countdown_number = 10

        if current_time - self.slowed_time <= 700:
            countdown_number = 10
        if 700 < current_time - self.slowed_time <= 1400:
            countdown_number = 9
        if 1400 < current_time - self.slowed_time <= 2100:
            countdown_number = 8
        if 2100 < current_time - self.slowed_time <= 2800:
            countdown_number = 7
        if 2800 < current_time - self.slowed_time <= 3500:
            countdown_number = 6
        if 3500 < current_time - self.slowed_time <= 4200:
            countdown_number = 5
        if 4200 < current_time - self.slowed_time <= 4900:
            countdown_number = 4
        if 4900 < current_time - self.slowed_time <= 5600:
            countdown_number = 3
        if 5600 < current_time - self.slowed_time <= 6300:
            countdown_number = 2
        if 6300 < current_time - self.slowed_time <= 7000:
            countdown_number = 1
        if current_time - self.slowed_time >= 7000:
            countdown_number = 0
            self.reset_time()
            self.can_slow_time = False

        time_counter = settings.basic_font.render(
            str(countdown_number), True, settings.font_color)
        time_counter_rect = time_counter.get_rect(
            center=(settings.screen_width/2, settings.screen_height/2 + 50))
        settings.screen.blit(time_counter, time_counter_rect)

    def reset_game(self):
        for rocket in self.rocket_group.sprites():
            rocket.kill()

        for laser in self.laser_group.sprites():
            laser.kill()
        
        for enemy in self.enemy_group.sprites():
            enemy.kill()
    
    def draw_score(self):
        player_score = settings.basic_font.render(
            "SCORE " + str(settings.score), True, settings.font_color)

        player_score_rect = player_score.get_rect(
            midleft=(10, 20))

        settings.screen.blit(player_score, player_score_rect)
        
        
    def draw_heart(self, life, index):
        heart = pygame.image.load('assets/life.png')
        heartScaled = pygame.transform.scale(heart, (40, 25))
        if (life >= 5):
            settings.screen.blit(heartScaled, (310, 50 * index))
        if (life >= 4):
            settings.screen.blit(heartScaled, (270, 50 * index))
        if (life >= 3):
            settings.screen.blit(heartScaled, (230, 50 * index))
        if (life >= 2):
            settings.screen.blit(heartScaled, (190, 50 * index))
        if (life >= 1):
            settings.screen.blit(heartScaled, (150, 50 * index))

    def draw_life(self):
        if len(self.rocket_group.sprites()) > 0:
            for index, rocket in enumerate(self.rocket_group.sprites()):
                index += 1

                lifes_text = settings.basic_font.render(
                    "LIFES P" + str(index), True, settings.font_color)

                if(index >= 2):
                    index = 1.7

                self.draw_heart(rocket.life, index)

                lifes_text_rect = lifes_text.get_rect(
                    midleft=(10, 60 * index))

                settings.screen.blit(lifes_text, lifes_text_rect)

class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([1, 1])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

class Button(AnimatedBlock):
    def __init__(self, base_images_path, number_of_images, x_pos, y_pos, resize, sprite_speed):
        super().__init__(base_images_path, number_of_images, x_pos, y_pos, resize)
        self.sprite_speed = sprite_speed

    def update(self):
        self.current_sprite += self.sprite_speed

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]

class Text(AnimatedBlock):
    def __init__(self, base_images_path, number_of_images, x_pos, y_pos, resize, sprite_speed):
        super().__init__(base_images_path, number_of_images, x_pos, y_pos, resize)
        self.sprite_speed = sprite_speed

    def update(self):
        self.current_sprite += self.sprite_speed

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]