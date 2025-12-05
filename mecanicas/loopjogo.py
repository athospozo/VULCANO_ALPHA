import pygame 
import random 
from PPlay.keyboard import *
from PPlay.collision import *
from PPlay.mouse import *
from PPlay.sprite import *
from PPlay.window import *
from PPlay.gameobject import *
from PPlay.gameimage import *
from mecanicas.personagem import Jogador
from mecanicas.lava import lava
from mecanicas.camera import Camera
from mecanicas.plataforma import *

def loopjogo(janela, mouse, gm1, teclado, PLAY, MENU, RANKING):
    contador = 100
    camera = Camera(janela)
    camera.scroll_limit_tela = janela.height * 0.33 
    
    gerenciador_plat = Plataforma(janela)
    
    jogador = Jogador(janela, gerenciador_plat.lista[0])

    obstaculo = lava(janela)
        
    while PLAY:

        if teclado.key_pressed("ESC"):
            PLAY = False
            MENU = True
            RANKING = False
            return PLAY, MENU, RANKING
        
        #plataformas
        gerenciador_plat.criacao_plataformas()
        gerenciador_plat.remocao_plataformas(janela)

        # Lógica de Game Over (Usa camera.y atualizado)
        pe_jogador_na_tela_y = (jogador.y - camera.y) + jogador.height
        
        if pe_jogador_na_tela_y > obstaculo.y:
            PLAY = False
            MENU = True
            RANKING = False
            return PLAY, MENU, RANKING
        
        obstaculo.lava_jogador(jogador)
        gm1.draw() 

        # Desenho
        gerenciador_plat.desenhar_plataformas(jogador)

        jogador.desenha(gerenciador_plat.lista)

        obstaculo.desenhar()

        janela.update()
        
    return PLAY, MENU, RANKING