import pygame
from src.canvas import Canvas



class Rubber:

    def __init__(self, dimension:int) -> None:
        
        self.dimension = dimension


    def paint(self, dest_canvas:Canvas):

        for i in range(self.dimension):
            for j in range(self.dimension):

                dest_canvas.surface.set_at((pygame.mouse.get_pos()[0] + i + int(dest_canvas.coords.x), pygame.mouse.get_pos()[1] + j + int(dest_canvas.coords.y)) ,(0,0,0,0))