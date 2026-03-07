import pygame
from settings import *

def draw_menu(window,font):

    window.fill((100,200,100))

    title = font.render("FOREST ADVENTURE",True,BLACK)
    start = font.render("ENTER - START",True,BLACK)

    control1 = font.render("ARROWS - MOVE",True,BLACK)
    control2 = font.render("SPACE - JUMP",True,BLACK)

    window.blit(title,(250,150))
    window.blit(start,(300,200))
    window.blit(control1,(280,260))
    window.blit(control2,(280,300))