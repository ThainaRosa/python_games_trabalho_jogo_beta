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

        # cooldown de dano
        self.hit_cooldown = 0
        self.hit_delay = 20

    def move(self, player_x):

        if self.x > player_x:
            self.x -= self.speed
        else:
            self.x += self.speed

        self.frame += 0.15

        if self.frame >= len(self.walk):
            self.frame = 0

        self.image = self.walk[int(self.frame)]

        # reduz cooldown
        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1

    def draw(self, window, camera_x):

        # efeito piscando ao levar dano
        if self.hit_cooldown % 4 < 2:
            window.blit(self.image, (self.x - camera_x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 64, 64)

    def hit(self, player_x):

        if self.hit_cooldown == 0:
            self.hp -= 1
            self.hit_cooldown = self.hit_delay

            # KNOCKBACK
            if self.x > player_x:
                self.x += 115
            else:
                self.x -= 115