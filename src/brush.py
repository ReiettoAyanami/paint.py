import json
import pickle
import pygame
from pygame import PixelArray

from src.lzbrush_conversion import load_lzbrush, lzbrush_to_pygame_surface, lzbrushfile_to_pygame_surface


class Brush:

    def __init__(self, lzbrush_path:str, size:int = 20, hardness:int = 50, color = (0,0,0)) -> None:
        
        self.brush_img = lzbrushfile_to_pygame_surface(lzbrush_path)

        self.brush_img.set_alpha(hardness)
        
        maxs = max(self.brush_img.get_width(), self.brush_img.get_width())


        self.brush_img = pygame.transform.scale(self.brush_img, (int(self.brush_img.get_width()/maxs * size),int(self.brush_img.get_height()/maxs * size)))

        self.brush_img.fill(color, special_flags=pygame.BLEND_ADD)

        
        

    def paint(self, dest_canvas):
        dest_canvas.surface.blit(self.brush_img, ((pygame.mouse.get_pos()[0] - self.brush_img.get_width()//2) - dest_canvas.coords.x,(pygame.mouse.get_pos()[1] - self.brush_img.get_height()//2) - dest_canvas.coords.y))

    def surf_paint_at(self, coords:pygame.Vector2 or tuple[int, int], surface):
        surface.blit(self.brush_img, coords)
    
    def update_color(self, new_color):

        pygame.transform.threshold(self.brush_img,self.brush_img,self.color, (0,0,0,0),new_color, 1, None, True)
        self.color = new_color
