import pygame
from settings import *

menu_options = ["START GAME", "EXIT"]
selected = 0


def draw_text_outline(surface, text, font, color, outline_color, x, y):

    base = font.render(text, True, color)
    outline = font.render(text, True, outline_color)

    # borda
    surface.blit(outline, (x-2, y))
    surface.blit(outline, (x+2, y))
    surface.blit(outline, (x, y-2))
    surface.blit(outline, (x, y+2))

    # texto principal
    surface.blit(base, (x, y))


def draw_menu(window, font):

    bg = pygame.image.load("images/menu/menu_bg.png")
    bg = pygame.transform.scale(bg, window.get_size())
    window.blit(bg, (0,0))

    # opções do menu
    for i, option in enumerate(menu_options):

        if i == selected:
            color = (255,0,0)
            text = "> " + option
        else:
            color = (255,255,255)
            text = option

        draw_text_outline(
            window,
            text,
            font,
            color,
            (0,0,0),
            300,
            220 + i*50
        )

    # controles
    draw_text_outline(
        window,
        "Z - Atacar",
        font,
        (255,255,255),
        (0,0,0),
        270,
        340
    )

    draw_text_outline(
        window,
        "ESPAÇO - Pular",
        font,
        (255,255,255),
        (0,0,0),
        270,
        380
    )

    draw_text_outline(
        window,
        "SETAS - Movimentar",
        font,
        (255, 255, 255),
        (0, 0, 0),
        270,
        420
    )

