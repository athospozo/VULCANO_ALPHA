from mecanicas.personagem import Jogador
from mecanicas.lava import lava
from mecanicas.plataforma import *

def loopjogo(janela, mouse, gm1, teclado, PLAY, MENU, RANKING):
    
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
            return PLAY, MENU, RANKING
        
        #plataformas
        gerenciador_plat.criacao_plataformas()
        gerenciador_plat.remocao_plataformas(janela)

        # Lógica de Game Over (Usa camera.y atualizado)
        pe_jogador_na_tela_y = jogador.y + jogador.height
        
        if pe_jogador_na_tela_y > obstaculo.y:
            PLAY = False
            MENU = True
            RANKING = False
            return PLAY, MENU, RANKING
        
        obstaculo.lava_jogador(jogador)

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
        gerenciador_plat.desenhar_plataformas(jogador)

        jogador.desenha(gerenciador_plat.lista)

        obstaculo.desenhar()

        janela.update()
        
    return PLAY, MENU, RANKING