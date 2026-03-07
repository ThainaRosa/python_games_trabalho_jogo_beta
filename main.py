import pygame

from settings import *
from player import Player
from enemy import Enemy
from coin import Coin
from menu import draw_menu

pygame.init()

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Forest Adventure")

font = pygame.font.SysFont("Arial", 30)

player = Player(100, 350)

# lista de inimigos
enemies = []

spawn_timer = 0
spawn_delay = 300  # MAIS TEMPO ENTRE INIMIGOS

coin = Coin()

score = 0

backgrounds = [
    pygame.image.load("images/background/bg1.png"),
    pygame.image.load("images/background/bg2.png"),
    pygame.image.load("images/background/bg3.png")
]

for i in range(len(backgrounds)):
    backgrounds[i] = pygame.transform.scale(backgrounds[i], (WIDTH, HEIGHT))

bg_index = 0
bg_timer = 0

clock = pygame.time.Clock()

game_state = "menu"

running = True

while running:

    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if game_state == "menu":

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_state = "game"

    keys = pygame.key.get_pressed()

    if game_state == "menu":

        draw_menu(window, font)

    elif game_state == "game":

        bg_timer += 1

        if bg_timer > 600:
            bg_timer = 0
            bg_index += 1

            if bg_index >= len(backgrounds):
                bg_index = 0

        window.blit(backgrounds[bg_index], (0, 0))

        player.move(keys)

        player_rect = pygame.Rect(player.x, player.y, 64, 64)

        # SPAWN DE INIMIGOS
        spawn_timer += 1

        if spawn_timer >= spawn_delay and len(enemies) < 3:
            spawn_timer = 0
            enemies.append(Enemy(WIDTH, 360))

        # INIMIGOS
        for enemy in enemies[:]:

            enemy.move()

            if player_rect.colliderect(enemy.get_rect()):
                game_state = "gameover"

            # remove inimigos que saíram da tela
            if enemy.x < -100:
                enemies.remove(enemy)

            enemy.draw(window)

        # COLISÃO MOEDA
        if player_rect.colliderect(coin.get_rect()):

            score += 1
            coin.respawn()

        # DESENHAR
        player.draw(window)
        coin.draw(window)

        # PLACAR
        score_text = font.render(f"Coins: {score}", True, (255,255,255))
        window.blit(score_text, (20,20))

    elif game_state == "gameover":

        window.fill((0,0,0))

        text = font.render("GAME OVER", True, (255,0,0))
        window.blit(text, (WIDTH//2 - 100, HEIGHT//2))

    pygame.display.update()

pygame.quit()