from cgitb import text
import imp
import json
from os import system
import os
import random
from select import select
import sys
import pygame
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP, BUTTON_LEFT, BUTTON_MIDDLE, BUTTON_RIGHT
from pygame.time import Clock
from pygame import MOUSEMOTION, MOUSEWHEEL, gfxdraw
from src.rubber import Rubber
from src.brush import Brush
from src.canvas import Canvas
from random import randint
from colorsys import hsv_to_rgb, rgb_to_hsv
from src.lzbrush_conversion import *
from src.image_button import Image_Button
from src.inventory_menu import Inventory_Menu
from src.utils import *

pygame.init()
pygame.font.init()
SIZE = WIDTH, HEIGHT = (600,400)
BGCOLOR = (255,255,255)
GFONT = pygame.font.SysFont("Comic Sans MS", 30)
window = pygame.display.set_mode(SIZE,pygame.RESIZABLE)
pygame.display.set_caption('test')
clock = Clock()

current_color = (0,0,0)
current_hardness = 255
current_size = 100


# PER MASSIMO:
# IL BUG CHE TI HO MANDATO SI TROVA IN src.canvas 
# E PENSO CHE SIA DOVUTO ALLA FUNZIONE update_on_painting
# MA NON CAPISCO COME MAI SCALI IN QUESTO MODO LA SURFACE
# 
# sus


"""
TODO
FIX:
    - Non far disegnare quando si sta nel rect del menu -> Fatto sus
    - Rifare la gomma

    ## IMPORTANTE 
    - RIFAI IL RESIZE DELLA CANVAS
    - SISTEMA ALLINEAMENTO CON PENNELLO


IMPLEMENTA:
    - Slider per hardness e size 
    - Resize della canvas -> Fatto, (da finire)
    - Menu in alto 
    
    ## IMPORTANTE 
    - ZOOM 
    


Promemoria:
    - Tieni una foto di tutti i brush

"""


c = Canvas((480, 270), coords=(0,50))
b = [Brush(f'default_brushes/default.lzb', hardness=10, color=(0,0,0), size=100)]

bs = []
textures = []
for i, f in enumerate(os.listdir('lzbrushes')):
    
    bs.append(Brush(f'lzbrushes/{f}',hardness =  current_hardness, color = current_color, size = current_size))

for i, f in enumerate(os.listdir('brushesimg')):
    textures.append(pygame.image.load(f'brushesimg/{f}'))

brush_list = Inventory_Menu(textures, (0,0), color=(0,0,0,100), outline_color=(0,0,0), button_dimension=20, button_offset=pygame.Vector2(3,3))


r = Rubber(100)


def main():
    
    running = True
    mouse_pressed = {'left' : False, 'right':False, 'wheel': False}
    selected_brush = 0
    

    while running:
       
        mouse_clicked = {'left' : False, 'right':False, 'wheel': False}
        mouse_moved = False
        mouse_scroll = 0
        is_painting = False

        events = {
            'mouse_clicked': mouse_clicked,
            'mouse_pressed': mouse_pressed
        }
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            
            if event.type == MOUSEMOTION:
                mouse_moved = True
            

            if event.type == MOUSEBUTTONDOWN:
                if event.button == BUTTON_LEFT:
                    mouse_pressed['left'] = True
                    mouse_clicked['left'] = True

                elif event.button == BUTTON_MIDDLE:
                    mouse_pressed['wheel'] = True
                    mouse_clicked['wheel'] = True

                elif event.button == BUTTON_RIGHT:
                    mouse_pressed['right'] = True
                    mouse_clicked['right'] = True

            if event.type == MOUSEBUTTONUP:
                if event.button == BUTTON_LEFT:
                    mouse_pressed['left'] = False
                elif event.button == BUTTON_MIDDLE:
                    mouse_pressed['wheel'] = False
                elif event.button == BUTTON_RIGHT:
                    mouse_pressed['right'] = False

            if event.type == MOUSEWHEEL:
                mouse_scroll = event.y
            

            
        


        window.fill(BGCOLOR)
        

        
        c.show(window)
        c.update_size_on_drag(events)
        

        if not brush_list.hover() and c.countourn_rect.collidepoint(pygame.mouse.get_pos()):
            if mouse_clicked['left']:
                is_painting = True
            

            if mouse_pressed['left'] and mouse_moved:
                is_painting = True

            elif mouse_pressed['right']:
                r.paint(c)

            if mouse_clicked['wheel']:
                c.clear()

        brush_list.show(window)
        brush_list.update(events)

        selected_brush = brush_list.get_selected()

        c.update_on_painting(bs[selected_brush], is_painting)
        
        
        pygame.display.update()

if __name__ == '__main__':
    main()