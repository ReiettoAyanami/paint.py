from tkinter.messagebox import RETRY
import pygame
from pygame import gfxdraw

from src.button import Button

class Image_Button(Button):

    def __init__(self, rect: pygame.Rect or list[int, int, int, int],image:pygame.Surface, outline_color: tuple[int, int, int, int] = (255,255,255,255)) -> None:
        super().__init__(rect, outline_color = outline_color)


        self.rect = pygame.Rect(rect)
        self.image = image
        self.image = pygame.transform.scale(self.image, (self.rect.w, self.rect.h))

    def show(self, surface):

        surface.blit(self.image, (self.rect.x, self.rect.y))
        gfxdraw.rectangle(surface,self.rect, self.outline_color)
        