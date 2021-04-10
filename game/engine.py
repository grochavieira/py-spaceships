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
    def __init__(self, base_images_path, number_of_images, x_pos, y_pos, resize):
        super().__init__(base_images_path, number_of_images, x_pos, y_pos, resize)
        self.speed = random.uniform(0.8, 2) if resize <= 1.1  else random.uniform(0.5, 0.8)  # define a velocidade do inimigo
        self.sprite_speed = 0.07 # define a velocidade da troca de sprites
        self.initial_life = random.randint(1, 3) if resize <= 1.1  else random.randint(3, 6) # vida do inimigo
        self.life = self.initial_life

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
            self.rect.left = settings.screen_width - 50


class Rocket(AnimatedBlock):
    def __init__(self, base_images_path, number_of_images, x_pos, y_pos, resize, speed, sprite_speed):
        super().__init__(base_images_path, number_of_images, x_pos, y_pos, resize)
        self.speed = speed  # define a velocidade da espaçonave
        self.sprite_speed = sprite_speed # define a velocidade da troca de sprites
        self.movement_y = 0  # define a movimentação da espaçonave no eixo y
        self.movement_x = 0  # define a movimentação da espaçonave no eixo x

    # função para limitar até onde a espaçonave pode ir
    def screen_constrain(self):
        if self.rect.top <= 0:  
            self.rect.top = 0
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
    
    def draw_score(self):
        player_score = settings.basic_font.render(
            "SCORE " + str(settings.score), True, settings.font_color)

        player_score_rect = player_score.get_rect(
            midleft=(10, 20))

        settings.screen.blit(player_score, player_score_rect)
        
        
        