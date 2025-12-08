import pygame 
from PPlay.animation import *
from PPlay.keyboard import *

class lava:
    def __init__(self, janela):

        #basico:
        self.janela = janela
        self.teclado = Keyboard()

        #gerando animacao da lava:
        self.sprite_lava = Animation("ARTES/lava.png", 2)

        #definindo propriedades:
        self.width = self.janela.width
        self.height = self.janela.height
        self.sprite_lava.width = self.width
        self.sprite_lava.height = self.height
        self.velocidade = 0

        try:
            self.sprite_lava.image = pygame.transform.scale(self.sprite_lava.image, (int(self.width * 2), int(self.height)))
        except Exception as e:
            print(f"Erro ao redimensionar imagem da Lava: {e}")
        
        #tempo de animacao:
        self.sprite_lava.set_total_duration(800)
        
        #posicionamento inicial (embaixo da tela):
        self.x = 0
        self.y = self.janela.height - self.janela.height/15
        self.espaco = False

    def lava_jogador(self, jogador):

        # Vamos ver se a lava pode comecar a subir:
        if (self.teclado.key_pressed("SPACE") or self.teclado.key_pressed("W")):
            self.espaco = True

        self.velocidade = 5

        if (self.espaco):
            # Se jogador parado, lava sobe normal ate um limite maximo para ficar mais divertido
            if (jogador.subindo == False and self.y > self.janela.height/2):
                    self.y -= self.velocidade*0.8*self.janela.delta_time()
            
            # Se jogador pulando/subindo, lava sobe mais rápido para pressionar
            else:
                if (self.y < self.janela.height - 10):
                    self.y += self.velocidade*5*self.janela.delta_time()
        
    def desenhar(self): 
        self.sprite_lava.set_position(self.x, self.y)
        self.sprite_lava.update()
        self.sprite_lava.draw()