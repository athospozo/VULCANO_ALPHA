from PPlay.animation import *
from PPlay.keyboard import *
from PPlay.window import *

class Jogador:

    #definicao de caracteristicas basicas
    def __init__ (self, janela, plataforma1):

        #definicooes basicas:
        self.teclado = Keyboard()
        self.janela = janela
        self.dt = 0

        #primeiro a geracao de personagem:
        self.anim_parado = Animation("ARTES/parado.png", 2)
        self.anim_esquerda = Animation ("ARTES/esquerda.png", 4)
        self.anim_direita = Animation ("ARTES/direita.png", 4)

        #agora definimos as medidas dos sprites:
        self.width = self.janela.width/25
        self.height = self.janela.height/20
        self.anim_direita.height = self.anim_esquerda.height = self.anim_parado.height = self.height
        self.anim_direita.width = self.anim_esquerda.width = self.anim_parado.width = self.width

        #vamos entao colocar os sprites de acordo com os tamanhos definidos:
        try:
            self.anim_parado.image = pygame.transform.scale(self.anim_parado.image, (self.width * 2, self.height))
            self.anim_esquerda.image = pygame.transform.scale(self.anim_esquerda.image, (self.width * 4, self.height))
            self.anim_direita.image = pygame.transform.scale(self.anim_direita.image, (self.width * 4, self.height))
        except Exception as e:
            print(f"Erro ao redimensionar imagens do Personagem: {e}")

        #definindo o tempo das animacoes dos sprites
        self.anim_parado.set_total_duration(1000)
        self.anim_direita.set_total_duration(500)
        self.anim_esquerda.set_total_duration(500)

        #definindo posicoes iniciais:
        self.agora = self.anim_parado
        self.x = plataforma1.x + plataforma1.width / 2 - self.width / 2
        self.y = plataforma1.y - plataforma1.height*2

        #fisica do movimento horizontal:
        self.velocidade_horizontal = self.janela.width/5
        self.no_chao = True

        #fisica do movimento vertical:
        self.velocidade_vertical = 0
        self.gravidade = self.janela.height*7
        self.forca_pulo = self.janela.height*1.5
        self.jumping = False

        #variavel para propósitos externos à classe
        self.subindo = False
        self.qnte_pulos = 0

    #definindo quando ha uma colisao de personagem com outro sprite:
    def colisao (self, possivel_colisao):

        #sobreposição no eixo x:
        if ((self.x <= possivel_colisao.x + possivel_colisao.width) and
            (self.x + self.width >= possivel_colisao.x)):

            #averiguando colisao por cima:
            if ((self.y + self.height >= possivel_colisao.y - 2) and
                (self.y + self.height <= possivel_colisao.y + possivel_colisao.height/2)): 
                return 1
            
            #averiguando colisao por baixo:
            if ((self.y >= possivel_colisao.y + possivel_colisao.height/2) and
                (self.y <= possivel_colisao.y + possivel_colisao.height)): 
                return -1
            
    #definindo como o personagem interage com as plataformas:
    def personagem_plataformas (self, lista_plataformas):

        #comecamos pela premissa que o jogador nao esta em contato com plataformas:
        self.no_chao = False

        #vamos checar todas as plataformas
        for plataforma in lista_plataformas:

            #primeiro vamos garantir que a plataformas esteja em uma margem necessaria para gastar processamento:
            if ((plataforma.y >= -20) and
                (plataforma.y + plataforma.height <= self.janela.height)):
                
                self.aux = self.colisao(plataforma)

                #verificamos se é colisao por cima
                if (self.aux == 1):
                    if self.velocidade_vertical >= 0:
                        self.y = plataforma.y - self.height
                        self.velocidade_vertical = 0
                        self.no_chao = True
                        self.jumping = False
                        #mesma verificacao na classe dads plataformas:
                        if (self.qnte_pulos > 15):
                            self.x += plataforma.vx * self.dt

                #verificamos se é colisao por baixo
                elif (self.aux == -1):
                    self.y = (plataforma.y + plataforma.height) + 10
                    self.no_chao = False
                    self.velocidade_vertical = 4
                    if ((self.jumping) and (self.velocidade_vertical > 0)):
                        self.velocidade_vertical = 0
                    
    #definicao do funcionamento do pulo:
    def pulo (self):
        
        #caso de haver pressionamento das teclas de pulo e o personagem nao estar pulando:
        if (((self.teclado.key_pressed("SPACE")) or (self.teclado.key_pressed("W"))) and (self.no_chao == True)
            and (self.jumping == False)):
            self.jumping = True
            self.no_chao = False
            self.velocidade_vertical = -self.forca_pulo
            self.qnte_pulos += 1

    #movimento horizontal do jogador:
    def mov (self):
        
        self.velocidade_vertical += self.gravidade*self.dt

        #por padrao é parado:
        self.agora = self.anim_parado

        #movimento para a esquerda:
        if (self.teclado.key_pressed("A") or self.teclado.key_pressed("LEFT")):
            self.agora = self.anim_esquerda
            self.x -= self.velocidade_horizontal * self.dt
        
        #movimento para a direita:
        if (self.teclado.key_pressed("D") or self.teclado.key_pressed("RIGHT")):
            self.agora = self.anim_direita
            self.x += self.velocidade_horizontal * self.dt

        #verificando os "limites" horizontais da tela:
            #lado esquerdo:
        if self.x < 0:
            self.x = 0
            #lado direito:
        elif self.x + self.width > self.janela.width:
            self.x = self.janela.width - self.width

        #pulando ou caindo
        if (self.no_chao == False):
            self.y += (self.velocidade_vertical * self.dt)
    
    #colocar o personagem na tela:
    def desenha (self, lista_plataformas):

        #premissa:
        self.subindo = False
        
        #calculo de delta time usado em algumas funcoes
        self.dt = self.janela.delta_time()
        
        #primeiro checamos se o personagem esta na plataforma:
        self.personagem_plataformas (lista_plataformas)

        #agora verificamos se ele pulou:
        self.pulo()
        #momento emm que o jogador está subindo e a câmera também tem que subir
        if (self.velocidade_vertical < 0):
            self.subindo = True

        #agora seu movimento horizontal:
        self.mov()

        self.agora.set_position (self.x, self.y)
        self.agora.update()

        self.agora.draw()