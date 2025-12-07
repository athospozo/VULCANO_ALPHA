import pygame
from PPlay.keyboard import *
from PPlay.mouse import *
from PPlay.window import *
from PPlay.gameimage import *

from mecanicas.menu import gamemenu
from mecanicas.loopjogo import loopjogo
from mecanicas.ranking import ranking, salvar_pontuacao 

pygame.init()
mouse = Mouse()
teclado = Keyboard()

janela_largura = 1000
janela_altura = 500
janela = Window(janela_largura, janela_altura)
janela.set_title('VULCANO')

# Carregamento das imagens de fundo (certifique-se que elas existem na pasta ARTES)
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

# Variável para armazenar o tempo retornado pelo jogo
tempo_jogo = 0

while True:
    
    janela.set_background_color([0,0,0])

    if MENU:
        PLAY, MENU, RANKING = gamemenu(janela, mouse, menu_img, PLAY, MENU, RANKING)
    
    elif PLAY:
        # Chama o loop do jogo e espera 4 valores de retorno (incluindo o tempo)
        PLAY, MENU, RANKING, tempo_jogo = loopjogo(janela, mouse, gm1, teclado, PLAY, MENU, RANKING)
        
        # Se o tempo for maior que 0, significa que o jogador morreu
        if tempo_jogo > 0:
            print("\n" + "="*40)
            print(f"FIM DE JOGO! Você sobreviveu: {tempo_jogo:.2f} segundos.")
            # Pequeno delay para não bugar o input do nome
            janela.delay(500)
            
            # Nota: O input aqui é no terminal. Para input na janela seria necessário outra lógica.
            nome = input("Digite seu nome para o Ranking: ")
            
            if nome.strip() != "":
                salvar_pontuacao(nome, tempo_jogo)
                print("Pontuação Salva com sucesso!")
            else:
                print("Nome vazio, pontuação não salva.")
                
            print("="*40 + "\n")
            
            # Zera o tempo para não pedir de novo
            tempo_jogo = 0
    
    elif RANKING:
        PLAY, MENU, RANKING = ranking(janela, teclado, ranking_img, PLAY, MENU, RANKING)

    janela.update()