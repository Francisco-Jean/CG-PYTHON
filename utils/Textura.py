import numpy as np
from math import floor
from PIL import Image

class Textura:
    def __init__(self, textura):
        self.img = np.array(Image.open(textura))
        self.largura = self.img.shape[1]
        self.altura = self.img.shape[0]

    def get_texel(self, tx, ty):
        
        tx = abs(tx)
        ty = abs(ty)

        tx = tx - floor(tx)
        ty = ty - floor(ty)

        x = round((self.largura -1) * tx)
        y = round((self.altura -1) * ty)

        return self.img[y, x]