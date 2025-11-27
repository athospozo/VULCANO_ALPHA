# Em: main.py

import pygame
from PPlay.keyboard import *
from PPlay.collision import *
from PPlay.mouse import *
from PPlay.sprite import *
from PPlay.window import *
from PPlay.gameobject import *
from PPlay.gameimage import *

from menu import gamemenu
from loopjogo import loopjogo
from ranking import ranking

pygame.init()
mouse = Mouse()
teclado = Keyboard()

janela_largura = 1920
janela_altura = 1080
janela = Window(janela_largura, janela_altura)
janela.set_title('VULCANO')

gm1 = GameImage('ARTES/jogar1.png')
menu_img = GameImage('ARTES/menu.png')
ranking_img = GameImage('ARTES/menu.png') 

MENU = True
RANKING = False
PLAY = False

while True:
    
    janela.set_background_color([0,0,0])

    if MENU:
        PLAY, MENU, RANKING = gamemenu(janela, mouse, menu_img, teclado, PLAY, MENU, RANKING)
    
    elif PLAY:
        PLAY, MENU, RANKING = loopjogo(janela, mouse, gm1, teclado, PLAY, MENU, RANKING)
    
    elif RANKING:
        PLAY, MENU, RANKING = ranking(janela, teclado, ranking_img, PLAY, MENU, RANKING)

    janela.update()