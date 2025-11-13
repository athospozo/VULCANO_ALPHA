# Em: biblioteca/menu.py

from PPlay.keyboard import *
from PPlay.collision import *
from PPlay.mouse import *
from PPlay.sprite import *
from PPlay.window import *
from PPlay.gameobject import *
from PPlay.gameimage import *
import random

def gamemenu(janela, mouse, menu,  teclado , PLAY,MENU,RANKING):
    
    play = GameObject()
    play.x = 634
    play.y = 573
    play.width = 1279 - 634
    play.height = 651 - 573
    ranking = GameObject()
    ranking.x= play.x
    ranking.y = 694
    ranking.width = play.width
    ranking.height = 762 - 694
    sair = GameObject()
    sair.x = play.x
    sair.y = 814
    sair.width = play.width
    sair.height = 891 - 814
    
    if mouse.is_over_object(play) and mouse.is_button_pressed(1):
        PLAY = True
        MENU = False
    elif mouse.is_over_object(ranking) and mouse.is_button_pressed(1):
        RANKING = True
        MENU = False
    elif mouse.is_over_object(sair) and mouse.is_button_pressed(1):
        janela.close()

    menu.draw()
    return PLAY, MENU, RANKING