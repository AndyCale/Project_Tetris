from PIL import Image


image = Image.new("RGB", (560, 1), (0, 0, 0))
pix = image.load()
'''for i in range(50, 100):
    for j in range(50):
        pix[i, j] = (0, 0, 0)
for i in range(50, 100):
    for j in range(100, 150):
        pix[i, j] = (0, 0, 0)'''
image.save("data//horiz.png")