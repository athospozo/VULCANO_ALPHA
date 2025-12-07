import random
import pygame
from PPlay.sprite import Sprite
from PPlay.keyboard import *

class Plataforma:
    #definindo caracteristicas iniciais:
    def __init__(self, janela):
        
        #basicos:
        self.janela = janela
        self.teclado = Keyboard()
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
            primeira.image = pygame.transform.scale(primeira.image, (int(self.width), int(self.height)))
        except Exception as e:
            print(f"Erro ao redimensionar plataforma: {e}")

        #armazenando ele
        self.lista.append(primeira)

        #definindo medidas para geracao aleatoria de plataformas:
        self.gap = self.janela.height/4

        #para acrescentar uma certa dificuldade:
        self.velocidade_base = self.janela.width/5

        #para inicializar o jogo
        self.apertou_espaco = False

    #funcao que vai auxiliar numa melhor criacao de plataformas
    def escolhe_x(self):
        ultima = self.lista[-1]

        #distancia entre uma plataforma e outra
        gap_minimo = 10 
        gap_maximo = int(self.width * 0.5) 

        #lado direito ou esuqerdo
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
        return int(self.janela.width/2)

    def escolhe_y (self):
        ultima = self.lista[-1]
        y = ultima.y - self.gap
        return y
        
    #mantendo uma lista de plataformas de 15 elementos:
    def criacao_plataformas (self):
        i = len(self.lista) - 1
        while ((i+1 < 15)):
            x = self.escolhe_x()
            y = self.escolhe_y()
            
            nova_plataforma = Sprite(random.choice(["ARTES/plataforma1.png", "ARTES/plataforma2.png", "ARTES/plataforma3.png"]))

            try:
                nova_plataforma.image = pygame.transform.scale(nova_plataforma.image, (int(self.width), int(self.height)))
            except Exception as e:
                print(f"Erro ao redimensionar plataforma: {e}")

            nova_plataforma.x = x
            nova_plataforma.y = y 

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