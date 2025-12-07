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
            primeira.image = pygame.transform.scale(primeira.image, (self.width, self.height))
        except Exception as e:
            print(f"Erro ao redimensionar plataforma: {e}")

        #armazenando ele
        self.lista.append(primeira)

        #definindo medidas paara geracao aleatoria de plataformas:
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
            
            #mais longe da outra plataforma:
            limite_min = int(ultima.x - self.width - gap_maximo)
            #mais perto:
            limite_max = int(ultima.x - self.width - gap_minimo)

            #verificando se cabe na tela
            if limite_max > 0:

                inicio = max(0, limite_min)
                fim = limite_max
                
                if inicio < fim:
                    return random.randint(inicio, fim)

        #LADO DIREITO:
        if (lado == 2):
           
            #mais perto:
            limite_min = int(ultima.x + ultima.width + gap_minimo)
            #mais longe:
            limite_max = int(ultima.x + ultima.width + gap_maximo)

            #verificando se cabe na tela:
            if limite_min < self.janela.width - self.width:

                inicio = limite_min
                fim = min(self.janela.width - self.width, limite_max)
                
                if inicio < fim:
                    return random.randint(inicio, fim)

        #caso nenhuma condicao seja satisfeita:
        return int(self.escolhe_x())

    def escolhe_y (self):

        #pegamos a ultima plataforma
        ultima = self.lista[-1]

        #nossa distancia será constante
        y = ultima.y - self.gap

        return y
        
    #mantendo uma lista de plataformas de 15 elementos:
    def criacao_plataformas (self):
        
        #criando um i de acordo com a quantidade de vezes que precisaremos gerar uma plataforma
        i = len(self.lista) - 1
        
        while ((i+1 < 15)):

            #decidindo posicoes:
            x = self.escolhe_x()
            y = self.escolhe_y()
            
            #escolhendo plataforma nova:
            nova_plataforma = Sprite(random.choice(["ARTES/plataforma1.png", "ARTES/plataforma2.png", "ARTES/plataforma3.png"]))

            #redefinindo o tamanho do sprite:
            try:
                nova_plataforma.image = pygame.transform.scale(nova_plataforma.image, (self.width, self.height))
            except Exception as e:
                print(f"Erro ao redimensionar plataforma: {e}")

            #posicionando a nova plataforma
            nova_plataforma.x = x
            nova_plataforma.y = y 

            # Define a velocidade individual da plataforma
            direcao = random.choice([-1, 1])
            nova_plataforma.vx = self.velocidade_base * direcao

            #armazenando
            self.lista.append(nova_plataforma)
        
            i += 1   

    #removendo plataformas que sairam do frame
    def remocao_plataformas(self, janela):
        for plataforma in self.lista:
            if plataforma.y > janela.height:
                self.lista.remove(plataforma)
    
    def dificuldade (self, dt):

        # Percorre cada plataforma individualmente
        for plataforma in self.lista:
            
            plataforma.x += plataforma.vx * dt

            # Bateu na esquerda
            if plataforma.x <= 0:
                plataforma.x = 0
                plataforma.vx = -plataforma.vx # Inverte a velocidade dela
            
            # Bateu na direita
            elif plataforma.x + self.width >= self.janela.width:
                plataforma.x = self.janela.width - self.width
                plataforma.vx = -plataforma.vx
    
    #desenho
    def desenhar_plataformas (self, personagem):

        #mecanica que comeca apenas se espaco for apertado:
        if (self.teclado.key_pressed("SPACE") or self.teclado.key_pressed("W")):
            self.apertou_espaco = True

        #depois de 30 pulos o eixo horizontal se movimenta
        if (personagem.qnte_pulos > 15):
            self.dificuldade(personagem.dt)
        
        for plataforma in self.lista:

            #se o personagem pula nossa plataforma desce mais
            if (personagem.subindo):
                plataforma.y = plataforma.y + personagem.gravidade/7*self.janela.delta_time()
                #vamos verificar se o personagem esta muito em cima:
                if (personagem.y < self.janela.height/4):
                    plataforma.y = plataforma.y + personagem.gravidade/14*self.janela.delta_time()
            
            #espera o espaco para comecar:
            if (self.apertou_espaco):
                plataforma.y += 20/2*self.janela.delta_time()

            plataforma.set_position(plataforma.x, plataforma.y)
            plataforma.draw()