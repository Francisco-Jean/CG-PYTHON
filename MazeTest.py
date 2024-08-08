import pygame
import Imagem
import Poligono
import Textura

def mazeTest():
    pygame.init()
    dim = [720, 512]
    img = Imagem.Imagem(dim[0], dim[1])

    # Criando um Espaço para o labirinto
    maze = Poligono.Poligono()
    maze.insere_ponto(0, 0, (255, 255, 255), 0, 0)
    maze.insere_ponto(dim[0], 0, (255, 255, 255), 1, 0)
    maze.insere_ponto(dim[0], dim[1], (255, 255, 255), 1, 1)
    maze.insere_ponto(0, dim[1], (255, 255, 255), 0, 1)

    rato0 = Textura.Textura("rato1.png")
    rato1 = Textura.Textura("rato2.png")
    rato2 = Textura.Textura("rato3.png")
    rato3 = Textura.Textura("rato4.png")
    modo = 0
    cresce = True
    rato = Poligono.Poligono()
    rato.insere_ponto(5, 260, (255, 255, 255), 0, 1)
    rato.insere_ponto(35, 260, (127, 127, 127), 1, 1)
    rato.insere_ponto(35, 305, (0, 0, 0), 1, 0)
    rato.insere_ponto(5, 305, (255, 255, 255), 0, 0)

    labirinto = Textura.Textura("Nivel 1.png")

    janela = [0, 0, dim[0], dim[1]]
    viewport = [0, 0, dim[0], dim[1]]
    # maze.mapeiaJanela(janela, viewport)
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
    img.scanline(maze.poligono, -1, labirinto)

    while running:
        clock.tick(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if transformar:
            img.limpa_imagem()

            # Clipping
            clipped_poligono = rato.clipping_cohen_sutherland(0, 0, dim[0], dim[1])
            if clipped_poligono:
                if modo == 0:
                    img.scanline(clipped_poligono, -1, rato0)
                elif modo == 1:
                    img.scanline(rato.poligono, -1, rato1)
                elif modo == 2:
                    img.scanline(rato.poligono, -1, rato2)
                elif modo == 3:
                    img.scanline(rato.poligono, -1, rato3)

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
        if teclas_pressionadas[pygame.K_UP]:
            dy -= deslocamento
            if ang != 90:
                centro_x, centro_y = rato.get_centro()
                rato.transforma(rato.translacao(-centro_x, -centro_y))
                if ang == 0:
                    rato.transforma(rato.rotacao(-90))
                elif ang == 270:
                    rato.transforma(rato.rotacao(180))
                elif ang == 180:
                    rato.transforma(rato.rotacao(90))
                rato.transforma(rato.translacao(centro_x, centro_y))
                ang = 90
        elif teclas_pressionadas[pygame.K_DOWN]:
            dy += deslocamento
            if ang != 270:
                centro_x, centro_y = rato.get_centro()
                rato.transforma(rato.translacao(-centro_x, -centro_y))
                if ang == 0:
                    rato.transforma(rato.rotacao(90))
                elif ang == 90:
                    rato.transforma(rato.rotacao(180))
                elif ang == 180:
                    rato.transforma(rato.rotacao(-90))
                rato.transforma(rato.translacao(centro_x, centro_y))
                ang = 270
        elif teclas_pressionadas[pygame.K_LEFT]:
            dx -= deslocamento
            if ang != 180:
                centro_x, centro_y = rato.get_centro()
                rato.transforma(rato.translacao(-centro_x, -centro_y))
                if ang == 0:
                    rato.transforma(rato.rotacao(-180))
                elif ang == 90:
                    rato.transforma(rato.rotacao(-90))
                elif ang == 270:
                    rato.transforma(rato.rotacao(90))
                rato.transforma(rato.translacao(centro_x, centro_y))
                ang = 180
        elif teclas_pressionadas[pygame.K_RIGHT]:
            dx += deslocamento
            if ang != 0:
                centro_x, centro_y = rato.get_centro()
                rato.transforma(rato.translacao(-centro_x, -centro_y))
                if ang == 90:
                    rato.transforma(rato.rotacao(90))
                elif ang == 180:
                    rato.transforma(rato.rotacao(180))
                elif ang == 270:
                    rato.transforma(rato.rotacao(-90))
                rato.transforma(rato.translacao(centro_x, centro_y))
                ang = 0

        if dx != 0 or dy != 0:
            rato.transforma(rato.translacao(dx, dy))
            transformar = True

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    mazeTest()
