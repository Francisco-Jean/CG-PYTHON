import numpy as np

class Poligono:
    def __init__(self):
        self.poligono = []
    
    def insere_ponto(self, x, y, i, tx, ty):
        self.poligono.append([x, y, i, tx, ty])
    
    def desenha_poligono(self, im, intensidade):
        for i in range(len(self.poligono)-1):
            im.bresenham(self.poligono[i][0], self.poligono[i][1], self.poligono[i+1][0], self.poligono[i+1][1], intensidade)
        
        im.bresenham(self.poligono[len(self.poligono) -1][0], self.poligono[len(self.poligono)-1][1], self.poligono[0][0], self.poligono[0][1], intensidade)

    def transforma(self, matriz):
        for i in range(len(self.poligono)):
            ponto = np.array([self.poligono[i][0], self.poligono[i][1], 1])
            ponto = np.dot(matriz, ponto)
            self.poligono[i][0] = ponto[0]
            self.poligono[i][1] = ponto[1]
    
    def rotacao(self, angulo, t = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]):
        angulo = np.radians(angulo)
        matriz = np.array([[np.cos(angulo), -np.sin(angulo), 0], [np.sin(angulo), np.cos(angulo), 0], [0, 0, 1]])
        return np.dot(matriz, t)
    
    def translacao(self, tx, ty, t = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]):
        matriz = np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]])
        return np.dot(matriz, t)
    
    def escala(self, sx, sy, t = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]):
        matriz = np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])
        return np.dot(matriz, t)
    
    def cisalhamento(self, shx, shy, t = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]):
        matriz = np.array([[1, shx, 0], [shy, 1, 0], [0, 0, 1]])
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

        matriz = np.array([[lvp/lj, 0, xvpmin - xmin * lvp/lj], 
                           [0, -avp/aj, avp + avp*ymin/aj + yvpmin],
                           [0, 0, 1]])
        self.transforma(matriz)