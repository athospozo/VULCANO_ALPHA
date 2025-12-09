from PPlay.animation import *
from PPlay.keyboard import *
from PPlay.window import *
import pygame
import random

class Jogador:

    #definicao de caracteristicas basicas
    def __init__ (self, janela, direita, esquerdo, parado, pulo, plataforma1):

        #definindo sons:
        self.jump = pygame.mixer.Sound(pulo)

        #definicooes basicas:
        self.teclado = Keyboard()
        self.janela = janela
        self.dt = 0

        #primeiro a geracao de personagem:
        self.anim_parado = Animation(parado, 2)
        self.anim_esquerda = Animation (esquerdo, 4)
        self.anim_direita = Animation (direita, 4)

        #agora definimos as medidas dos sprites:
        self.width = self.janela.width/25
        self.height = self.janela.height/20
        self.anim_direita.height = self.anim_esquerda.height = self.anim_parado.height = self.height
        self.anim_direita.width = self.anim_esquerda.width = self.anim_parado.width = self.width

        #vamos entao colocar os sprites de acordo com os tamanhos definidos:
        try:
            self.anim_parado.image = pygame.transform.scale(self.anim_parado.image, (int(self.width * 2), int(self.height)))
            self.anim_esquerda.image = pygame.transform.scale(self.anim_esquerda.image, (int(self.width * 4), int(self.height)))
            self.anim_direita.image = pygame.transform.scale(self.anim_direita.image, (int(self.width * 4), int(self.height)))
        except Exception as e:
            print(f"Erro ao redimensionar imagens do Personagem: {e}")

        #definindo o tempo das animacoes dos sprites
        self.anim_parado.set_total_duration(1000)
        self.anim_direita.set_total_duration(500)
        self.anim_esquerda.set_total_duration(500)

        #definindo posicoes iniciais:
        self.agora = self.anim_parado
        self.x = plataforma1.x + plataforma1.width / 2 - self.width / 2
        self.y = plataforma1.y - plataforma1.height*2

        #fisica do movimento horizontal:
        self.velocidade_horizontal = self.janela.width/4
        self.no_chao = True

        #fisica do movimento vertical:
        self.velocidade_vertical = 0
        self.gravidade = self.janela.height*7
        self.forca_pulo = self.janela.height*1.5
        self.jumping = False

        #variavel para propósitos externos à classe
        self.subindo = False
        self.qnte_pulos = 0

        #definindo se o jogador tem poder ou nao:
        self.tipo_poder = None
        self.guarda_pulo = 1
        self.espaco_apertado = False
    
    def escolhe_poder (self):
        #self.tipo_poder = random.choice(["LAVA", "PULO"])
        self.tipo_poder = "PULO"
    
    #definindo quando ha uma colisao de personagem com outro sprite:
    def colisao (self, possivel_colisao):
        #sobreposição no eixo x:
        if ((self.x <= possivel_colisao.x + possivel_colisao.width) and
            (self.x + self.width >= possivel_colisao.x)):

            #averiguando colisao por cima:
            if ((self.y + self.height >= possivel_colisao.y - 2) and
                (self.y + self.height <= possivel_colisao.y + possivel_colisao.height/2)): 
                return 1
            
            #averiguando colisao por baixo:
            if ((self.y >= possivel_colisao.y + possivel_colisao.height/2) and
                (self.y <= possivel_colisao.y + possivel_colisao.height)): 
                return -1
            
        return 0
            
    #definindo como o personagem interage com as plataformas:
    def personagem_plataformas (self, lista_plataformas):
        self.no_chao = False
        for plataforma in lista_plataformas:
            if ((plataforma.y >= -20) and
                (plataforma.y + plataforma.height <= self.janela.height + 20)):
                
                '''#vamos verificar se fez colisao com a moedinha de poder:
                if (plataforma.poder):
                    if (self.colisao(plataforma.moedinha) != 0):
                        plataforma.poder = False
                        self.escolhe_poder()'''
        
                self.aux = self.colisao(plataforma)

                #verificamos se é colisao por cima
                if (self.aux == 1):
                    if self.velocidade_vertical >= 0:
                        self.y = plataforma.y - self.height
                        self.velocidade_vertical = 0
                        self.no_chao = True
                        self.jumping = False
                        if (self.qnte_pulos > 15):
                            self.x += plataforma.vx * self.dt

                #verificamos se é colisao por baixo
                elif (self.aux == -1):
                    self.y = (plataforma.y + plataforma.height) + 10
                    self.no_chao = False
                    self.velocidade_vertical = 4
                    if ((self.jumping) and (self.velocidade_vertical > 0)):
                        self.velocidade_vertical = 0
                    
    def pulo (self):

        if (((self.teclado.key_pressed("SPACE")) or (self.teclado.key_pressed("W"))) and (self.no_chao == True)
            and (self.jumping == False)):
            self.jumping = True
            self.no_chao = False
            self.velocidade_vertical = -self.forca_pulo
            self.qnte_pulos += 1
            self.guarda_pulo += 1
            self.espaco_apertado = True
            self.jump.play()
    
    '''def pulo_duplo (self):

        if (((self.teclado.key_pressed("SPACE")) or (self.teclado.key_pressed("W"))) 
            and (self.tipo_poder == "PULO") and (self.espaco_apertado) and (self.jumping)):
            self.espaco_apertado = False
            self.velocidade_vertical = -self.forca_pulo
            self.guarda_pulo += 1
            self.jump.play()'''


    def mov (self):

        self.velocidade_vertical += self.gravidade*self.dt

        self.agora = self.anim_parado

        if (self.teclado.key_pressed("A") or self.teclado.key_pressed("LEFT")):
            self.agora = self.anim_esquerda
            self.x -= self.velocidade_horizontal * self.dt
        
        if (self.teclado.key_pressed("D") or self.teclado.key_pressed("RIGHT")):
            self.agora = self.anim_direita
            self.x += self.velocidade_horizontal * self.dt

        # Limites da tela
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > self.janela.width:
            self.x = self.janela.width - self.width

        # Atualiza Y
        if (self.no_chao == False):
            self.y += (self.velocidade_vertical * self.dt)
    
    def desenha (self, lista_plataformas):
        self.subindo = False
        self.dt = self.janela.delta_time()
        
        self.personagem_plataformas (lista_plataformas)
        self.pulo()
        if (self.tipo_poder == "PULO"):
            self.pulo_duplo()
        
        if (self.velocidade_vertical < 0):
            self.subindo = True

        self.mov()

        self.agora.set_position (self.x, self.y)
        self.agora.update()
        self.agora.draw()