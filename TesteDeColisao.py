import pygame
import sys

# Definição do labirinto (1 = parede, 0 = caminho)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

def draw_maze(screen, maze):
    block_size = 40  # Tamanho de cada bloco do labirinto
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            color = (0, 0, 0) if cell == 1 else (255, 255, 255)
            pygame.draw.rect(screen, color, pygame.Rect(x * block_size, y * block_size, block_size, block_size))

def main():
    pygame.init()
    
    # Configurações da janela
    screen = pygame.display.set_mode((400, 360))
    pygame.display.set_caption("Labirinto com Controle de Colisão")
    
    # Carregar a imagem do jogador
    player_image = pygame.image.load("ratin.png")
    player_rect = player_image.get_rect()
    player_rect.topleft = (40, 40)  # Posição inicial do jogador
    
    # Loop principal
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Movimentação do jogador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_rect.x -= 1
        if keys[pygame.K_RIGHT]:
            player_rect.x += 1
        if keys[pygame.K_UP]:
            player_rect.y -= 1
        if keys[pygame.K_DOWN]:
            player_rect.y += 1
        
        # Verificar colisão com as paredes
        block_size = 40
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                if cell == 1:
                    wall_rect = pygame.Rect(x * block_size, y * block_size, block_size, block_size)
                    if player_rect.colliderect(wall_rect):
                        # Reverter movimento se houver colisão
                        if keys[pygame.K_LEFT]:
                            player_rect.x += 1
                        if keys[pygame.K_RIGHT]:
                            player_rect.x -= 1
                        if keys[pygame.K_UP]:
                            player_rect.y += 1
                        if keys[pygame.K_DOWN]:
                            player_rect.y -= 1
        
        # Preencher o fundo
        screen.fill((0, 0, 255))
        
        # Desenhar o labirinto
        draw_maze(screen, maze)
        
        # Desenhar o jogador
        screen.blit(player_image, player_rect.topleft)
        
        # Atualizar a tela
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()