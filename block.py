import pygame 
from settings import *

# Classe des balle
class Block(pygame.sprite.Sprite):
    # Couleur, largeur, hauteur
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self) 

        # Definition de son image
        self.image = pygame.Surface([width, height ]) 
        self.image.fill(white)
        self.image.set_colorkey(white)
        pygame.draw.ellipse(self.image,color,[0, 0, width , height ])

        # Recuperation de son rectangle
        self.rect = self.image.get_rect() 
        