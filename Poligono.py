import numpy as np

class Poligono:
    def __init__(self):
        self.poligono = []
        self.centro = np.array([0.0, 0.0])
        self.tamanho_poligono = 0
    
    def insere_ponto(self, x, y, i, tx, ty):
        self.poligono.append([x, y, i, tx, ty])
        self.tamanho_poligono += 1
        self.centro = self.calcular_centro()
    
    def desenha_poligono(self, im, intensidade):
        for i in range(len(self.poligono) - 1):
            im.bresenham(self.poligono[i][0], self.poligono[i][1], self.poligono[i + 1][0], self.poligono[i + 1][1], intensidade)
        im.bresenham(self.poligono[-1][0], self.poligono[-1][1], self.poligono[0][0], self.poligono[0][1], intensidade)

    def calcular_centro(self):
        pontos = np.array([p[:2] for p in self.poligono])  # Extraímos apenas as coordenadas x e y
        return np.mean(pontos, axis=0)
    
    def get_centro(self):
        return self.centro

    def circunferencia(self, im, xc, yc, r, intensidade):
        # Limpa o polígono atual
        self.poligono = []
        self.tamanho_poligono = 0
        
        # Adiciona pontos da circunferência ao polígono
        ang = 0
        while ang < 2 * np.pi:
            x = int(xc + r * np.cos(ang))
            y = int(yc + r * np.sin(ang))
            
            # Verifica se os pontos estão dentro dos limites da imagem
            if 0 <= x < im.largura and 0 <= y < im.altura:
                self.insere_ponto(x, y, intensidade, 0, 0)  # tx e ty são 0 porque não estamos usando textura aqui
            ang += 0.25
        
    def transforma(self, matriz):
        for i in range(len(self.poligono)):
            ponto = np.array([self.poligono[i][0], self.poligono[i][1], 1])
            ponto = np.dot(matriz, ponto)
            self.poligono[i][0], self.poligono[i][1] = ponto[0], ponto[1]
        self.centro = self.calcular_centro()
    
    def rotacao(self, angulo, t=np.identity(3)):
        angulo = np.radians(angulo)
        matriz = np.array([
            [np.cos(angulo), -np.sin(angulo), 0],
            [np.sin(angulo),  np.cos(angulo), 0],
            [0, 0, 1]
        ])
        return np.dot(matriz, t)
    
    def translacao(self, tx, ty, t=np.identity(3)):
        matriz = np.array([
            [1, 0, tx],
            [0, 1, ty],
            [0, 0, 1]
        ])
        return np.dot(matriz, t)

    def escala(self, sx, sy, t=np.identity(3)):
        matriz = np.array([
            [sx, 0, 0],
            [0, sy, 0],
            [0, 0, 1]
        ])
        return np.dot(matriz, t)
    
    def cisalhamento(self, shx, shy, t=np.identity(3)):
        matriz = np.array([
            [1, shx, 0],
            [shy, 1, 0],
            [0, 0, 1]
        ])
        return np.dot(matriz, t)
    
    def mapeiaJanela(self, j, v):
        lvp = v[2]
        lj = j[2]
        xvpmin = v[0]
        xmin = j[0]
        avp = v[3]
        ymin = j[1]
        aj = j[3]
        yvpmin = v[1]

        matriz = np.array([
            [lvp / lj, 0, xvpmin - xmin * lvp / lj],
            [0, -avp / aj, avp + avp * ymin / aj + yvpmin],
            [0, 0, 1]
        ])
        self.transforma(matriz)
    
    
    def clipping_cohen_sutherland(self, x_min, y_min, x_max, y_max):
        INSIDE = 0  # 0000
        LEFT = 1    # 0001
        RIGHT = 2   # 0010
        BOTTOM = 4  # 0100
        TOP = 8     # 1000

        def compute_out_code(x, y):
            code = INSIDE
            if x < x_min:
                code |= LEFT
            elif x > x_max:
                code |= RIGHT
            if y < y_min:
                code |= BOTTOM
            elif y > y_max:
                code |= TOP
            return code

        new_poligono = []

        for i in range(len(self.poligono)):
            x0, y0, i0, tx0, ty0 = self.poligono[i]
            x1, y1, i1, tx1, ty1 = self.poligono[(i + 1) % self.tamanho_poligono]
            out_code0 = compute_out_code(x0, y0)
            out_code1 = compute_out_code(x1, y1)
            accept = False

            while True:
                if out_code0 == 0 and out_code1 == 0:
                    accept = True
                    break
                elif (out_code0 & out_code1) != 0:
                    break
                else:
                    out_code_out = out_code0 if out_code0 != 0 else out_code1
                    x, y, i_interp, tx, ty = 0.0, 0.0, [0, 0, 0], 0.0, 0.0

                    if out_code_out & TOP:
                        x = x0 + (x1 - x0) * (y_max - y0) / (y1 - y0)
                        y = y_max
                    elif out_code_out & BOTTOM:
                        x = x0 + (x1 - x0) * (y_min - y0) / (y1 - y0)
                        y = y_min
                    elif out_code_out & RIGHT:
                        y = y0 + (y1 - y0) * (x_max - x0) / (x1 - x0)
                        x = x_max
                    elif out_code_out & LEFT:
                        y = y0 + (y1 - y0) * (x_min - x0) / (x1 - x0)
                        x = x_min

                    t = ((x - x0) / (x1 - x0)) if (x1 - x0) != 0 else ((y - y0) / (y1 - y0))
                    for k in range(3):
                        i_interp[k] = i0[k] + t * (i1[k] - i0[k])
                    tx = tx0 + t * (tx1 - tx0)
                    ty = ty0 + t * (ty1 - ty0)

                    if out_code_out == out_code0:
                        x0, y0, i0, tx0, ty0 = x, y, i_interp, tx, ty
                        out_code0 = compute_out_code(x0, y0)
                    else:
                        x1, y1, i1, tx1, ty1 = x, y, i_interp, tx, ty
                        out_code1 = compute_out_code(x1, y1)

            if accept:
                if not new_poligono or new_poligono[-1][:2] != [x0, y0]:
                    new_poligono.append([x0, y0, i0, tx0, ty0])
                if new_poligono[-1][:2] != [x1, y1]:
                    new_poligono.append([x1, y1, i1, tx1, ty1])

        return new_poligono