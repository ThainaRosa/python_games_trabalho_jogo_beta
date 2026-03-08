import pygame
from settings import *

def draw_menu(window, font):
    bg = pygame.image.load("images/menu/menu_bg.png")
    bg = pygame.transform.scale(bg, window.get_size())
    window.blit(bg, (0, 0))

    title = font.render("FOREST ADVENTURE", True, BLACK)
    start = font.render("ENTER - Iniciar", True, BLACK)

    control1 = font.render("ARROWS - Movimenta", True, BLACK)
    control2 = font.render("SPACE - Pula", True, BLACK)

    window.blit(title, (250, 150))
    window.blit(start, (300, 200))
    window.blit(control1, (280, 260))
    window.blit(control2, (280, 300))
