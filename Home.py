import pygame
import numpy as np
import Imagem
import Poligono
import Textura
from MazeTest import mazeTest

def handleClick():
    print("Círculo clicado!")

def is_inside_circle(x, y, radius, pos):
    # Calcular a distância euclidiana entre o ponto do clique e o centro do círculo
    distance = np.linalg.norm(np.array((x, y)) - np.array(pos))
    inside = distance <= radius
    # Adicionar instruções de depuração
    print(f"Mouse Pos: {pos}, Circle Center: ({x}, {y}), Radius: {radius}, Distance: {distance}, Inside: {inside}")
    return inside

def main():
    pygame.init()
    dim = [720, 512]
    img = Imagem.Imagem(dim[0], dim[1])

    # Criando um Círculo
    circle = Poligono.Poligono()
    circle.circunferencia(img, 360, 132, 60, (240, 209, 104))

    # Criando um Triângulo
    tri = Poligono.Poligono()
    tri.insere_ponto(330, 167, (255, 255, 255), 0, 0)
    tri.insere_ponto(400, 132, (255, 255, 255), 0, 0)
    tri.insere_ponto(330, 97, (255, 255, 255), 0, 0)

    # Criando um Espaço para o Título
    titulo = Poligono.Poligono()
    titulo.insere_ponto(68, 362, (255, 255, 255), 0, 0)
    titulo.insere_ponto(652, 362, (255, 255, 255), 1, 0)
    titulo.insere_ponto(652, 252, (255, 255, 255), 1, 1)
    titulo.insere_ponto(68, 252, (255, 255, 255), 0, 1)

    title = Textura.Textura("Title.png")

    janela = [0, 0, dim[0], dim[1]]
    viewport = [0, 0, dim[0], dim[1]]
    tri.mapeiaJanela(janela, viewport)
    titulo.mapeiaJanela(janela, viewport)
    circle.mapeiaJanela(janela, viewport)

    screen = pygame.display.set_mode((dim[0], dim[1]))
    pygame.display.set_caption("Cheese Eater")
    clock = pygame.time.Clock()
    running = True

    # Processar a imagem antes do loop principal
    img.limpa_imagem()
    img.scanline(circle.poligono, (240, 209, 104))
    img.scanline(tri.poligono, (255, 255, 255))
    img.scanline(titulo.poligono, -1, title)
    img.bresenham(68, 130, 652, 130, (255, 255, 255))
    img.bresenham(68, 280, 652, 280, (255, 255, 255))
    img.flood_fill(320, 180, (226, 164, 45), (0, 0, 0))

    # Converte a imagem processada em uma superfície Pygame
    surface = pygame.image.frombuffer(img.img.tobytes(), (img.largura, img.altura), "RGB")

    while running:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(f"Mouse clicked at: {event.pos}")
                if is_inside_circle(360, 380, 60, event.pos):
                    mazeTest()

        # Desenha a imagem na tela
        screen.blit(surface, (0, 0))
        pygame.display.flip()
        
    pygame.quit()

if __name__ == "__main__":
    main()
