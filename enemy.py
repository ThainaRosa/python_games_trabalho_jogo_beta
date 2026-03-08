import pygame

class Enemy:
    def __init__(self, x, y, ground_offset=50):

        self.walk = [
            pygame.image.load("images/enemy/enemy1.png"),
            pygame.image.load("images/enemy/enemy2.png"),
            pygame.image.load("images/enemy/enemy3.png")
        ]

        for i in range(len(self.walk)):
            self.walk[i] = pygame.transform.scale(self.walk[i], (64, 64))

        self.image = self.walk[0]

        self.frame = 0

        self.x = x
        self.y = y + ground_offset

        self.speed = 2

        # vida
        self.hp = 2

    def move(self, player_x):

        if self.x > player_x:
            self.x -= self.speed
        else:
            self.x += self.speed

        self.frame += 0.15

        if self.frame >= len(self.walk):
            self.frame = 0

        self.image = self.walk[int(self.frame)]

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 64, 64)

    def hit(self):
        self.hp -= 1
