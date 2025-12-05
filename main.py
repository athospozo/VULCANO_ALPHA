# Em: main.py

import pygame
from PPlay.keyboard import *
from PPlay.collision import *
from PPlay.mouse import *
from PPlay.sprite import *
from PPlay.window import *
from PPlay.gameobject import *
from PPlay.gameimage import *

from mecanicas.menu import gamemenu
from mecanicas.loopjogo import loopjogo
from mecanicas.ranking import ranking

pygame.init()
mouse = Mouse()
teclado = Keyboard()

janela_largura = 1000
janela_altura = 500
janela = Window(janela_largura, janela_altura)
janela.set_title('VULCANO')

gm1 = GameImage('ARTES/jogar1.png')
menu_img = GameImage('ARTES/menu.png')
ranking_img = GameImage('ARTES/menu.png') 

try:
    gm1.image = pygame.transform.scale(gm1.image, (janela_largura, janela_altura))
    menu_img.image = pygame.transform.scale(menu_img.image, (janela_largura, janela_altura))
    ranking_img.image = pygame.transform.scale(ranking_img.image, (janela_largura, janela_altura))
except Exception as e:
    print(f"Erro ao redimensionar imagens de fundo: {e}")

MENU = True
RANKING = False
PLAY = False

while True:
    
    janela.set_background_color([0,0,0])

    if MENU:
        PLAY, MENU, RANKING = gamemenu(janela, mouse, menu_img, PLAY, MENU, RANKING)
    
    elif PLAY:
        PLAY, MENU, RANKING = loopjogo(janela, mouse, gm1, teclado, PLAY, MENU, RANKING)
    
    elif RANKING:
        PLAY, MENU, RANKING = ranking(janela, teclado, ranking_img, PLAY, MENU, RANKING)

    janela.update()