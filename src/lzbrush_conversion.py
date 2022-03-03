
import pickle
import pygame


def image_to_lzbrush(path):
    surf = pygame.image.load(path)
    brush_img = pygame.Surface(surf.get_size(), pygame.SRCALPHA, 32).convert_alpha()
    
    lzbrush = {
            'size': brush_img.get_size(),
            'values': []
        }

    for x in range(brush_img.get_size()[0]):
        for y in range(brush_img.get_size()[1]):
            pc = surf.get_at((x,y))

            if pc[3] == 0:
                na = 0  
            else:
                na =  - (pc[0] - 255)


            if na != 0:
                lzbrush['values'].append([na,(x,y)])

    return lzbrush


def dump_lzbrush(lzbrush_obj, dest_file_name:str):
    if not dest_file_name.endswith(('.lzb', '.lzbrush')):
        dest_file_name = f'{dest_file_name}.lzbrush'

    with open(dest_file_name, 'wb') as lz:
        pickle.dump(lzbrush_obj, lz, pickle.HIGHEST_PROTOCOL)

def load_lzbrush(dest_file_name):
    with open(dest_file_name, 'rb') as lz:
        return pickle.load(lz)


def lzbrush_to_pygame_surface(lzbrush_obj):
    

    brush_surf = pygame.Surface(lzbrush_obj['size'], pygame.SRCALPHA, 32).convert_alpha()
    
    for e in lzbrush_obj['values']:
        brush_surf.set_at(e[1], [0,0,0,e[0]])

    return brush_surf

def lzbrushfile_to_pygame_surface(file_path):
    
    return lzbrush_to_pygame_surface(load_lzbrush(file_path))


            



