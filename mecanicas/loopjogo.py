<<<<<<< HEAD
import pygame 
import time
from PPlay.keyboard import *
from PPlay.collision import *
from PPlay.mouse import *
from PPlay.sprite import *
from PPlay.window import *
from PPlay.gameobject import *
from PPlay.gameimage import *
=======
>>>>>>> 3a6f222b9c31c067716533b23f937674e65a3202
from mecanicas.personagem import Jogador
from mecanicas.lava import lava
from mecanicas.plataforma import *

def loopjogo(janela, mouse, gm1, teclado, PLAY, MENU, RANKING):
<<<<<<< HEAD
    # Inicia contagem de tempo
    inicio_tempo = time.time()
    tempo_final = 0

    camera = Camera(janela)
    camera.scroll_limit_tela = janela.height * 0.33 
=======
>>>>>>> 3a6f222b9c31c067716533b23f937674e65a3202
    
    gerenciador_plat = Plataforma(janela)
    
    jogador = Jogador(janela, gerenciador_plat.lista[0])

    obstaculo = lava(janela)
    
    contador_frames = 0
    tempo_acumulado = 0
    fps_atual = 0

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

<<<<<<< HEAD
        # Lógica de Game Over
        pe_jogador_na_tela_y = (jogador.y - camera.y) + jogador.height
=======
        # Lógica de Game Over (Usa camera.y atualizado)
        pe_jogador_na_tela_y = jogador.y + jogador.height
>>>>>>> 3a6f222b9c31c067716533b23f937674e65a3202
        
        if pe_jogador_na_tela_y > obstaculo.y:
            PLAY = False
            MENU = True
            RANKING = False
            # Calcula tempo final
            tempo_final = time.time() - inicio_tempo
            return PLAY, MENU, RANKING, tempo_final
        
        obstaculo.lava_jogador(jogador)
<<<<<<< HEAD
        
        # --- DESENHO ---
        gm1.draw() 

=======

        gm1.draw() 


        dt = janela.delta_time()
        
        # --- Lógica do Contador de FPS ---
        tempo_acumulado += dt
        contador_frames += 1
        
        # A cada 1 segundo, atualizamos o valor do FPS
        if tempo_acumulado >= 1.0:
            fps_atual = contador_frames
            contador_frames = 0
            tempo_acumulado = 0

        #print (fps_atual)

        # Desenho
>>>>>>> 3a6f222b9c31c067716533b23f937674e65a3202
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