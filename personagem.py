# Em: biblioteca/personagem.py

import pygame 
from PPlay.animation import *
from PPlay.window import *
from PPlay.sprite import *
from PPlay.keyboard import *

class Personagem:
    def __init__(self, xinicial, yinicial, altura, largura, plataforma1):

        #gerando os sprites
        self.anim_parado = Animation("ARTES/parado.png", 2)
        self.anim_esquerda = Animation ("ARTES/esquerda.png", 4)
        self.anim_direita = Animation ("ARTES/direita.png", 4)

        #definindo os tamanhos
        self.width = largura
        self.height = altura
        self.anim_direita.height = self.anim_esquerda.height = self.anim_parado.height = self.height
        self.anim_direita.width = self.anim_esquerda.width = self.anim_parado.width = self.width

        try:
            self.anim_parado.image = pygame.transform.scale(self.anim_parado.image, (self.width * 2, self.height))
            self.anim_esquerda.image = pygame.transform.scale(self.anim_esquerda.image, (self.width * 4, self.height))
            self.anim_direita.image = pygame.transform.scale(self.anim_direita.image, (self.width * 4, self.height))
        except Exception as e:
            print(f"Erro ao redimensionar imagens do Personagem: {e}")

        #definindo o tempo da animacao
        self.anim_parado.set_total_duration(1000)
        self.anim_direita.set_total_duration(500)
        self.anim_esquerda.set_total_duration(500)

        #definicoes basicas
        self.agora = self.anim_parado
        self.x = plataforma1.x + plataforma1.width / 2 - self.width / 2
        self.y = plataforma1.y - plataforma1.height*2

        #fisica do movimento
        self.velocidade_horizontal = 200
        self.velocidade_y = 0
        self.gravidade_forca = 1200
        self.forca_pulo = -800
        self.velocidade_max_queda = 2000 
        self.velocidade_max_pulo = -2500
        self.no_chao = False

        self.margem_de_colisao = 15
        self.colidindo = True
    
    def jogador_plataformas(self, objetos):
        #detecta a colisao (a ser aprimorado), com isso determina os booleanos gravidade e colidindo(permissao para pular)
        for objeto in objetos:
            if self.x  + self.agora.width >= objeto.x and self.x <= objeto.x + objeto.width:
                self.colidindo = True
                ''''if self.y + self.agora.height <= objeto.y + objeto.height/2 and self.y + self.agora.height > objeto.y + 5:
                    self.colidindo = False
                elif self.y >= objeto.y + objeto.height/2 and self.y < objeto.y + objeto.height:
                    self.gravidade = True
                    self.colidindo =  True
                else:
                    self.colidindo = False
                    self.gravidade = True'''
                if self.colidindo:
                    if (self.velocidade_y >= 0) and abs((self.y + self.height) - objeto.y) < self.margem_de_colisao:
                        self.y = objeto.y - objeto.height 
                        self.velocidade_y = 0      
                        self.no_chao = True        
                        break 
                    if (self.velocidade_y < 0) and abs(self.y - (objeto.y + objeto.height)) < self.margem_de_colisao:
                        self.y = objeto.y + objeto.height
                        self.velocidade_y = 0 
                        break

    def atualizar(self, janela, teclado):
        # --- TRAVA DE SEGURANÇA 1: DELTA_TIME ---
        dt = janela.delta_time()
        if dt > 0.1: # Se o lag for > 0.1s
            dt = 0.016 # Use um valor normal
        # --- FIM DA TRAVA 1 ---
        
        # Pulo
        if (teclado.key_pressed("SPACE") or teclado.key_pressed("W")) and self.no_chao:
            self.velocidade_y = self.forca_pulo # Vai usar -300
            self.no_chao = False 

        # Gravidade (usando 'dt' seguro)
        if not self.no_chao:
            self.velocidade_y += self.gravidade_forca * dt
        elif self.velocidade_y > 0:
            self.velocidade_y = 0 
            
        # --- TRAVA DE SEGURANÇA 2: VELOCIDADE TERMINAL ---
        if self.velocidade_y > self.velocidade_max_queda:
            self.velocidade_y = self.velocidade_max_queda
        if self.velocidade_y < self.velocidade_max_pulo:
            self.velocidade_y = self.velocidade_max_pulo
        # --- FIM DA TRAVA 2 ---
            
        # Movimento Vertical (usando 'dt' seguro)
        self.y += self.velocidade_y * dt

        # Movimento Horizontal (usando 'dt' seguro)
        if teclado.key_pressed("A") or teclado.key_pressed("LEFT"):
            self.agora = self.anim_esquerda
            if self.x > 0: 
                self.x -= self.velocidade_horizontal * dt
        elif teclado.key_pressed("D") or teclado.key_pressed("RIGHT"):
            self.agora = self.anim_direita
            if self.x < janela.width - self.width:
                self.x += self.velocidade_horizontal * dt
        else:
            if self.no_chao:
                self.agora = self.anim_parado
        self.agora.update()

    def desenhar(self, camera):
        screen_y = self.y - camera.y
        self.agora.set_position(self.x, screen_y)
        self.agora.draw()