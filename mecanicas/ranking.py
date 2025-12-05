# Em: biblioteca/ranking.py

from PPlay.keyboard import *
from PPlay.collision import *
from PPlay.mouse import *
from PPlay.sprite import *
from PPlay.window import *
from PPlay.gameobject import *
from PPlay.gameimage import *

def ranking(janela, teclado, ranking_img, PLAY, MENU, RANKING):
    
    if teclado.key_pressed("ESC"):
        PLAY = False
        MENU = True
        RANKING = False

    ranking_img.draw()
    janela.draw_text("RANKING (ALPHA)", janela.width / 2 - 150, 200, size=48, color=(255, 255, 255))
    janela.draw_text("Pressione [ESC] para voltar", janela.width / 2 - 180, 800, size=32, color=(255, 255, 255))

    return PLAY, MENU, RANKING