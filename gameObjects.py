import os
import pygame

from settings import (
    screenWidth, screenHeight, fps, 
    COLOR_BG, COLOR_COIN, COLOR_PLAYER, COLOR_TEXT, 
    jumpHeight, gravity, playerSpeed, COLOR_PLATFORM
)

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(COLOR_PLATFORM)
        self.rect = self.image.get_rect(topleft=(x, y))

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, COLOR_COIN, (0, 0, width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()


        frame_names = [
            "1.png", "2.png", "3.png", "4.png"
        ]

        self.walk_frames_right = []
        for name in frame_names:
            path = os.path.join("images", "player", name)
            img = pygame.image.load(path).convert_alpha()
            img = img.subsurface(img.get_bounding_rect()).copy()
            scaled_img = pygame.transform.scale(img, (width, height))
            self.walk_frames_right.append(scaled_img)

        
        self.walk_frames_left = [
            pygame.transform.flip(f, True, False) for f in self.walk_frames_right
        ]

      
        self.frame_index = 0.0
        self.animation_speed = 0.15  
        self.facing_right = True

       
        self.image = self.walk_frames_right[0]
        self.rect = self.image.get_rect(topleft=(x, y))

   
        self.vel_y = 0
        self.vel_x = 0
        self.on_ground = False

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        dx = 0

     
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= playerSpeed
            self.facing_right = False
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += playerSpeed
            self.facing_right = True

        self.rect.x += dx


        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if dx > 0:
                    self.rect.right = platform.rect.left
                elif dx < 0:
                    self.rect.left = platform.rect.right

       
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screenWidth:
            self.rect.right = screenWidth

        
        if (keys[pygame.K_w] or keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground:
            self.vel_y = jumpHeight
            self.on_ground = False

      
        self.vel_y += gravity
        self.rect.y += self.vel_y
        self.on_ground = False

      
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0


        if self.rect.top > screenHeight:
            self.rect.topleft = (100, 100)
            self.vel_y = 0


        self.animate(dx)

    def animate(self, dx):
        
        frames = self.walk_frames_right if self.facing_right else self.walk_frames_left

        if dx != 0 and self.on_ground:
            
            self.frame_index += self.animation_speed
            if self.frame_index<2.0 or self.frame_index>=4:
                self.frame_index = 2.0
            self.image = frames[int(self.frame_index)]
        else:
            
            self.frame_index = 2.0
            self.image = frames[0]
