from ProLib import *

path = './brainMRI.png'

# Initializing Object
im = ProLib(path)
print(im)

#Applying Median Filter
im.median_filter()

#Smoothining
kernel = np.array([[1 / 16, 2 / 16, 1 / 16], [1 / 8, 1 / 4, 1 / 8], [1 / 16, 2 / 16, 1 / 16]])
im.apply_kernel(kernel)

#Applying Vertical Edge Detection Filter
kernel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
imgy = im.apply_kernel(kernel)

#Applying Horizontal Edge Detection Filter
kernel = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
imgx = im.apply_kernel(kernel)

#Sobel
im.npImg = np.sqrt(np.square(imgx) + np.square(imgy))

#Canny
theta=np.arctan2(imgy,imgx)
im.suppress_nonmax(theta)
im.threshold()


im.showImg()
im.saveImg("canny.jpg")
x1, y1 = 50, 50
x2, y2 = im.getdist(x1, y1)
#im.drawImg(x1,y1,x2,y2)