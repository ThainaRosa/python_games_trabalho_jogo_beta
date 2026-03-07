import pygame

class Player:

    def __init__(self, x, y):

        # carregar animação de corrida
        self.run = [
            pygame.image.load("images/player/run1.png"),
            pygame.image.load("images/player/run2.png"),
            pygame.image.load("images/player/run3.png"),
            pygame.image.load("images/player/run4.png")
        ]

        # redimensionar todas imagens
        for i in range(len(self.run)):
            self.run[i] = pygame.transform.scale(self.run[i], (64,64))

        self.image = self.run[0]

        self.frame = 0

        self.x = x
        self.y = y

        self.vel = 5

        self.jump = False
        self.jump_count = 10

    def move(self, keys):

        moving = False

        if keys[pygame.K_LEFT]:
            self.x -= self.vel
            moving = True

        if keys[pygame.K_RIGHT]:
            self.x += self.vel
            moving = True

        # animação de corrida
        if moving:
            self.frame += 0.2
            if self.frame >= len(self.run):
                self.frame = 0
            self.image = self.run[int(self.frame)]

        # pulo
        if not self.jump:

            if keys[pygame.K_SPACE]:
                self.jump = True

        else:

            if self.jump_count >= -10:

                self.y -= (self.jump_count * abs(self.jump_count)) * 0.5
                self.jump_count -= 1

            else:

                self.jump = False
                self.jump_count = 10

    def draw(self, window):

        window.blit(self.image,(self.x,self.y))