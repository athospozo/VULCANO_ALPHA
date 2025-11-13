# Em: biblioteca/lava.py

import pygame 
from PPlay.keyboard import *
from PPlay.sprite import *
from PPlay.animation import *

class lava:
    def __init__(self, personagem, janela):
        self.sprite_lava = Animation("ARTES/lava.png", 2)
        self.sprite_lava.width = janela.width
        self.sprite_lava.height = janela.height
        try:
            self.sprite_lava.image = pygame.transform.scale(
                self.sprite_lava.image, 
                (self.sprite_lava.width * 2, self.sprite_lava.height)
            )
        except Exception as e:
            print(f"Erro ao redimensionar imagem da Lava: {e}")
        self.sprite_lava.set_total_duration(800)
        self.x = 0
        self.y = janela.height - janela.height/6

    def atualizar(self):
        self.sprite_lava.update()

    def desenhar(self): 
        self.sprite_lava.set_position(self.x, self.y)
        self.sprite_lava.draw()