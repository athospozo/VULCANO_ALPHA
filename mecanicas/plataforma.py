# Em: biblioteca/plataforma.py
import random
import pygame
from PPlay.sprite import Sprite

class Plataforma:
    #definindo caracteristicas iniciais:
    def __init__(self, janela):
        
        #basicos:
        self.janela = janela
        self.lista = []
        self.listay = []

        #definindo as medidas dos sprites
        self.width = self.janela.width//5
        self.height = self.janela.height//20

        #criando uma plataforma inicial:
        primeira = Sprite("ARTES/plataforma1.png")
        primeira.x = self.janela.width/2 - self.width/2
        primeira.y = self.janela.height - self.janela.height/4

        #redefinindo o tamanho do sprite:
        try:
            primeira.image = pygame.transform.scale(primeira, (self.width, self.height))
        except Exception as e:
            print(f"Erro ao redimensionar plataforma: {e}")

        #armazenando ele
        self.lista.append(primeira)

        #definindo medidas paara geracao aleatoria de plataformas:
        self.espaco_vertical = self.janela.height/4.5

    #funcao que vai auxiliar numa melhor criacao de plataformas
    def guarda_y (self):
        #premissa:
        self.listay = []
        
        for plataformas in self.lista:
            self.listay.append(plataformas.y)

    #mantendo uma lista de plataformas de 15 elementos:
    def criacao_plataformas (self):
        
        #criando um i de acordo com a quantidade de vezes que precisaremos gerar uma plataforma
        i = len(self.lista) - 1
        
        while ((i+1 < 15)):

            #as decisoes vao se basear na ultima plataforma
            ultima_plataforma = self.lista[-1]

            novo_x_centro = -1
            #geracao aleatoria de um x:
            while ((novo_x_centro < 0 or novo_x_centro > self.janela.width) or 
                   (novo_x_centro > ultima_plataforma.x - self.width/2 and novo_x_centro < ultima_plataforma.x + self.width/2)):
                novo_x_centro = random.randint(int(ultima_plataforma.x - self.janela.width/5),
                                            int(ultima_plataforma.x/2 + ultima_plataforma.width + self.janela.width/5))
            
            nova_plataforma = Sprite(random.choice(["ARTES/plataforma1.png", "ARTES/plataforma2.png", "ARTES/plataforma3.png"]))

            #redefinindo o tamanho do sprite:
            try:
                nova_plataforma.image = pygame.transform.scale(nova_plataforma, (self.width, self.height))
            except Exception as e:
                print(f"Erro ao redimensionar plataforma: {e}")

            #posicionando a nova plataforma
            nova_plataforma.x = novo_x_centro - nova_plataforma.width / 2
            nova_plataforma.y = ultima_plataforma.y - self.espaco_vertical
            self.lista.append(nova_plataforma)

            i += 1   

    #removendo plataformas que sairam do frame
    def remocao_plataformas(self, janela):
        for plataforma in self.lista:
            if plataforma.y > janela.height:
                self.lista.remove(plataforma)
    
    #desenho
    def desenhar_plataformas (self, personagem):
        for plataforma in self.lista:
            if (personagem.subindo):
                plataforma.y = plataforma.y - personagem.velocidade_vertical*1.2*self.janela.delta_time()
            plataforma.set_position(plataforma.x, plataforma.y)
            plataforma.draw()