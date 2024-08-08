import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import Imagem
import Poligono
import Textura

# Vertex Shader
vertex_shader_source = """
#version 330
in vec2 position;
in vec2 texCoords;
out vec2 TexCoords;
void main()
{
    gl_Position = vec4(position, 0.0, 1.0);
    TexCoords = texCoords;
}
"""

# Fragment Shader
fragment_shader_source = """
#version 330
in vec2 TexCoords;
out vec4 color;
uniform sampler2D pixel_texture;
void main()
{
    color = texture(pixel_texture, TexCoords);
}
"""

def create_shader_program(vertex_src, fragment_src):
    vertex_shader = compileShader(vertex_src, GL_VERTEX_SHADER)
    fragment_shader = compileShader(fragment_src, GL_FRAGMENT_SHADER)
    shader_program = compileProgram(vertex_shader, fragment_shader)
    return shader_program

def setup_buffers(vertices, indices):
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)

    glBindVertexArray(VAO)

    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    position = glGetAttribLocation(shader_program, 'position')
    glVertexAttribPointer(position, 2, GL_FLOAT, GL_FALSE, 4 * vertices.itemsize, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)

    texCoords = glGetAttribLocation(shader_program, 'texCoords')
    glVertexAttribPointer(texCoords, 2, GL_FLOAT, GL_FALSE, 4 * vertices.itemsize, ctypes.c_void_p(2 * vertices.itemsize))
    glEnableVertexAttribArray(texCoords)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    return VAO

def create_texture():
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return texture_id

def main():
    pygame.init()
    dim = [720, 512]
    img = Imagem.Imagem(dim[0], dim[1])

    # Criando um Espaço para o labirinto
    maze = Poligono.Poligono()
    maze.insere_ponto(0, 0, (255, 255, 255), 0, 0)
    maze.insere_ponto(dim[0]*3, 0, (255, 255, 255), 1, 0)
    maze.insere_ponto(dim[0]*3, dim[1]*3, (255, 255, 255), 1, 1)
    maze.insere_ponto(0, dim[1]*3, (255, 255, 255), 0, 1)

    labirinto = Textura.Textura("Nivel 1.png")

    janela = [0, 0, dim[0], dim[1]]
    viewport = [0, 0, dim[0], dim[1]]
    maze.mapeiaJanela(janela, viewport)

    pygame.display.set_mode((dim[0], dim[1]), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Cheese Eater")
    clock = pygame.time.Clock()
    running = True

    global shader_program
    shader_program = create_shader_program(vertex_shader_source, fragment_shader_source)
    glUseProgram(shader_program)

    vertices = np.array([
        -1.0,  1.0,  0.0, 0.0,
        -1.0, -1.0,  0.0, 1.0,
         1.0, -1.0,  1.0, 1.0,
         1.0,  1.0,  1.0, 0.0,
    ], dtype=np.float32)

    indices = np.array([
        0, 1, 2,
        2, 3, 0
    ], dtype=np.uint32)

    VAO = setup_buffers(vertices, indices)
    texture_id = create_texture()

    # Processar a imagem antes do loop principal
    img.limpa_imagem()
    img.scanline(maze.poligono, -1, labirinto)
    img.flood_fill(320, 180, (226, 164, 45), (0, 0, 0))

    # Carregar a textura resultante uma única vez
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.largura, img.altura, 0, GL_RGB, GL_UNSIGNED_BYTE, img.img)

    while running:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        glClear(GL_COLOR_BUFFER_BIT)
        glBindVertexArray(VAO)
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
        pygame.display.flip()
        
    pygame.quit()

if __name__ == "__main__":
    main()
