from numpy import real
import pygame
from pygame import gfxdraw
from src.brush import Brush
from src.utils import *

from src.button import Button
class Canvas:

    def __init__(self,canvas_size:tuple[int, int],real_size: tuple[int, int] = (1920,1080),coords:tuple[int,int] = (0,0)) -> None:
        
        # Abbastanza self-explainatory sono una surface dove sta la vera immagine che avrà una risoluzione più alta,
        # Mentre la seconda serve solo a rappresentarla sullo schermo

        self.real_surface = pygame.Surface(real_size, pygame.SRCALPHA, 32)
        self.surface = pygame.transform.scale(self.real_surface, canvas_size)

        self.real_surface.convert_alpha()
        self.surface.convert_alpha()
        
        # Qua ci sono degli attributi, stati ecc...

        self.coords = pygame.Vector2(coords) # Sono le coordinate dove la canvas verrà messa nella finestra
        self.resizing = {'right':False, 'bottom':False, 'bottomright':False}
        self.countourn_rect = pygame.Rect(self.coords.x,self.coords.y, self.surface.get_width(), self.surface.get_height()) 
        # Serviva un rect della surface visto che il metodo self.surface.get_rect() ti ritorna un rect dove le coordinate sono di base (0,0) per qualche motivo


        # Sono i pulsanti che servono a cambiare la dimensione della canvas

        self.border_hitboxes = {
                
                'right': Button((self.countourn_rect.topright[0], self.countourn_rect.topright[1], 10, self.surface.get_rect().h)),
                'bottom': Button((self.countourn_rect.bottomleft[0], self.countourn_rect.bottomleft[1], self.surface.get_rect().w, 10)),
                'bottomright': Button((self.countourn_rect.bottomright[0], self.countourn_rect.bottomright[1], 10, 10))
                
        }
        self.minsize = 10

    # Serve a mostrare la canvas

    def show(self, window):
        for hitbox in self.border_hitboxes:
            self.border_hitboxes[hitbox].show(window)
            if self.border_hitboxes[hitbox].hover():
                gfxdraw.rectangle(window,self.border_hitboxes[hitbox].rect, (0,0,0))

        self.countourn_rect.x, self.countourn_rect.y = self.coords
        gfxdraw.rectangle(window, self.countourn_rect, (0,0,0))
        window.blit(self.surface, self.coords)
        
    
    # Per avere le coordinate del mouse relative alla canvas

    def get_mouse_pos_on_canvas(self):

        return pygame.mouse.get_pos()[0] - self.coords.x, pygame.mouse.get_pos()[1] - self.coords.y

    # Per trasformare tutto, server per quando draggo i pulsanti che ho menzionato prima nell'__init__

    def resize(self,new_size:tuple[int,int]):

        # Proporzioni per ottenere quale debba essere la nuova dimensione della canvas
        
        
        original_size = self.countourn_rect.size
        new_real_size = (
            ((self.real_surface.get_width()  * new_size[0])/ original_size[0]),
            ((self.real_surface.get_height() * new_size[1])/original_size[1])
        )
        
        # Creo delle nuove surface e le rimpiazzo con quelle nuove
        new_surf = pygame.Surface(new_size, pygame.SRCALPHA, 32)
        new_real_surf = pygame.Surface(new_real_size, pygame.SRCALPHA, 32)

        new_surf.blit(self.surface, (0,0))
        new_real_surf.blit(self.real_surface, (0,0))

        self.surface = new_surf
        self.real_surface = new_real_surf

        # Aggiusto alcuni elementi della UI alla nuova dimensione della canvas

        self.countourn_rect = pygame.Rect(self.coords.x,self.coords.y, self.surface.get_width() + 1, self.surface.get_height() + 1) 
        self.border_hitboxes['right'].rect = pygame.Rect(self.countourn_rect.topright[0], self.countourn_rect.topright[1], 10, self.surface.get_rect().h)
        self.border_hitboxes['bottom'].rect = pygame.Rect(self.countourn_rect.bottomleft[0], self.countourn_rect.bottomleft[1], self.surface.get_rect().w, 10)
        self.border_hitboxes['bottomright'].rect = pygame.Rect((self.countourn_rect.bottomright[0], self.countourn_rect.bottomright[1], 10, 10))


    # Pulisce la canvas, serve solo per testare...

    def clear(self):

        clean_surface = pygame.Surface(self.surface.get_size(), pygame.SRCALPHA, 32)
        self.surface = clean_surface

    #   ---------
    #   Questa è la funzione che da problemi da quanto ho potuto constatare:
    #   A quanto pare il blit non fa quello che deve fare(?) 
    #   Qualche calcolo è andato storto e non riesco a capire
    #   maprange(s,a,b) è il corrispondente di processing
    #   [https://rosettacode.org/wiki/Map_range]
    #   ---------
    
    def update_on_painting(self, brush:Brush, is_painting:bool):
        
        pos =   ( 
                    maprange(self.get_mouse_pos_on_canvas()[0], (0, self.surface.get_size()[0]), (0, self.real_surface.get_size()[0])),
                    maprange(self.get_mouse_pos_on_canvas()[1], (0, self.surface.get_size()[1]), (0, self.real_surface.get_size()[1]))
                )

        if is_painting:
            
            brush.surf_paint_at(pos,self.real_surface)

            self.surface =  pygame.transform.scale(self.real_surface,self.surface.get_size())

           

    # Serve per cambiare la dimensione al drag dei bottoni.
    
    def update_size_on_drag(self, events:dict):

        for k in self.border_hitboxes:
            if self.border_hitboxes[k].hover() and events.get('mouse_clicked').get('left'):
                self.resizing[k] = True
            elif not events.get('mouse_pressed').get('left'):
                self.resizing[k] = False
        
        
        if self.resizing['right']:
            dst = pygame.mouse.get_pos()[0] - (self.border_hitboxes['right'].rect.w // 2) - self.countourn_rect.right

            self.resize(( max(self.surface.get_width() + dst, self.minsize), self.surface.get_height()))


        if self.resizing['bottom']:
            dst  = pygame.mouse.get_pos()[1] - (self.border_hitboxes['bottom'].rect.h // 2)  - self.countourn_rect.bottom
            
            self.resize((self.surface.get_width(), max(self.surface.get_height() + dst, self.minsize)))

        if self.resizing['bottomright']:
            
            # Calcolo la distanza tra pos e mouse_pos
            # La aggiungo ai lati e poi scalo con self.resize

            dst = (pygame.mouse.get_pos()[0] - (self.border_hitboxes['bottomright'].rect.w // 2)  - self.countourn_rect.right, pygame.mouse.get_pos()[1] - (self.border_hitboxes['bottomright'].rect.h // 2)  - self.countourn_rect.bottom)
            self.resize((max(self.surface.get_width() + dst[0], self.minsize), max(self.surface.get_height() + dst[1], self.minsize)))

        