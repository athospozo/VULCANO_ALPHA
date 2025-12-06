from PPlay.window import *
from PPlay.gameimage import *
import os

ARQUIVO_RANKING = "ranking.txt"

def salvar_pontuacao(nome, tempo):
    try:
        with open(ARQUIVO_RANKING, "a") as arquivo:
            arquivo.write(f"{nome},{tempo:.2f}\n")
    except Exception as e:
        print(f"Erro ao salvar ranking: {e}")

def carregar_top_5():
    pontuacoes = []
    
    if not os.path.exists(ARQUIVO_RANKING):
        return []

    try:
        with open(ARQUIVO_RANKING, "r") as arquivo:
            linhas = arquivo.readlines()
            
            for linha in linhas:
                dados = linha.strip().split(",")
                if len(dados) == 2:
                    nome = dados[0]
                    try:
                        tempo = float(dados[1])
                        pontuacoes.append((nome, tempo))
                    except ValueError:
                        continue
        
        # Ordena: Maior tempo primeiro (sobrevivência)
        pontuacoes.sort(key=lambda x: x[1], reverse=True)
        
        return pontuacoes[:5]
        
    except Exception as e:
        print(f"Erro ao ler ranking: {e}")
        return []

def ranking(janela, teclado, ranking_img, PLAY, MENU, RANKING):
    
    top_5 = carregar_top_5()

    while RANKING:
        if teclado.key_pressed("ESC"):
            PLAY = False
            MENU = True
            RANKING = False
            return PLAY, MENU, RANKING

        janela.set_background_color([0, 0, 0])
        
        # Título
        janela.draw_text("RANKING (TOP 5)", janela.width / 2 - 180, 50, size=48, color=(255, 215, 0))

        # Lista de nomes
        y_pos = 150
        posicao = 1
        
        if not top_5:
            janela.draw_text("Nenhum recorde ainda.", janela.width / 2 - 150, y_pos, size=32, color=(255, 255, 255))
        else:
            for nome, tempo in top_5:
                texto = f"{posicao}. {nome} - {tempo:.2f}s"
                janela.draw_text(texto, janela.width / 2 - 150, y_pos, size=30, color=(255, 255, 255))
                y_pos += 60
                posicao += 1

        janela.draw_text("Pressione [ESC] para voltar", janela.width / 2 - 180, janela.height - 50, size=24, color=(200, 200, 200))

        janela.update()

    return PLAY, MENU, RANKING