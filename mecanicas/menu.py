from PPlay.mouse import *
from PPlay.gameobject import *

def gamemenu(janela, mouse, menu, PLAY, MENU, RANKING):
    
    #botao play
    play = GameObject()
    play.x = janela.width * 0.3302
    play.y = janela.height * 0.5305
    play.width = janela.width * 0.3359
    play.height = janela.height * 0.0722

    #botao ranking
    ranking = GameObject()
    ranking.x= janela.width * 0.3302
    ranking.y = janela.height * 0.6426
    ranking.width = janela.width * 0.3359
    ranking.height = janela.height * 0.0630

    #botao sair
    sair = GameObject()
    sair.x = janela.width * 0.3302
    sair.y = janela.height * 0.7537
    sair.width = janela.width * 0.3359
    sair.height = janela.height * 0.0713
    
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