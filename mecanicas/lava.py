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
        self.width = janela.width
        self.height = janela.height
        self.sprite_lava.width = self.width
        self.sprite_lava.height = self.height
        self.velocidade = 0

        try:
            self.sprite_lava.image = pygame.transform.scale(self.sprite_lava.image, (int(self.width * 2), int(self.height)))

        except Exception as e:
            print(f"Erro ao redimensionar imagem da Lava: {e}")
        
        #tempo de animacao:
        self.sprite_lava.set_total_duration(800)
        
        #posicionamento:
        self.x = 0
        self.y = janela.height - janela.height/15
        self.espaco = False

    #aqui definimos como a lava funciona de acordo com o jogador:
    def lava_jogador(self, jogador):

        #vamos ver se a lava pode comecar a subir:
        if (self.teclado.key_pressed("SPACE") or self.teclado.key_pressed("W")):
            self.espaco = True

        #definindo uma velocidade para nossa lava
        self.velocidade = 5

        #a logica de funcionamento da logica espera o teclado espaco ser pressionado:
        if (self.espaco):
            #caso de o jogador estar parado:
            if (jogador.subindo == False):
                    self.y -= self.velocidade*self.janela.delta_time()
            
            #caso de o jogador estar pulando
            else:
                #vamos adicionar um minimo para o tamanho da lava:
                if (self.y < self.janela.height - 10):
                    self.y += self.velocidade*4*self.janela.delta_time()
        
    def desenhar(self): 
        self.sprite_lava.set_position(self.x, self.y)
        self.sprite_lava.update()
        self.sprite_lava.draw()