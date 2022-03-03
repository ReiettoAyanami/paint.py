import os
import pygame
from src.lzbrush_conversion import *

pygame.init()
pygame.init()
pygame.font.init()
SIZE = WIDTH, HEIGHT = (600,400)
BGCOLOR = (50,50,50)
window = pygame.display.set_mode(SIZE,pygame.RESIZABLE)
pygame.display.set_caption('sus')



f = input('file to convert: ')
df = input('destination: ')


dump_lzbrush(image_to_lzbrush(f), df)

