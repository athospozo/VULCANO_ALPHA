import pygame
from PPlay.window import *

def tela_game_over(janela, tempo):
    """
    Exibe tela de Game Over e captura o nome digitado.
    """
    input_nome = ""
    digitando = True
    
    pygame.event.clear()
    pygame.time.delay(300)

    clock = pygame.time.Clock()
    contador_piscar = 0

    while digitando:
        clock.tick(60) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    if len(input_nome) > 0: 
                        digitando = False
                
                elif event.key == pygame.K_BACKSPACE:
                    input_nome = input_nome[:-1]
                
                else:
                    if len(input_nome) < 12 and event.unicode.isprintable():
                        input_nome += event.unicode

        janela.set_background_color([0, 0, 0])

        janela.draw_text("FIM DE JOGO!", janela.width/2 - 120, 150, size=40, color=(255, 0, 0))
        janela.draw_text(f"Sobreviveu: {tempo:.2f}s", janela.width/2 - 140, 220, size=30, color=(255, 255, 255))
        janela.draw_text("Digite seu nome e ENTER:", janela.width/2 - 180, 350, size=24, color=(200, 200, 200))
        
        # Cursor piscando
        contador_piscar += 1
        cursor = ""
        if (contador_piscar // 30) % 2 == 0:
            cursor = "_"

        texto_final = input_nome + cursor
        
        largura_texto = len(texto_final) * 15
        janela.draw_text(texto_final, janela.width/2 - (largura_texto/2), 400, size=40, color=(255, 255, 0))

        # Usando update nativo do Pygame para não travar o teclado
        pygame.display.update()
    
    return input_nome