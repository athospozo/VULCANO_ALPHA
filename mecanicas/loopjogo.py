import pygame 
import time
from PPlay.keyboard import *
from PPlay.collision import *
from PPlay.mouse import *
from PPlay.sprite import *
from PPlay.window import *
from PPlay.gameobject import *
from PPlay.gameimage import *

from mecanicas.personagem import Jogador
from mecanicas.lava import lava
from mecanicas.plataforma import *

def loopjogo(janela, gm1, teclado, PLAY, MENU, RANKING):

    morreu = pygame.mixer.Sound("SONS/lava.flac")

    # --- ALTERAÇÃO 1: Inicialização do Timer ---
    # Não pegamos o tempo agora. Apenas zeramos as variáveis.
    inicio_tempo = 0
    tempo_final = 0
    jogo_iniciou = False
    
    # Inicialização das Plataformas, Jogador e Obstáculo
    gerenciador_plat = Plataforma(janela)
    jogador = Jogador(janela, gerenciador_plat.lista[0])
    obstaculo = lava(janela)

    while PLAY:

        if teclado.key_pressed("ESC"):
            PLAY = False
            MENU = True
            RANKING = False
            # Retorna 0 no tempo pois saiu pelo ESC
            return PLAY, MENU, RANKING, 0
        
        # --- ALTERAÇÃO 2: Verificar início do jogo ---
        # Se o jogo ainda não iniciou (timer parado), esperamos o pulo
        if not jogo_iniciou:
            if teclado.key_pressed("SPACE") or teclado.key_pressed("W"):
                jogo_iniciou = True
                inicio_tempo = time.time()
        
        # Lógica das Plataformas
        gerenciador_plat.criacao_plataformas()
        gerenciador_plat.remocao_plataformas(janela)

        # Lógica de Game Over
        pe_jogador_na_tela_y = jogador.y + jogador.height
        
        if pe_jogador_na_tela_y > obstaculo.y:
            pygame.mixer.music.fadeout(2000)
            morreu.play()
            PLAY = False
            MENU = True
            RANKING = False
            
            # --- ALTERAÇÃO 3: Cálculo do tempo final ao morrer ---
            if jogo_iniciou:
                tempo_final = time.time() - inicio_tempo
            else:
                tempo_final = 0 # Morreu sem nem começar (raro, mas evita bugs)
                
            return PLAY, MENU, RANKING, tempo_final
        
        # Atualiza a lava e o Jogador
        obstaculo.lava_jogador(jogador)
        
        # Desenha o Fundo
        gm1.draw() 

        # Desenho dos objetos
        gerenciador_plat.desenhar_plataformas(jogador)
        jogador.desenha(gerenciador_plat.lista)
        obstaculo.desenhar()

        # --- HUD (CRONÔMETRO) ---
        # --- ALTERAÇÃO 4: Exibição condicional do tempo ---
        if jogo_iniciou:
            tempo_atual = time.time() - inicio_tempo
        else:
            tempo_atual = 0.0

        texto_tempo = f"{tempo_atual:.1f}s"

        largura_box = 110
        altura_box = 40
        x_box = janela.width - largura_box - 10
        y_box = 10

        # Desenha caixa do tempo
        pygame.draw.rect(janela.screen, (0, 0, 0), (x_box, y_box, largura_box, altura_box))
        pygame.draw.rect(janela.screen, (255, 255, 255), (x_box, y_box, largura_box, altura_box), 2)
        janela.draw_text(texto_tempo, x_box + 15, y_box + 5, size=30, color=(255, 255, 255))

        janela.update()
        
    return PLAY, MENU, RANKING, 0