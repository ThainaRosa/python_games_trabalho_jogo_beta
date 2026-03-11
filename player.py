import pygame

class Player:
    def __init__(self, x, y, ground_offset=65):

        def load_sprite(path, size=(84,84), colorkey=None):
            img = pygame.image.load(path)
            if colorkey is not None:
                img = img.convert()
                img.set_colorkey(colorkey)
            else:
                img = img.convert_alpha()
            return pygame.transform.scale(img, size)

        # Animação corrida
        self.run = [
            load_sprite("images/player/run1.png"),
            load_sprite("images/player/run2.png"),
            load_sprite("images/player/run3.png"),
            load_sprite("images/player/run4.png")
        ]

        # Animação ataque
        self.attack = [
            load_sprite("images/player/attack1.png"),
            load_sprite("images/player/attack2.png")
        ]

        # Animação dano
        self.hurt_img = load_sprite("images/player/hurt.png")

        # Estado inicial
        self.image = self.run[0]
        self.frame = 0
        self.attack_frame = 0

        self.attacking = False
        self.attack_cooldown = 0

        # Dano
        self.hurted = False
        self.hurt_timer = 0
        self.hurt_duration = 15

        # Posição
        self.x = x
        self.y = y + ground_offset

        # Direção
        self.direction = 1  # 1 = direita, -1 = esquerda

        # Movimento
        self.vel = 5
        self.jump = False
        self.jump_count = 10


    def move(self, keys):

        moving = False

        if keys[pygame.K_LEFT]:
            self.x -= self.vel
            self.direction = -1
            moving = True

        if keys[pygame.K_RIGHT]:
            self.x += self.vel
            self.direction = 1
            moving = True

        # Iniciar ataque
        if keys[pygame.K_z] and not self.attacking and self.attack_cooldown == 0:
            self.attacking = True
            self.attack_frame = 0

        # Animação ataque
        if self.attacking:

            self.attack_frame += 0.3

            if self.attack_frame >= len(self.attack):
                self.attack_frame = 0
                self.attacking = False
                self.attack_cooldown = 20

            self.image = self.attack[int(self.attack_frame)]

        else:

            if moving:
                self.frame += 0.2

                if self.frame >= len(self.run):
                    self.frame = 0

                self.image = self.run[int(self.frame)]

        # Cooldown ataque
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Pulo
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

        # Atualiza dano
        if self.hurted:

            self.hurt_timer -= 1

            if self.hurt_timer <= 0:
                self.hurted = False


    def draw(self, window, camera_x):

        if self.hurted:
            img = self.hurt_img
        else:
            img = self.image

        # espelha sprite se estiver olhando para esquerda
        if self.direction == -1:
            img = pygame.transform.flip(img, True, False)

        window.blit(img, (self.x - camera_x, self.y))


    def get_rect(self):
        return pygame.Rect(self.x, self.y, 64, 64)


    def get_attack_rect(self):

        if self.direction == 1:
            return pygame.Rect(self.x + 50, self.y + 10, 40, 40)
        else:
            return pygame.Rect(self.x - 40, self.y + 10, 40, 40)


    def hit(self):

        self.hurted = True
        self.hurt_timer = self.hurt_duration

        if self.direction == 1:
            self.x -= 120
        else:
            self.x += 120

