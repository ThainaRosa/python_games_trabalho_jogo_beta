import pygame
import random

class Coin:

    def __init__(self):

        images = [
            "images/coins/coin1.png",
            "images/coins/coin2.png",
            "images/coins/coin3.png"
        ]

        image = pygame.image.load(random.choice(images))

        # diminuir tamanho
        self.image = pygame.transform.scale(image, (32, 32))

        self.x = random.randint(200, 700)
        self.y = 320

    def draw(self, window):

        window.blit(self.image, (self.x, self.y))

    def get_rect(self):

        return pygame.Rect(self.x, self.y, 32, 32)

    def respawn(self):

        self.x = random.randint(200, 700)