import random
import pygame
from PPlay.sprite import Sprite
from PPlay.keyboard import *
import os
import sys

#Funcao para o executavel
def resolver_caminho(arquivo):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, arquivo)

class Plataforma:
    #definindo caracteristicas iniciais:
    def __init__(self, janela):
        
        #basicos:
        self.janela = janela
        self.teclado = Keyboard()
        self.lista = []
        self.poderes = []

        #definindo as medidas dos sprites
        self.width = self.janela.width//5
        self.height = self.janela.height//20

        #criando uma plataforma inicial:
        primeira = Sprite(resolver_caminho("ARTES/plataforma1.png"))
        primeira.x = self.janela.width/2 - self.width/2
        primeira.y = self.janela.height - self.janela.height/4
        primeira.poder = False

        #redefinindo o tamanho do sprite:
        try:
            primeira.image = pygame.transform.scale(primeira.image, (int(self.width), int(self.height)))
        except Exception as e:
            print(f"Erro ao redimensionar plataforma: {e}")

        #armazenando ele
        self.lista.append(primeira)

        #definindo medidas para geracao aleatoria de plataformas:
        self.gap = self.janela.height/4

        #para acrescentar uma certa dificuldade:
        self.velocidade_base = self.janela.width/6

        #para inicializar o jogo
        self.apertou_espaco = False

        #definindo quando as plataformas tem poder nelas:
        self.contagem = 1

    '''#aqui vamos colocar o poder naa plataforma:
    def adiciona_poder (self, plataforma):

        #vamos gerar o sprite do poder:
        poder = Sprite(resolver_caminho("ARTES/coin.png"))
        poder.width = self.width/3
        poder.height = self.height*2

        #redefinindo o tamanho do sprite:
        try:
            poder.image = pygame.transform.scale(poder.image, (int(self.width/3), int(self.height*2)))
        except Exception as e:
            print(f"Erro ao redimensionar plataforma: {e}")
    
        #vamos definir as posicoes:
        poder.x = plataforma.x + plataforma.width/2 - poder.width/2
        poder.y = plataforma.y - poder.height*3

        return poder'''

    #funcao que vai auxiliar numa melhor criacao de plataformas
    def escolhe_x(self):
        ultima = self.lista[-1]

        #distancia entre uma plataforma e outra
        gap_minimo = 10 
        gap_maximo = int(self.width * 0.4) 

        #lado direito ou esquerdo
        lado = random.choice([1, 2])

        #LADO ESQUERO:
        if lado == 1:
            limite_min = int(ultima.x - self.width - gap_maximo)
            limite_max = int(ultima.x - self.width - gap_minimo)

            if limite_max > 0:
                inicio = max(0, limite_min)
                fim = limite_max
                if inicio < fim:
                    return random.randint(inicio, fim)

        #LADO DIREITO:
        if (lado == 2):
            limite_min = int(ultima.x + ultima.width + gap_minimo)
            limite_max = int(ultima.x + ultima.width + gap_maximo)

            if limite_min < self.janela.width - self.width:
                inicio = limite_min
                fim = min(int(self.janela.width - self.width), limite_max)
                if inicio < fim:
                    return random.randint(inicio, fim)

        #caso nenhuma condicao seja satisfeita, tenta recursivamente (cuidado com recursão infinita, mas ok por enquanto)
        return (self.escolhe_x())

    def escolhe_y (self):
        ultima = self.lista[-1]
        y = ultima.y - self.gap
        return y
        
    #mantendo uma lista de plataformas de 15 elementos:
    def criacao_plataformas (self):
        i = len(self.lista) - 1
        while ((i+1 < 15)):

            '''#vamos iterar nossa contagem a cada vez que uma plataforma é adicionada:
            self.contagem += 1'''
            
            x = self.escolhe_x()
            y = self.escolhe_y()
            
            nova_plataforma = Sprite(random.choice([resolver_caminho("ARTES/plataforma1.png"),
                                                    resolver_caminho("ARTES/plataforma2.png"),
                                                     resolver_caminho("ARTES/plataforma3.png")]))

            try:
                nova_plataforma.image = pygame.transform.scale(nova_plataforma.image, (int(self.width), int(self.height)))
            except Exception as e:
                print(f"Erro ao redimensionar plataforma: {e}")

            nova_plataforma.x = x
            nova_plataforma.y = y 

            '''#vamos adicionar o poder:
            nova_plataforma.poder = False'''

            '''if (self.contagem % 15 == 0):
                nova_plataforma.poder = True
                nova_plataforma.moedinha = self.adiciona_poder(nova_plataforma)'''

            direcao = random.choice([-1, 1])
            nova_plataforma.vx = self.velocidade_base * direcao

            self.lista.append(nova_plataforma)
            i += 1   

    def remocao_plataformas(self, janela):
        for plataforma in self.lista:
            if plataforma.y > janela.height:
                self.lista.remove(plataforma)
    
    def dificuldade (self, dt):
        for plataforma in self.lista:
            plataforma.x += plataforma.vx * dt
            if plataforma.x <= 0:
                plataforma.x = 0
                plataforma.vx = -plataforma.vx 
            elif plataforma.x + self.width >= self.janela.width:
                plataforma.x = self.janela.width - self.width
                plataforma.vx = -plataforma.vx
    
    def desenhar_plataformas (self, personagem):

        if (self.teclado.key_pressed("SPACE") or self.teclado.key_pressed("W")):
            self.apertou_espaco = True

        if (personagem.qnte_pulos > 15):
            self.dificuldade(personagem.dt)
        
        for plataforma in self.lista:
            # Mecanica de Scrolling: se o personagem sobe, a plataforma desce
            if (personagem.subindo):
                plataforma.y = plataforma.y + personagem.gravidade/7*self.janela.delta_time()

                if (personagem.y < self.janela.height/4):
                    plataforma.y = plataforma.y + personagem.gravidade/14*self.janela.delta_time()

            # Scrolling constante inicial
            if (self.apertou_espaco):
                plataforma.y += 20/2*self.janela.delta_time()
        
            plataforma.set_position(plataforma.x, plataforma.y)
            plataforma.draw()

            '''if plataforma.poder: 
                # Atualiza a posição da moeda para acompanhar a plataforma
                plataforma.moedinha.y = plataforma.y - plataforma.moedinha.height * 1.5
                
                # Desenha a moeda
                plataforma.moedinha.set_position(plataforma.moedinha.x, plataforma.moedinha.y)
                plataforma.moedinha.draw()'''