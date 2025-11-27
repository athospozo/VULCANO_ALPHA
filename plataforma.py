# Em: biblioteca/plataforma.py
import random
import pygame
from PPlay.sprite import Sprite

class Plataforma (Sprite):

    def __init__(self, imagem_path, x_centro, y_pos,
                  largura, altura, janela):
        super().__init__(imagem_path)
        self.width = largura
        self.height = altura
        self.lista = []
        self.contador = 0

        try:
            self.image = pygame.transform.scale(self.image, (largura, altura))
        except Exception as e:
            print(f"Erro ao redimensionar plataforma: {e}")

        primeira = Sprite("ARTES/plataforma1.png")
        primeira.x = x_centro - primeira.width / 2
        primeira.y = y_pos

        self.lista.append(primeira)

        self.min_gap_vertical, self.max_gap_vertical = janela.height/5, janela.height/4

    def criacao_plataformas (self, janela):
        #cria plataformas até ter 15
        i = len(self.lista) - 1
        while ((i+1 < 15)):
            #requer uma melhor aplicacao das escolhas de x e y
            novo_x_centro = random.randint(int(self.lista[i].x/2),
                                            int(janela.width - self.lista[i].x/2 - self.lista[i].width))
            gap_vertical = random.randint(int(self.min_gap_vertical), int(self.max_gap_vertical))
            nova_plataforma = Sprite(random.choice(["ARTES/plataforma1.png", "ARTES/plataforma2.png", "ARTES/plataforma3.png"]))
            nova_plataforma.x = novo_x_centro - nova_plataforma.width / 2
            nova_plataforma.y = self.lista[i-1].y - gap_vertical
            self.lista.append(nova_plataforma)
            i += 1   

    def remocao_plataformas(self, janela):
        for plataforma in self.lista:
            if plataforma.y > janela.height:
                self.lista.remove(plataforma)
        print(len(self.lista))
    
    def desenhar_plataformas (self, camera):
        #requer aplicacao ou da camera ou do deltatime, apenas para simular movimento
        for plataforma in self.lista:
            screen_y = plataforma.y
            plataforma.set_position(plataforma.x, screen_y)
            plataforma.draw()