from ProLib import *

path = './brainMRI.png'
im = ProLib(path)
print(im)
im.median_filter()
kernel = np.array([[1 / 16, 2 / 16, 1 / 16], [1 / 8, 1 / 4, 1 / 8], [1 / 16, 2 / 16, 1 / 16]])
im.apply_kernel(kernel)
kernel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
imgy = im.apply_kernel(kernel)
kernel = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
imgx = im.apply_kernel(kernel)
im.npimg = np.sqrt(np.square(imgx) + np.square(imgy))
img = im.npimg.astype(np.uint8)
po = img.fromarray(img)

