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
from mecanicas.camera import Camera
from mecanicas.plataforma import *

def loopjogo(janela, mouse, gm1, teclado, PLAY, MENU, RANKING):
    # Inicia contagem de tempo
    inicio_tempo = time.time()
    tempo_final = 0

    camera = Camera(janela)
    camera.scroll_limit_tela = janela.height * 0.33 
    
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
        
        # Plataformas
        gerenciador_plat.criacao_plataformas()
        gerenciador_plat.remocao_plataformas(janela)

        # Lógica de Game Over
        pe_jogador_na_tela_y = (jogador.y - camera.y) + jogador.height
        
        if pe_jogador_na_tela_y > obstaculo.y:
            PLAY = False
            MENU = True
            RANKING = False
            # Calcula tempo final
            tempo_final = time.time() - inicio_tempo
            return PLAY, MENU, RANKING, tempo_final
        
        obstaculo.lava_jogador(jogador)
        
        # --- DESENHO ---
        gm1.draw() 

        gerenciador_plat.desenhar_plataformas(jogador)
        jogador.desenha(gerenciador_plat.lista)
        obstaculo.desenhar()

        # --- HUD (CRONÔMETRO) ---
        tempo_atual = time.time() - inicio_tempo
        texto_tempo = f"{tempo_atual:.1f}s"

        # Fundo do cronômetro (Caixa preta)
        largura_box = 110
        altura_box = 40
        x_box = janela.width - largura_box - 10
        y_box = 10

        # Desenha retângulo preto
        pygame.draw.rect(janela.screen, (0, 0, 0), (x_box, y_box, largura_box, altura_box))
        # Borda branca (opcional)
        pygame.draw.rect(janela.screen, (255, 255, 255), (x_box, y_box, largura_box, altura_box), 2)

        # Texto do tempo
        janela.draw_text(texto_tempo, x_box + 15, y_box + 5, size=30, color=(255, 255, 255))

        janela.update()
        
    return PLAY, MENU, RANKING, 0