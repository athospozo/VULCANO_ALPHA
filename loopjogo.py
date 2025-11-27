# Em: biblioteca/loopjogo.py
import pygame 
import random 
from PPlay.keyboard import *
from PPlay.collision import *
from PPlay.mouse import *
from PPlay.sprite import *
from PPlay.window import *
from PPlay.gameobject import *
from PPlay.gameimage import *
from personagem import Personagem
from lava import lava
from camera import Camera
from plataforma import *

def loopjogo(janela, mouse, gm1, teclado, PLAY, MENU, RANKING):
    
    contador = 100
    fps = 0
    camera = Camera(janela)
    camera.scroll_limit_tela = janela.height * 0.33 

    largura_plat = 424
    altura_plat = 87
    pos_y_plataforma = janela.height / 2 + 150 
    
    gerenciador_plat = Plataforma(
        imagem_path='ARTES/plataforma1.png',
        x_centro=janela.width / 2,
        y_pos=pos_y_plataforma,
        largura=largura_plat,
        altura=altura_plat,
        janela=janela
    )
    
    altura_jogador = 80
    largura_jogador = 60
    pos_x_jogador = janela.width / 2
    pos_y_jogador = gerenciador_plat.y
    
    jogador = Personagem(
        xinicial=pos_x_jogador,
        yinicial=pos_y_jogador,
        altura=altura_jogador,
        largura=largura_jogador,
        plataforma1=gerenciador_plat.lista[0]
    )
    jogador.no_chao = True 
    
    obstaculo = lava(jogador, janela)
        
    while PLAY:
        contador += 1

        if teclado.key_pressed("ESC"):
            PLAY = False
            MENU = True
            RANKING = False
            return PLAY, MENU, RANKING
        
        #plataformas
        gerenciador_plat.criacao_plataformas(janela)
        gerenciador_plat.remocao_plataformas(janela)
    
        # Ordem: Jogador primeiro, Câmera depois
        jogador.jogador_plataformas(gerenciador_plat.lista)
        jogador.atualizar(janela, teclado)
        obstaculo.atualizar()

        # Lógica de Game Over (Usa camera.y atualizado)
        pe_jogador_na_tela_y = (jogador.y - camera.y) + jogador.height
        
        if pe_jogador_na_tela_y > obstaculo.y:
            PLAY = False
            MENU = True
            RANKING = False
            return PLAY, MENU, RANKING
        
        gm1.draw() 

        #FPS
        if contador % 100 == 0:
            dt = janela.delta_time()
            if dt > 0:
                fps = 1 / dt
            else:
                fps = 0
        janela.draw_text(f"FPS: {int(fps)}", 10, 10, size=20, color=(255, 255, 255))

        # Desenho
        gerenciador_plat.desenhar_plataformas(camera)
        jogador.desenhar(camera)
        obstaculo.desenhar()
        janela.update()
        
    return PLAY, MENU, RANKING