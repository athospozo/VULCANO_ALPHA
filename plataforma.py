# Em: biblioteca/plataforma.py

import pygame
from PPlay.sprite import Sprite

class Plataforma(Sprite):
    def __init__(self, imagem_path, x_centro, y_pos, largura, altura):
        super().__init__(imagem_path)
        self.width = largura
        self.height = altura
        try:
            self.image = pygame.transform.scale(self.image, (largura, altura))
        except Exception as e:
            print(f"Erro ao redimensionar plataforma: {e}")
        self.x = x_centro - (self.width / 2)
        self.y = y_pos

    def desenhar(self, camera):
        screen_y = self.y - camera.y
        self.set_position(self.x, screen_y)
        self.draw()
