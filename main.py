import pygame

import menu
from settings import *
from player import Player
from enemy import Enemy
from coin import Coin
from menu import draw_menu
from menu import draw_menu, menu_options

pygame.init()

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Forest Adventure")

font = pygame.font.SysFont("Arial", 30)

# player começa em cima do chão
player = Player(100, HEIGHT - 164)

# inimigos
enemies = []

spawn_timer = 0
spawn_delay = 500

coin = Coin()

score = 0

# vidas
lives = 4

heart_img = pygame.image.load("images/ui/heart.png")
heart_img = pygame.transform.scale(heart_img, (32,32))

# CAMADAS DE PARALAXE
bg_sky = pygame.image.load("images/background/sky.png")
bg_mountains = pygame.image.load("images/background/mountains.png")
bg_trees = pygame.image.load("images/background/trees.png")

bg_sky = pygame.transform.scale(bg_sky,(WIDTH,HEIGHT))
bg_mountains = pygame.transform.scale(bg_mountains,(WIDTH,HEIGHT))
bg_trees = pygame.transform.scale(bg_trees,(WIDTH,HEIGHT))

# CHÃO
ground = pygame.image.load("images/ground/ground.png")
ground = pygame.transform.scale(ground,(WIDTH,100))

# câmera
camera_x = 0

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

                if event.key == pygame.K_UP:
                    menu.selected -= 1

                if event.key == pygame.K_DOWN:
                    menu.selected += 1

                menu.selected %= len(menu_options)

                if event.key == pygame.K_RETURN:

                    if menu_options[menu.selected] == "START GAME":
                        game_state = "game"

                    if menu_options[menu.selected] == "EXIT":
                        running = False

    keys = pygame.key.get_pressed()

    if game_state == "menu":

        draw_menu(window, font)

    elif game_state == "game":

        # mover jogador
        player.move(keys)

        # câmera segue jogador
        camera_x = player.x - WIDTH//2

        player_rect = pygame.Rect(player.x, player.y, 64, 64)

        # PARALAXE INFINITO
        sky_x = -camera_x * 0.2 % WIDTH
        mountain_x = -camera_x * 0.5 % WIDTH
        trees_x = -camera_x * 0.8 % WIDTH

        window.blit(bg_sky, (sky_x - WIDTH, 0))
        window.blit(bg_sky, (sky_x, 0))

        window.blit(bg_mountains, (mountain_x - WIDTH, 0))
        window.blit(bg_mountains, (mountain_x, 0))

        window.blit(bg_trees, (trees_x - WIDTH, 0))
        window.blit(bg_trees, (trees_x, 0))

        # CHÃO INFINITO
        ground_x = -camera_x % WIDTH

        window.blit(ground, (ground_x - WIDTH, HEIGHT - 100))
        window.blit(ground, (ground_x, HEIGHT - 100))

        # spawn inimigos
        spawn_timer += 1

        if spawn_timer >= spawn_delay and len(enemies) < 2:
            spawn_timer = 0
            enemies.append(Enemy(player.x + WIDTH, HEIGHT - 140))

        # inimigos
        for enemy in enemies[:]:

            enemy.move(player.x)

            # ATAQUE DO PLAYER
            if player.attacking:

                attack_rect = player.get_attack_rect()

                if attack_rect.colliderect(enemy.get_rect()):

                    enemy.hit()

                    if enemy.hp <= 0:
                        enemies.remove(enemy)
                        continue

            # COLISÃO COM PLAYER
            if player_rect.colliderect(enemy.get_rect()):

                player.hit()
                lives -= 1
                enemies.remove(enemy)

                if lives <= 0:
                    game_state = "gameover"

            window.blit(enemy.image,(enemy.x - camera_x, enemy.y))

        # colisão moeda
        if player_rect.colliderect(coin.get_rect()):

            score += 1
            coin.respawn()

        # desenhar moeda
        window.blit(coin.image,(coin.x - camera_x, coin.y))

        # desenhar jogador
        player.draw(window, camera_x)

        # placar
        score_text = font.render(f"Coins: {score}",True,(255,255,255))
        window.blit(score_text,(20,20))

        # vidas
        for i in range(lives):
            window.blit(heart_img,(WIDTH - 180 + i*40,20))

    elif game_state == "gameover":

        window.fill((0,0,0))

        text = font.render("GAME OVER",True,(255,0,0))
        window.blit(text,(WIDTH//2 - 100, HEIGHT//2))

    pygame.display.update()

pygame.quit()