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

def handle_input(pol, deslocamento):
    teclas_pressionadas = pygame.key.get_pressed()
    dx, dy = 0, 0
    transformar = False

    if teclas_pressionadas[pygame.K_LEFT]:
        dx -= deslocamento
    if teclas_pressionadas[pygame.K_RIGHT]:
        dx += deslocamento
    if teclas_pressionadas[pygame.K_DOWN]:
        dy += deslocamento
    if teclas_pressionadas[pygame.K_UP]:
        dy -= deslocamento

    if dx != 0 or dy != 0:
        pol.transforma(pol.translacao(dx, dy))
        transformar = True

    if teclas_pressionadas[pygame.K_a] or teclas_pressionadas[pygame.K_d] or teclas_pressionadas[pygame.K_s] or teclas_pressionadas[pygame.K_w]:
        centro_x, centro_y = pol.get_centro()
        pol.transforma(pol.translacao(-centro_x, -centro_y))

        if teclas_pressionadas[pygame.K_a]:
            pol.transforma(pol.rotacao(-deslocamento))
        if teclas_pressionadas[pygame.K_d]:
            pol.transforma(pol.rotacao(deslocamento))
        if teclas_pressionadas[pygame.K_s]:
            pol.transforma(pol.escala(0.7, 0.7))
        if teclas_pressionadas[pygame.K_w]:
            pol.transforma(pol.escala(1.3, 1.3))

        pol.transforma(pol.translacao(centro_x, centro_y))
        transformar = True

    return transformar

def is_visible(bbox, viewport):
    # Check if the bounding box is within the viewport
    return not (bbox[2] < viewport[0] or bbox[0] > viewport[2] or bbox[3] < viewport[1] or bbox[1] > viewport[3])

def main():
    pygame.init()
    dim = [640, 360]
    img = Imagem.Imagem(dim[0], dim[1])
    textura = Textura.Textura("trafico.jpeg")
    pol = Poligono.Poligono()
    pol.insere_ponto(0, 0, (255, 255, 255), 0, 1)
    pol.insere_ponto(50, 0, (127, 127, 127), 1, 1)
    pol.insere_ponto(50, 50, (0, 0, 0), 1, 0)
    pol.insere_ponto(0, 50, (255, 255, 255), 0, 0)

    janela = [0, 0, dim[0], dim[1]]
    viewport = [0, 0, dim[0], dim[1]]
    pol.mapeiaJanela(janela, viewport)

    pygame.display.set_mode((dim[0], dim[1]), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Tela de exibição")
    clock = pygame.time.Clock()
    running = True
    deslocamento = 30

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

    while running:
        clock.tick(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if handle_input(pol, deslocamento):
            img.limpa_imagem()
            glClear(GL_COLOR_BUFFER_BIT)
            bbox = pol.get_bounding_box()
            if is_visible(bbox, viewport):
                glBindVertexArray(VAO)
                glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
                glBindVertexArray(0)
                pygame.display.flip()
                pygame.time.wait(10)
                img.scanline(pol.poligono, -1, textura)
                glBindTexture(GL_TEXTURE_2D, texture_id)
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.largura, img.altura, 0, GL_RGB, GL_UNSIGNED_BYTE, img.img)

    pygame.quit()

if __name__ == "__main__":
    main()