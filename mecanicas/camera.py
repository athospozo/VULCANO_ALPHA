# Em: biblioteca/camera.py

class Camera:
    def __init__(self, janela):
        self.janela = janela
        self.y = 0 
        self.scroll_limit_tela = janela.height * 0.6
        self.contar = 0

    def atualizar(self, jogador):
        """
        Lógica HÍBRIDA INSTANTÂNEA (A prova de explosão):
        NÃO usa delta_time(), por isso não pode "explodir".
        """
        if jogador.y < self.scroll_limit_tela:
            # Se o jogador está "alto", a câmera
            # INSTANTANEAMENTE vai para a posição correta.
            return jogador.y/30
            
        else:
            # Se o jogador está na "base", a câmera
            # INSTANTANEAMENTE trava no topo.
            return 0