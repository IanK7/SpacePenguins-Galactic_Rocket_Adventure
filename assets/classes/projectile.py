import pygame


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y + 85
        self.speed = 10

    def update(self):
        self.rect.x -= self.speed
        if self.rect.top > 600:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
