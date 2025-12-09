import pygame
from PPlay.keyboard import *
from PPlay.mouse import *
from PPlay.window import *
from PPlay.gameimage import *

from mecanicas.menu import gamemenu
from mecanicas.loopjogo import loopjogo
from mecanicas.ranking import ranking, salvar_pontuacao 
from mecanicas.teclado import tela_game_over

pygame.init()
mouse = Mouse()
teclado = Keyboard()

janela_largura = 1000
janela_altura = 700
janela = Window(janela_largura, janela_altura)
janela.set_title('VULCANO')

# Sons
try:
    pygame.mixer.music.load("SONS/LavaLoop.wav")
except:
    pass # Se não tiver som, o jogo segue mudo sem crashar
        
# Imagens
gm1 = GameImage('ARTES/jogar1.png')
menu_img = GameImage('ARTES/menu.png')
ranking_img = GameImage('ARTES/menu.png') 

try:
    gm1.image = pygame.transform.scale(gm1.image, (janela_largura, janela_altura))
    menu_img.image = pygame.transform.scale(menu_img.image, (janela_largura, janela_altura))
    ranking_img.image = pygame.transform.scale(ranking_img.image, (janela_largura, janela_altura))
except:
    pass 

MENU = True
RANKING = False
PLAY = False
tempo_jogo = 0

while True:
    janela.set_background_color([0,0,0])

    if MENU:
        PLAY, MENU, RANKING = gamemenu(janela, mouse, menu_img, PLAY, MENU, RANKING)
    
    elif PLAY:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)
            
        PLAY, MENU, RANKING, tempo_jogo = loopjogo(janela, gm1, teclado, PLAY, MENU, RANKING)
        
        if tempo_jogo > 0:
            pygame.mixer.music.stop()
            
            # Chama a tela de digitar nome
            nome_jogador = tela_game_over(janela, tempo_jogo)
            
            # Salva silenciosamente (sem print)
            if nome_jogador.strip() != "":
                salvar_pontuacao(nome_jogador, tempo_jogo)
            
            tempo_jogo = 0
            PLAY = False
            MENU = False
            RANKING = True 
    
    elif RANKING:
        PLAY, MENU, RANKING = ranking(janela, teclado, ranking_img, PLAY, MENU, RANKING)

    janela.update()