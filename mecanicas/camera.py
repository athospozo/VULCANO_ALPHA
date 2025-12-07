class Camera:
    def __init__(self, janela):
        self.janela = janela
        self.y = 0
        self.height = janela.height
        self.scroll_limit_tela = janela.height * 0.33
        self.contar = 0

    def atualizar(self, jogador):
        # Lógica HÍBRIDA INSTANTÂNEA: Não usa delta_time para evitar "explosão" de movimento
        # Se você quiser implementar o movimento de câmera "real" no futuro, use isto.
        # Por enquanto, a classe Plataforma.py já faz o "scroll" manualmente movendo os objetos.
        pass