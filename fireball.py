import pygame

class Fireball:

    def __init__(self, x, y, direction):

        self.x = x
        self.y = y

        self.radius = 10
        self.speed = 12

        self.direction = direction

    def move(self):
        self.x += self.speed * self.direction

    def draw(self, window, camera_x):
        pygame.draw.circle(
            window,
            (255,0,0),   # cor da bola de fogo
            (int(self.x - camera_x), int(self.y)),
            self.radius
        )

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.radius*2, self.radius*2)