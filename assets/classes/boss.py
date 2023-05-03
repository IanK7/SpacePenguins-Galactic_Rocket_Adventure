import pygame

from assets.classes.projectile import Projectile


class boss(pygame.sprite.Sprite):
    def __init__(self, x, y, screen):
        super().__init__()
        self.image = pygame.image.load("assets/sprites/Boss_Example.png")
        self.image = pygame.transform.scale(self.image, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.screen = screen
        self.attack_image = pygame.image.load("assets/sprites/water_projectile-removebg-preview.png")
        self.attack_sound = pygame.mixer.Sound("assets/audio/point.wav")
        self.attack_sound.set_volume(0.5)
        self.attack_delay = 120
        self.attack_timer = 0
        self.projectiles = pygame.sprite.Group()

        # Draw boss
        self.screen.blit(self.image, self.rect)

        # Update Boss
        self.update()

    def update(self):
        # si cambio esto dispara mas rapido cada projectil
        self.attack_timer -= 5
        # Shoot projectile
        if self.attack_timer <= 0:
            self.attack_timer = self.attack_delay
            # self.attack_sound.play()
            projectile = Projectile(self.rect.x, self.rect.y, self.attack_image)
            self.projectiles.add(projectile)

        # Update projectiles
        self.projectiles.update()

        # Draw projectiles
        self.projectiles.draw(self.screen)

    def shoot(self):
        self.attack_timer = 1
