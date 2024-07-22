import numpy as np
from numpy import sign
import matplotlib.pyplot as plt
from math import floor
import concurrent.futures

class Imagem:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.img = np.zeros((altura, largura), dtype='3int')
    
    def set_pixel(self, x, y, intensidade):
        if x < 0 or x >= self.largura or y < 0 or y >= self.altura:
            return
        self.img[y, x] = intensidade
    
    def imshow(self):
        plt.imshow(self.img)
        plt.show()

    def limpa_imagem(self):
        self.img = np.zeros((self.altura, self.largura), dtype='3int')
    
    def dda(self, xi, yi, xf, yf, intensidade):
        dx = xf - xi
        dy = yf - yi

        passos = abs(dx) if abs(dx) > abs(dy) else abs(dy)

        passo_x = dx / passos
        passo_y = dy / passos

        x = xi
        y = yi

        self.set_pixel(round(x), round(y), intensidade)


        for i in range(passos):
            x += passo_x
            y += passo_y
            self.set_pixel(round(x), round(y), intensidade)

    def dda_aa(self, xi, yi, xf, yf, intensidade):
        dx = xf - xi
        dy = yf - yi

        passos = abs(dx) if abs(dx) > abs(dy) else abs(dy)
        passo_x = dx / passos
        passo_y = dy / passos

        x = xi
        y = yi
        sx = sign(passo_x)
        sy = sign(passo_y)

        if sx == 0:
            sx = self.largura + 1
        if sy == 0:
            sy = self.altura + 1
    
        self.set_pixel(int(x), int(y), intensidade)

        for i in range(passos):
            x += passo_x
            y += passo_y
    
            if passo_x == 1 or passo_x == -1:
                prop = abs(y - floor(y))
                self.set_pixel(floor(x), floor(y), tuple(round((1-prop)* value) for value in intensidade))
                self.set_pixel(floor(x), floor(y + sy), tuple(round(prop* value) for value in intensidade))
            else:
                prop = abs(x - floor(x))
                self.set_pixel(floor(x), floor(y), tuple(round((1-prop)* value) for value in intensidade))
                self.set_pixel(floor(x + sx), floor(y), tuple(round(prop* value) for value in intensidade))

    def bresenham(self, xi, yi, xf, yf, intensidade):
        if xf < xi:
            aux = xf
            xf = xi
            xi = aux
            aux = yf
            yf = yi
            yi = aux

        dx = abs(xf - xi)
        dy = abs(yf - yi)

        aux = 0
        if dy > dx:
            aux = dx
            dx = dy
            dy = aux
            aux = 1
        
        y = 0

        dy2 = 2 * dy
        dy2dx2 = dy2 - 2*dx
        s = sign(yf - yi)

        p = dx - dy2
        
        for x in range(dx+1):
            if p < 0:
                p -= dy2dx2
                y += 1
            else:
                p -= dy2  
                
            if aux == 0:
                self.set_pixel(xi + x, yi + s * y, intensidade)
            else:
                self.set_pixel(xi + y, yi + s*x, intensidade)
    def scanline(self, poligono, intensidade=-1, tex=0):
        
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
                x0, x1 = p_int[i][0], p_int[i+1][0]
                if x0 == x1:
                    continue
                for x in range(round(x0), round(x1)):
                    if intensidade != -1:
                        cor = intensidade
                    else:
                        k = (x - x0) / (x1 - x0)
                        inten = tuple(round(p_int[i][2][j] + k * (p_int[i+1][2][j] - p_int[i][2][j])) for j in range(3))
                        tx = p_int[i][3] + k * (p_int[i+1][3] - p_int[i][3])
                        ty = p_int[i][4] + k * (p_int[i+1][4] - p_int[i][4])
                        cor = inten
                        if tex != 0:
                            cor = tex.get_texel(tx, ty)
                    self.set_pixel(round(x), round(y), cor)

        def process_scanline(y, pi, poligono):
            p_int = []
            for i in range(len(poligono)):
                pf = poligono[i]
                intersec = intersecao(y, pi, pf)
                if intersec:
                    p_int.append(intersec)
                pi = pf
            pf = poligono[0]
            intersec = intersecao(y, pi, pf)
            if intersec:
                p_int.append(intersec)
            if len(p_int) > 1:
                print_scan(p_int, intensidade, tex)

        yi, yf = min(p[1] for p in poligono), max(p[1] for p in poligono)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_scanline, y, poligono[0], poligono) for y in range(round(yi), round(yf))]
            concurrent.futures.wait(futures)
            

            



    