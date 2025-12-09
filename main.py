import pygame
from PPlay.keyboard import *
from PPlay.mouse import *
from PPlay.window import *
from PPlay.gameimage import *
import os
import sys

from mecanicas.menu import gamemenu
from mecanicas.loopjogo import loopjogo
from mecanicas.ranking import ranking, salvar_pontuacao 
from mecanicas.teclado import tela_game_over

# --- CONFIGURAÇÃO PARA EXECUTÁVEL ---
def resolver_caminho(arquivo):
    try:
        # Se estiver rodando como .exe (PyInstaller)
        base_path = sys._MEIPASS
    except AttributeError:
        # Se estiver rodando no Python normal
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, arquivo)

# TRUQUE DE MESTRE: Muda o diretório de trabalho para a pasta do executável.
# Isso faz com que seus outros arquivos (personagem.py, lava.py) encontrem
# as imagens "ARTES/..." sem precisar mudar o código deles.
if hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

pygame.init()
mouse = Mouse()
teclado = Keyboard()

#Funcao para o executavel
def resolver_caminho(arquivo):
    
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, arquivo)

#Sprite lava:
img_lava_path = resolver_caminho("ARTES/lava.png")

#Sprite personagem:
img_direita_path = resolver_caminho("ARTES/direita.png")
img_esquerda_path = resolver_caminho("ARTES/esquerda.png")
img_parado_path = resolver_caminho("ARTES/parado.png")

#Som pulo:
pulo = resolver_caminho("SONS/jump.wav")

#Som morte:
morte = ("SONS/lava.flac")


janela_largura = 1000
janela_altura = 700
janela = Window(janela_largura, janela_altura)
janela.set_title('VULCANO')

#definindo som:
#sons:
pygame.mixer.music.load("SONS/LavaLoop.wav")
        
# Carregamento das imagens de fundo (certifique-se que elas existem na pasta ARTES)
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
        pygame.mixer.music.play(-1)
        # Chama o loop do jogo e espera 4 valores de retorno (incluindo o tempo)
        PLAY, MENU, RANKING, tempo_jogo = loopjogo(janela, gm1, img_lava_path,
                                                   img_direita_path, img_esquerda_path,
                                                    img_parado_path, teclado,
                                                     PLAY, MENU, RANKING, pulo, morte)
        
        if tempo_jogo > 0:
            pygame.mixer.music.stop()
            
            # Chama a tela de digitar nome (Sua lógica gráfica)
            nome_jogador = tela_game_over(janela, tempo_jogo)
            
            # Salva pontuação
            if nome_jogador.strip() != "":
                salvar_pontuacao(nome_jogador, tempo_jogo)
            
            tempo_jogo = 0
            PLAY = False
            MENU = False
            RANKING = True 
    
    elif RANKING:
        PLAY, MENU, RANKING = ranking(janela, teclado, ranking_img, PLAY, MENU, RANKING)

    janela.update()