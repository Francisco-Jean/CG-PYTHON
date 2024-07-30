import numpy as np
from numpy import sign
import matplotlib.pyplot as plt
from math import floor
import concurrent.futures

class Imagem:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.img = np.zeros((altura, largura, 3), dtype=np.uint8)  # Corrigido para 3 canais (RGB)
    
    def set_pixel(self, x, y, intensidade):
        if len(intensidade) > 3:
            intensidade = intensidade[:3]
        if 0 <= x < self.largura and 0 <= y < self.altura:
            self.img[y, x] = np.clip(intensidade, 0, 255)  # Garante que a intensidade esteja no intervalo [0, 255]
    
    def imshow(self):
        plt.imshow(self.img)
        plt.axis('off')  # Remove eixos para visualização limpa
        plt.show()

    def limpa_imagem(self):
        self.img.fill(0)  # Método mais eficiente para limpar a imagem
    
    def dda(self, xi, yi, xf, yf, intensidade):
        dx = xf - xi
        dy = yf - yi

        passos = max(abs(dx), abs(dy))

        passo_x = dx / passos
        passo_y = dy / passos

        x, y = xi, yi

        for _ in range(passos + 1):
            self.set_pixel(round(x), round(y), intensidade)
            x += passo_x
            y += passo_y

    def dda_aa(self, xi, yi, xf, yf, intensidade):
        dx = xf - xi
        dy = yf - yi

        passos = max(abs(dx), abs(dy))
        passo_x = dx / passos
        passo_y = dy / passos

        x, y = xi, yi
        sx = sign(passo_x) if passo_x != 0 else 1
        sy = sign(passo_y) if passo_y != 0 else 1
    
        self.set_pixel(int(x), int(y), intensidade)

        for _ in range(passos):
            x += passo_x
            y += passo_y
    
            if passo_x != 0:
                prop = abs(y - floor(y))
                self.set_pixel(floor(x), floor(y), tuple(round((1-prop)*value) for value in intensidade))
                self.set_pixel(floor(x), floor(y + sy), tuple(round(prop*value) for value in intensidade))
            else:
                prop = abs(x - floor(x))
                self.set_pixel(floor(x), floor(y), tuple(round((1-prop)*value) for value in intensidade))
                self.set_pixel(floor(x + sx), floor(y), tuple(round(prop*value) for value in intensidade))

    def bresenham(self, xi, yi, xf, yf, intensidade):
        if xf < xi:
            xi, xf = xf, xi
            yi, yf = yf, yi

        dx = abs(xf - xi)
        dy = abs(yf - yi)
        steep = dy > dx

        if steep:
            dx, dy = dy, dx
            swap = lambda a, b: (b, a)
            xi, yi = swap(xi, yi)
            xf, yf = swap(xf, yf)

        d = 2 * dy - dx
        y = yi

        for x in range(xi, xf + 1):
            if steep:
                self.set_pixel(y, x, intensidade)
            else:
                self.set_pixel(x, y, intensidade)
            if d > 0:
                y += 1
                d -= 2 * dx
            d += 2 * dy

    def scanline(self, poligono, intensidade=-1, tex=None):
        def intersecao(y, pi, pf):
            if pi[1] == pf[1]:
                return None
            t = (y - pi[1]) / (pf[1] - pi[1])
            if not (0 < t <= 1):
                return None
            x = pi[0] + t * (pf[0] - pi[0])
            cor = tuple(round(pi[2][i] + t * (pf[2][i] - pi[2][i])) for i in range(3))
            tx = pi[3] + t * (pf[3] - pi[3])
            ty = pi[4] + t * (pf[4] - pi[4])
            return [x, y, cor, tx, ty]

        def print_scan(p_int, intensidade, tex):
            p_int = sorted(p_int, key=lambda x: x[0])
            y = p_int[0][1]
            for i in range(0, len(p_int), 2):
                x0, x1 = p_int[i][0], p_int[i + 1][0]
                if x0 == x1:
                    continue
                for x in range(round(x0), round(x1)):
                    if intensidade != -1:
                        cor = intensidade
                    else:
                        k = (x - x0) / (x1 - x0)
                        inten = tuple(round(p_int[i][2][j] + k * (p_int[i + 1][2][j] - p_int[i][2][j])) for j in range(3))
                        tx = p_int[i][3] + k * (p_int[i + 1][3] - p_int[i][3])
                        ty = p_int[i][4] + k * (p_int[i + 1][4] - p_int[i][4])
                        cor = inten
                        if tex:
                            cor = tex.get_texel(tx, ty)
                    self.set_pixel(round(x), round(y), cor)

        yi, yf = min(p[1] for p in poligono), max(p[1] for p in poligono)
        
        for y in range(round(yi), round(yf)):
            p_int = []
            pi = poligono[-1]
            for pf in poligono:
                intersec = intersecao(y, pi, pf)
                if intersec:
                    p_int.append(intersec)
                pi = pf
            if len(p_int) > 1:
                print_scan(p_int, intensidade, tex)

            

            



    