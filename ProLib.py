import numpy as np
from PIL import Image as im
from PIL import ImageDraw


class ProLib:

    def __init__(self, path):
        print('init')
        self.img = im.open(path)
        self.npImg = np.array(self.img)
        self.h, self.w = self.npImg.shape

    def median_filter(self):
        sumi = np.zeros((5, 5, 3), dtype=np.uint32)
        for i in range(self.h):
            for j in range(self.w):
                if i <= 5 or j <= 5 or i >= self.h - 5 or j >= self.w - 5:
                    continue
                else:
                    sumi = self.npImg[i - 2:i + 3, j - 2:j + 3]
                    sumi = np.median(sumi, axis=0)
                    sumi = np.median(sumi, axis=0)
                    self.npImg[i, j] = sumi
        return self.npImg

    def apply_kernel(self, kernel):
        print(kernel)
        new_img = np.zeros_like(self.npImg)
        h, w = self.npImg.shape
        for i in range(3, h - 3):
            for j in range(3, w - 3):
                x = np.sum(self.npImg[i:i + 3, j:j + 3] * kernel)
                if x < 0:
                    x = 0
                elif x > 255:
                    x = 255
                self.npImg[i][j] = x

        self.npImg = self.npImg / self.npImg.max() * 255
        return self.npImg

    def suppress_nonmax(self, angle):
        new_img = np.zeros_like(self.npImg)
        for i in range(1, self.h - 1):
            for j in range(1, self.w - 1):
                # angle 0
                if (0 <= angle[i, j] < 22.5) or (157.5 <= angle[i, j] <= 180):
                    q = self.npImg[i, j + 1]
                    r = self.npImg[i, j - 1]
                # angle 45
                elif 22.5 <= angle[i, j] < 67.5:
                    q = self.npImg[i + 1, j - 1]
                    r = self.npImg[i - 1, j + 1]
                # angle 90
                elif 67.5 <= angle[i, j] < 112.5:
                    q = self.npImg[i + 1, j]
                    r = self.npImg[i - 1, j]
                # angle 135
                elif 112.5 <= angle[i, j] < 157.5:
                    q = self.npImg[i - 1, j - 1]
                    r = self.npImg[i + 1, j + 1]
                if self.npImg[i][j] >= q and self.npImg[i][j] >= q:
                    new_img = self.npImg
        return new_img

    def threshold(self, low=0.05, high=0.09):
        hight = self.npImg.max() * high
        lowt = hight * low
        strongi, strongj = np.where(self.npImg >= hight)
        weaki, weakj = np.where((self.npImg >= lowt) & (self.npImg <= hight))
        new_img = np.zeros_like(self.npImg)
        new_img[strongi, strongj] = 255
        new_img[weaki, weakj] = 25
        kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
        new_img2 = np.zeros_like(self.npImg)
        for i in range(3, self.h - 3):
            for j in range(3, self.w - 3):
                if new_img[i, j] == 25:
                    x = np.sum(new_img[i:i + 3, j:j + 3] * kernel)
                    if x >= 255:
                        self.npImg[i, j] = 255
                elif new_img[i, j] == 255:
                    self.npImg[i, j] = 255
        return self.npImg

    def getdist(self, x, y):
        mindist = np.sqrt(self.npImg.shape[0] ** 2 + self.npImg.shape[1] ** 2)
        xN = 0
        yN = 0
        for i in range(self.h):
            for j in range(self.w):
                val = self.npImg[i, j]
                if val > 10:
                    dist = np.sqrt((x - i) ** 2 + (y - j) ** 2)
                    if dist < 3:
                        print(dist)
                    if dist < mindist:
                        xN = i
                        yN = j
                        mindist = dist
        print(mindist)
        print(xN)
        print(yN)
        return xN, yN

    def showImg(self):
        img = self.npImg
        img = img.astype(np.uint8)
        po = im.fromarray(img)
        im._show(po)
        return po

    def saveImg(self,name):
        img = self.showImg()
        img.save(name)


    def drawImg(self,x1,y1,x2,y2):
        img = self.npImg
        img = img.astype(np.uint8)
        po = im.fromarray(img)
        draw = ImageDraw.Draw(po)
        draw.line([(x1,y1),(x2,y2)],width=2, fill= 180)
        po.show()