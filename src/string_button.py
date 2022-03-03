from src.button import Button
import pygame
import pygame.font
from pygame import gfxdraw

pygame.font.init()

class String_Button (Button):

    def __init__(self, rect: pygame.Rect or list[int, int, int, int],text:str,font:pygame.font.Font or tuple[str, int] or pygame.font.SysFont = pygame.font.SysFont('Arial',20), text_color:tuple[int,int,int,int] = (255,255,255,255), color: tuple[int, int, int, int] = (100,100,100,255), outline_color: tuple[int, int, int, int] = (255,255,255,255)) -> None:
        super().__init__(rect, color, outline_color)
        
        self.text = text
        self.font =font
        self.text_color = text_color


        
        self.text = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text.get_rect()
        self.text_rect.center =  (self.rect.x + (self.rect.w / 2), self.rect.y + (self.rect.h / 2))
        

    def show(self,surface:pygame.Surface):
        
        gfxdraw.box(surface, self.rect,self.color)
        gfxdraw.rectangle(surface, self.rect, self.outline_color)
        surface.blit(self.text,self.text_rect)
        

        
