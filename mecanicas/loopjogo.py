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

def loopjogo(janela, gm1, lav, direita, esquerda, parado, teclado, PLAY, MENU, RANKING, pulo, morte):

    morreu = pygame.mixer.Sound(morte)

    # Inicia contagem de tempo
    inicio_tempo = time.time()
    tempo_final = 0

    # Inicialização das Plataformas, Jogador e Obstáculo
    gerenciador_plat = Plataforma(janela)
    jogador = Jogador(janela, direita, esquerda, parado, pulo, gerenciador_plat.lista[0])
    obstaculo = lava(janela, lav)

    while PLAY:

        if teclado.key_pressed("ESC"):
            pygame.mixer.music.fadeout(2000)
            PLAY = False
            MENU = True
            RANKING = False
            # Retorna 0 no tempo pois saiu pelo ESC
            return PLAY, MENU, RANKING, 0
        
        # Lógica das Plataformas
        gerenciador_plat.criacao_plataformas()
        gerenciador_plat.remocao_plataformas(janela)

        # Lógica de Game Over
        # Usamos a posição Y do jogador + altura para ver se encostou na lava
        pe_jogador_na_tela_y = jogador.y + jogador.height
        
        if pe_jogador_na_tela_y > obstaculo.y:
            pygame.mixer.music.fadeout(2000)
            morreu.play()
            PLAY = False
            MENU = True
            RANKING = False
            # Calcula tempo final
            tempo_final = time.time() - inicio_tempo
            return PLAY, MENU, RANKING, tempo_final
        
        # Atualiza a lava e o Jogador
        obstaculo.lava_jogador(jogador)
        
        # Desenha o Fundo
        gm1.draw() 

        # Desenho dos objetos
        # Passamos o jogador para o gerenciador desenhar as plataformas (scrolling)
        gerenciador_plat.desenhar_plataformas(jogador)
        jogador.desenha(gerenciador_plat.lista)
        obstaculo.desenhar()

        # --- HUD (CRONÔMETRO) ---
        tempo_atual = time.time() - inicio_tempo
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