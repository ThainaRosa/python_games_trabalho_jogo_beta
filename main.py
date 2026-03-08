import pygame

import menu
from settings import *
from player import Player
from enemy import Enemy
from coin import Coin
from menu import draw_menu, menu_options

pygame.init()
pygame.mixer.init()

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Forest Adventure")

font = pygame.font.SysFont("Arial", 30)

# ---------------- SOM ----------------

# musica menu
pygame.mixer.music.load("audio/menu_music.ogg")
pygame.mixer.music.set_volume(0.35)
pygame.mixer.music.play(-1)

# efeito dano
hit_sound = pygame.mixer.Sound("audio/player_hit.wav")
hit_sound.set_volume(0.75)

# -------------------------------------

# função para resetar jogo
def reset_game():
    global player, enemies, coin, score, lives, camera_x, spawn_timer

    player = Player(100, HEIGHT - 164)
    enemies = []
    coin = Coin()

    score = 0
    lives = 4

    camera_x = 0
    spawn_timer = 0


player = Player(100, HEIGHT - 164)
enemies = []
coin = Coin()

spawn_timer = 0
spawn_delay = 500

score = 0

lives = 4
max_lives = 6

# imagens UI
heart_img = pygame.image.load("images/ui/heart.png")
heart_img = pygame.transform.scale(heart_img, (32,32))

coin_icon = pygame.image.load("images/ui/coin.png")
coin_icon = pygame.transform.scale(coin_icon,(32,32))

gameover_img = pygame.image.load("images/ui/gameover.png")
gameover_img = pygame.transform.scale(gameover_img, (int(WIDTH*0.95), int(HEIGHT*0.95)))

gameover_rect = gameover_img.get_rect(center=(WIDTH//2, HEIGHT//2))

# PARALAXE
bg_sky = pygame.image.load("images/background/sky.png")
bg_mountains = pygame.image.load("images/background/mountains.png")
bg_trees = pygame.image.load("images/background/trees.png")

bg_sky = pygame.transform.scale(bg_sky,(WIDTH,HEIGHT))
bg_mountains = pygame.transform.scale(bg_mountains,(WIDTH,HEIGHT))
bg_trees = pygame.transform.scale(bg_trees,(WIDTH,HEIGHT))

# CHÃO
ground = pygame.image.load("images/ground/ground.png")
ground = pygame.transform.scale(ground,(WIDTH,100))

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

                        reset_game()
                        game_state = "game"

                        pygame.mixer.music.load("audio/game_music.ogg")
                        pygame.mixer.music.set_volume(0.30)
                        pygame.mixer.music.play(-1)

                    if menu_options[menu.selected] == "EXIT":
                        running = False

        elif game_state == "gameover":

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:

                    reset_game()
                    game_state = "game"

                    pygame.mixer.music.load("audio/game_music.ogg")
                    pygame.mixer.music.set_volume(0.30)
                    pygame.mixer.music.play(-1)

    keys = pygame.key.get_pressed()

    if game_state == "menu":

        draw_menu(window, font)

    elif game_state == "game":

        player.move(keys)

        camera_x = player.x - WIDTH//2

        player_rect = pygame.Rect(player.x, player.y, 64, 64)

        sky_x = -camera_x * 0.2 % WIDTH
        mountain_x = -camera_x * 0.5 % WIDTH
        trees_x = -camera_x * 0.8 % WIDTH

        window.blit(bg_sky, (sky_x - WIDTH, 0))
        window.blit(bg_sky, (sky_x, 0))

        window.blit(bg_mountains, (mountain_x - WIDTH, 0))
        window.blit(bg_mountains, (mountain_x, 0))

        window.blit(bg_trees, (trees_x - WIDTH, 0))
        window.blit(bg_trees, (trees_x, 0))

        ground_x = -camera_x % WIDTH

        window.blit(ground, (ground_x - WIDTH, HEIGHT - 100))
        window.blit(ground, (ground_x, HEIGHT - 100))

        spawn_timer += 1

        if spawn_timer >= spawn_delay and len(enemies) < 2:
            spawn_timer = 0
            enemies.append(Enemy(player.x + WIDTH, HEIGHT - 140))

        for enemy in enemies[:]:

            enemy.move(player.x)

            if player.attacking and enemy.hit_cooldown == 0:

                attack_rect = player.get_attack_rect()

                if attack_rect.colliderect(enemy.get_rect()):

                    enemy.hit(player.x)

                    if enemy.hp <= 0:
                        enemies.remove(enemy)
                        continue

            if player_rect.colliderect(enemy.get_rect()):

                if not player.hurted:
                    player.hit()
                    hit_sound.play()
                    lives -= 1

                    if lives <= 0:
                        game_state = "gameover"

            enemy.draw(window, camera_x)

        if player_rect.colliderect(coin.get_rect()):

            score += 1
            coin.respawn()

            if score % 5 == 0 and lives < max_lives:
                lives += 1

        window.blit(coin.image,(coin.x - camera_x, coin.y))

        player.draw(window, camera_x)

        window.blit(coin_icon,(20,20))
        score_text = font.render(str(score),True,(255,255,255))
        window.blit(score_text,(60,20))

        hearts_per_row = 4
        start_x = WIDTH - 180
        start_y = 20

        for i in range(lives):

            row = i // hearts_per_row
            col = i % hearts_per_row

            x = start_x + col * 40
            y = start_y + row * 40

            window.blit(heart_img, (x, y))

    elif game_state == "gameover":

        window.fill((0,0,0))
        window.blit(gameover_img, gameover_rect)

    pygame.display.update()

pygame.quit()