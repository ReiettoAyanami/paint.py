import pygame
from pygame import gfxdraw


class Button():
    
    def __init__(self, rect:pygame.Rect or list[int,int,int,int], color:tuple[int,int,int,int] = (100,100,100,255), outline_color:tuple[int,int,int,int] = (255,255,255,255)) -> None:
        self.rect = pygame.Rect(rect)
        self.color = color
        self.outline_color = outline_color

    def show(self, surface:pygame.Surface) -> None:
        gfxdraw.box(surface, self.rect,self.color)
        gfxdraw.rectangle(surface, self.rect, self.outline_color)


    def hover(self) -> bool:
        return True if self.rect.collidepoint(pygame.mouse.get_pos()) else False

    def on_event(self, event:bool, func):
        
        if event and (func is not None):
            return func()