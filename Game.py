import pygame
import utils.Imagem as Imagem
import utils.Poligono as Poligono
import utils.Textura as Textura
from random import randint

def mazeTest():

    pygame.mixer.init()
    pygame.mixer.music.load('assets/jogo.mp3')
    pygame.mixer.music.play(loops=-1)

    pygame.init()
    dim = [1020, 512]
    img = Imagem.Imagem(dim[0], dim[1])
    fundo = Imagem.Imagem(dim[0], dim[1])

    # Criando um Espaço para o labirinto
    maze = Poligono.Poligono()
    maze.insere_ponto(0, dim[1], (255, 255, 255), 0, 0)
    maze.insere_ponto(dim[0], dim[1], (255, 255, 255), 1, 0)
    maze.insere_ponto(dim[0], 0, (255, 255, 255), 1, 1)
    maze.insere_ponto(0, 0, (255, 255, 255), 0, 1)

    mini_maze = Poligono.Poligono()
    mini_maze.insere_ponto(0, dim[1], (255, 255, 255), 0, 0)
    mini_maze.insere_ponto(dim[0], dim[1], (255, 255, 255), 1, 0)
    mini_maze.insere_ponto(dim[0], 0, (255, 255, 255), 1, 1)
    mini_maze.insere_ponto(0, 0, (255, 255, 255), 0, 1)

    rato0 = Textura.Textura("assets/rato 1.png")
    rato1 = Textura.Textura("assets/rato 2.png")
    rato2 = Textura.Textura("assets/rato 3.png")
    rato3 = Textura.Textura("assets/rato 4.png")
    modo = 0
    cresce = True
    rato = Poligono.Poligono()
    rato.insere_ponto(5, 260, (255, 255, 255), 0, 1)
    rato.insere_ponto(35, 260, (127, 127, 127), 1, 1)
    rato.insere_ponto(35, 305, (0, 0, 0), 1, 0)
    rato.insere_ponto(5, 305, (255, 255, 255), 0, 0)
    centro_x, centro_y = rato.get_centro()
    rato.transforma(rato.translacao(-centro_x, -centro_y))
    rato.transforma(rato.rotacao(-90))
    rato.transforma(rato.translacao(centro_x, centro_y))
    rato.transforma(rato.translacao(-centro_x, -centro_y))
    rato.transforma(rato.escala(0.7, 0.7))
    rato.transforma(rato.translacao(centro_x, centro_y))

    lab_choose = randint(1, 3)
    if lab_choose == 1:
        labirinto = Textura.Textura("assets/Nivel 1.png")
    elif lab_choose == 2:
        labirinto = Textura.Textura("assets/Nivel 2.png")
    elif lab_choose == 3:
        labirinto = Textura.Textura("assets/Nivel 3.png")

    janela = [0, 0, dim[0], dim[1]]
    x_min, y_min = [100, 100]
    viewport = [x_min, y_min, dim[0] - x_min, dim[1] - y_min]
    mine_passo = 0.2
    mini_viewport = [0, 0, dim[0] * mine_passo, dim[1] * mine_passo]
    maze.mapeiaJanela(janela, viewport)
    mini_maze.mapeiaJanela(janela, mini_viewport)
    rato.mapeiaJanela(janela, viewport)

    screen = pygame.display.set_mode((dim[0], dim[1]))
    pygame.display.set_caption("Cheese Eater")
    clock = pygame.time.Clock()
    running = True

    ang = 90
    modo = 0
    cresce = True
    deslocamento = 5

    transformar = True
    fundo.scanline(maze.poligono, -1, labirinto)
    fundo.scanline(mini_maze.poligono, (255, 255, 255))
    centro_x, centro_y = rato.get_centro()
    rato.transforma(rato.translacao(-centro_x, -centro_y))
    rato.transforma(rato.rotacao(-90))
    rato.transforma(rato.translacao(centro_x, centro_y))

    ponto_personagem = Poligono.Poligono()
    ponto_personagem.insere_ponto(5, 260, (0, 0, 0), 0, 1)
    ponto_personagem.insere_ponto(35, 260, (0, 0, 0), 1, 1)
    ponto_personagem.insere_ponto(35, 305, (0, 0, 0), 1, 0)
    ponto_personagem.insere_ponto(5, 305, (0, 0, 0), 0, 0)

    ponto_personagem.mapeiaJanela(janela, mini_viewport)

    while running:
        
        clock.tick(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if transformar:
            img.img = fundo.img.copy()

            if modo == 0:
                img.scanline(rato.poligono, -1, rato0)
            elif modo == 1:
                img.scanline(rato.poligono, -1, rato1)
                
            elif modo == 2:
                img.scanline(rato.poligono, -1, rato2)
            elif modo == 3:
                img.scanline(rato.poligono, -1, rato3)
            
            img.scanline(ponto_personagem.poligono, (0, 0, 255))

            # Alterna entre os modos de transformação
            if cresce:
                modo += 1
                if modo == 4:
                    cresce = False
                    modo -= 1
            else:
                modo -= 1
                if modo == -1:
                    cresce = True
                    modo += 1

            # Atualiza a imagem do rato
            rato_surface = pygame.image.frombuffer(img.img.tobytes(), (img.largura, img.altura), 'RGB')
            screen.blit(rato_surface, (0, 0))

            transformar = False

        teclas_pressionadas = pygame.key.get_pressed()

        dx, dy = 0, 0
        ang_rot = 0
        if teclas_pressionadas[pygame.K_UP]:
            dy -= deslocamento
            if ang != 90:
                centro_x, centro_y = rato.get_centro()
                rato.transforma(rato.translacao(-centro_x, -centro_y))
                if ang == 0:
                    rato.transforma(rato.rotacao(-90))
                    ang_rot = -90
                elif ang == 270:
                    rato.transforma(rato.rotacao(180))
                    ang_rot = 180
                elif ang == 180:
                    rato.transforma(rato.rotacao(90))
                    ang_rot = 90
                ang = 90
        elif teclas_pressionadas[pygame.K_DOWN]:
            dy += deslocamento
            if ang != 270:
                centro_x, centro_y = rato.get_centro()
                rato.transforma(rato.translacao(-centro_x, -centro_y))
                if ang == 0:
                    rato.transforma(rato.rotacao(90))
                    ang_rot = 90
                elif ang == 90:
                    rato.transforma(rato.rotacao(180))
                    ang_rot = 180
                elif ang == 180:
                    rato.transforma(rato.rotacao(-90))
                    ang_rot = -90
                ang = 270
        elif teclas_pressionadas[pygame.K_LEFT]:
            dx -= deslocamento
            if ang != 180:
                centro_x, centro_y = rato.get_centro()
                rato.transforma(rato.translacao(-centro_x, -centro_y))
                if ang == 0:
                    rato.transforma(rato.rotacao(-180))
                    ang_rot = -180
                elif ang == 90:
                    rato.transforma(rato.rotacao(-90))
                    ang_rot = -90
                elif ang == 270:
                    rato.transforma(rato.rotacao(90))
                    ang_rot = 90
                ang = 180
        elif teclas_pressionadas[pygame.K_RIGHT]:
            dx += deslocamento
            if ang != 0:
                centro_x, centro_y = rato.get_centro()
                rato.transforma(rato.translacao(-centro_x, -centro_y))
                if ang == 90:
                    rato.transforma(rato.rotacao(90))
                    ang_rot = 90
                elif ang == 180:
                    rato.transforma(rato.rotacao(180))
                    ang_rot = 180
                elif ang == 270:
                    rato.transforma(rato.rotacao(-90))
                    ang_rot = -90
                ang = 0
        # if rato.check_collision(fundo):
        #     rato.transforma(rato.rotacao(-ang_rot))
        #     transformar = False
        if ang_rot != 0:
            rato.transforma(rato.translacao(centro_x, centro_y))

        if dx != 0 or dy != 0:
            rato.transforma(rato.translacao(dx, dy))
            ponto_personagem.transforma(ponto_personagem.translacao(dx * mine_passo , dy * mine_passo))
            transformar = True

            try:
                if rato.check_collision(fundo):
                    rato.transforma(rato.translacao(-dx, -dy))
                    ponto_personagem.transforma(ponto_personagem.translacao(-dx * mine_passo, -dy * mine_passo))
                    transformar = False
            except:
                rato.transforma(rato.translacao(-dx, -dy))
                ponto_personagem.transforma(ponto_personagem.translacao(-dx * mine_passo, -dy * mine_passo))
                transformar = False

        pygame.display.flip()

    pygame.mixer.music.stop()
    pygame.quit()

if __name__ == "__main__":
    mazeTest()