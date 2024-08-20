import pygame
import utils.Imagem as Imagem
import utils.Poligono as Poligono
import utils.Textura as Textura
from Home import home

def handleClick():
    print("Quadrado clicado!")

def is_inside_square(xmin, xmax, ymin, ymax, pos):
    inside = xmin <= pos[0] <= xmax and ymin <= pos[1] <= ymax
    return inside

def congrats():
    pygame.mixer.init()
    pygame.mixer.music.load('assets/win.mp3')
    pygame.mixer.music.play(loops=-1)
    pygame.init()
    dim = [720, 512]
    img = Imagem.Imagem(dim[0], dim[1])

    # Criando um Espaço para o texto de parabéns
    titulo = Poligono.Poligono()
    titulo.insere_ponto(69, 334, (255, 255, 255), 0, 0)
    titulo.insere_ponto(650, 334, (255, 255, 255), 1, 0)
    titulo.insere_ponto(650, 256, (255, 255, 255), 1, 1)
    titulo.insere_ponto(69, 256, (255, 255, 255), 0, 1)

    # Criando um Espaço para o botão de voltar
    back = Poligono.Poligono()
    back.insere_ponto(210, 195, (255, 255, 255), 0, 0)
    back.insere_ponto(510, 195, (255, 255, 255), 1, 0)
    back.insere_ponto(510, 95, (255, 255, 255), 1, 1)
    back.insere_ponto(210, 95, (255, 255, 255), 0, 1)

    # Criando um Espaço para o botão de voltar
    rato = Poligono.Poligono()
    rato.insere_ponto(488, 0, (255, 255, 255), 0, 1)
    rato.insere_ponto(488, 240, (255, 255, 255), 0, 0)
    rato.insere_ponto(dim[0], 240, (255, 255, 255), 1, 0)
    rato.insere_ponto(dim[0], 0, (255, 255, 255), 1, 1)

    background = Poligono.Poligono()
    background.insere_ponto(0, 0, (226, 164, 45), 0, 1)
    background.insere_ponto(0, dim[1], (226, 164, 45), 0, 0)
    background.insere_ponto(dim[0], dim[1], (226, 164, 45), 1, 0)
    background.insere_ponto(dim[0], 0, (226, 164, 45), 1, 1)

    title = Textura.Textura("assets/Congrats-title.png")
    back_img = Textura.Textura("assets/Home-buttom.png")
    rat = Textura.Textura("assets/Rat Mascot 1.png")

    janela = [0, 0, dim[0], dim[1]]
    viewport = [0, 0, dim[0], dim[1]]
    titulo.mapeiaJanela(janela, viewport)
    back.mapeiaJanela(janela, viewport)
    rato.mapeiaJanela(janela, viewport)

    screen = pygame.display.set_mode((dim[0], dim[1]))
    pygame.display.set_caption("Cheese Eater")
    clock = pygame.time.Clock()
    running = True

    # Processar a imagem antes do loop principal
    img.limpa_imagem()
    img.scanline(background.poligono, (226, 164, 45))
    img.scanline(rato.poligono, -1, rat)
    img.scanline(titulo.poligono, -1, title)
    img.scanline(back.poligono, -1, back_img)
    img.bresenham(69, 272, 650, 272, (255, 255, 255))
    img.bresenham(69, 162, 650, 162, (255, 255, 255))
    # img.flood_fill(320, 180, (226, 164, 45), (0, 0, 0))

    # Converte a imagem processada em uma superfície Pygame
    surface = pygame.image.frombuffer(img.img.tobytes(), (img.largura, img.altura), "RGB")

    while running:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if is_inside_square(210, 510, 317, 417, event.pos):
                    home()

        # Desenha a imagem na tela
        screen.blit(surface, (0, 0))
        pygame.display.flip()
        
    pygame.mixer.music.stop()
    pygame.quit()

if __name__ == "__main__":
    congrats()
