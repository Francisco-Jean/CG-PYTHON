import Poligono
import Textura
import Imagem
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np

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
    glBindTexture(GL_TEXTURE_2D, 0)
    return texture_id

def home():
  pygame.init()

  dim = [720, 512]

  pygame.display.set_mode((dim[0], dim[1]), DOUBLEBUF | OPENGL)
  pygame.display.set_caption("Tela de exibição")
  clock = pygame.time.Clock()

  img = Imagem.Imagem(dim[0], dim[1])

  # Criating a Circle
  # circle = Poligono.Poligono()
  # circ = circle.circunferencia(img, 360, 380, 60, (240, 209, 104))

  # Criating a Triangle
  tri = Poligono.Poligono()
  tri.insere_ponto(330, 345, (255, 255, 255), 0, 0)
  tri.insere_ponto(400, 380, (255, 255, 255), 0, 0)
  tri.insere_ponto(330, 415, (255, 255, 255), 0, 0)

  # Criating a Space to Title
  titulo = Poligono.Poligono()
  titulo.insere_ponto(62, 150, (255, 255, 255), 0, 0)
  titulo.insere_ponto(658, 150, (255, 255, 255), 0, 0)
  titulo.insere_ponto(658, 260, (255, 255, 255), 0, 0)
  titulo.insere_ponto(62, 260, (255, 255, 255), 0, 0)

  title = Textura.Textura("Title.png")

  janela = [0, 0, dim[0], dim[1]]
  viewport = [0, 0, dim[0], dim[1]]
  tri.mapeiaJanela(janela, viewport)
  # titulo.mapeiaJanela(janela, viewport)
  # circ.mapeiaJanela(janela, viewport)

  

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

  running = True
  transformar = True
  while running:
    clock.tick(120)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False

    if transformar:
      img.limpa_imagem()
      glClear(GL_COLOR_BUFFER_BIT)
      glBindVertexArray(VAO)
      glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
      glBindVertexArray(0)
      pygame.display.flip()
      pygame.time.wait(10)

      img.flood_fill(320, 180, (226, 164, 45), (0, 0, 0))
      # img.scanline(circ, (240, 209, 104))
      img.scanline(tri.poligono, (255, 255, 255))
      img.scanline(titulo.poligono, -1, title)

      glBindTexture(GL_TEXTURE_2D, texture_id)
      glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.largura, img.altura, 0, GL_RGB, GL_UNSIGNED_BYTE, img.img)
      transformar = False
    
    # Desenhar a textura na tela
    glClear(GL_COLOR_BUFFER_BIT)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex2f(-1.0, -1.0)
    glTexCoord2f(1.0, 0.0)
    glVertex2f(1.0, -1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex2f(1.0, 1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex2f(-1.0, 1.0)
    glEnd()
    pygame.display.flip()

  pygame.quit()

if __name__ == "__main__":
  home()