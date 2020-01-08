from PIL import Image


image = Image.new("RGB", (150, 150), (0, 0, 0))
pix = image.load()
for i in range(100, 150):
    for j in range(150):
        pix[i, j] = (255, 255, 255)
for i in range(50, 100):
    for j in range(50, 100):
        pix[i, j] = (255, 255, 255)
image.save("data//block_t.png")