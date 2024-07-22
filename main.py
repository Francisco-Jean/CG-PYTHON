import Imagem
import Poligono
import pygame
import Textura
import concurrent.futures

def main():
    dim = [640, 360]
    img = Imagem.Imagem(dim[0], dim[1])
    textura = Textura.Textura("trafico.jpeg")
    pol = Poligono.Poligono()
    pol.insere_ponto(0, 0, (255,255, 255), 0, 1)
    pol.insere_ponto(50, 0, (127,127,127), 1, 1)
    pol.insere_ponto(50, 50, (0,0,0), 1, 0)
    pol.insere_ponto(0, 50, (255,255,255), 0, 0)

    janela = [0, 0, dim[0], dim[1]]
    viewport = [0, 0, dim[0], dim[1]]
    pol.mapeiaJanela(janela, viewport)
    pol.cisalhamento(10, 0.5)

    tela = pygame.display.set_mode((img.largura, img.altura))
    pygame.init()
    pygame.display.set_caption("Tela de exibição")
    clock = pygame.time.Clock()
    running = True
    deslocamento = 30
    pixel_size = 1

    # Crie uma única instância de pygame.Rect para reutilização
    rect = pygame.Rect(0, 0, pixel_size, pixel_size)

    while running:
        clock.tick(120)
        img.scanline(pol.poligono, -1, textura)
        
        # Atualize a tela usando blitting
        tela.fill((0, 0, 0))
        for row in range(img.altura):
            for col in range(img.largura):
                rect.topleft = (col, row)
                tela.fill(img.img[row][col], rect)

        # Atualize a tela
        pygame.display.flip()
        img.limpa_imagem()

        # Lidar com eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pol.transforma(pol.translacao(0, -deslocamento))
                elif event.key == pygame.K_DOWN:
                    pol.transforma(pol.translacao(0, deslocamento))
                elif event.key == pygame.K_LEFT:
                    pol.transforma(pol.translacao(-deslocamento, 0))
                elif event.key == pygame.K_RIGHT:
                    pol.transforma(pol.translacao(deslocamento, 0))

    pygame.quit()

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(main)

