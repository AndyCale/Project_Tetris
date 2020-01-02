import pygame
import os
from random import choice
from PIL import Image


pygame.init()
size = width, height = 560, 500
screen = pygame.display.set_mode(size)

fps = 50
clock = pygame.time.Clock()
running = True


def load_image(name, pos=(0, 0), colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    '''img = Image.open(fullname)
    pix = img.load()
    x, y = img.size
    for i in range(x):
        for j in range(y):
            if pix[i, j] == (255, 255, 255):
                pix[i, j] = color'''
    if colorkey is None:
        colorkey = image.get_at(pos)
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Block(pygame.sprite.Sprite):
    #color = choice([(255, 0, 0), (0, 255, 0), (0, 0, 255)])
    image = load_image("block_l.png", (60, 0))

    def __init__(self):
        super().__init__(all_spr)
        self.image = Block.image
        self.rect = pygame.Rect(255, 0, 100, 150)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.top = self.rect[1]

    def update(self):
        if not pygame.sprite.collide_mask(self, down) and not any([pygame.sprite.collide_mask(self, i) not in ((0, 0), None) for i in all_spr]):
            self.rect[1] += 1

    def run(self, s):
        if s == "l" and not pygame.sprite.collide_mask(self, l) and not any([pygame.sprite.collide_mask(self, i) not in ((0, 0), None) for i in all_spr]):
            self.rect[0] -= 50
        if any([pygame.sprite.collide_mask(self, i) not in ((0, 0), None) for i in all_spr]):
            self.rect[0] += 50
        if s == "r" and not pygame.sprite.collide_mask(self, r) and not any([pygame.sprite.collide_mask(self, i) not in ((0, 0), None) for i in all_spr]):
            self.rect[0] += 50
        if any([pygame.sprite.collide_mask(self, i) not in ((0, 0), None) for i in all_spr]):
            self.rect[0] -= 50


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, group, im):
        super().__init__(group)
        self.image = load_image(im, -1, -1)
        self.rect = self.image.get_rect()
        if group == horiz_bord:
            self.rect.bottom = height - 5
        elif group == vert_bord_l:
            self.rect.left = 5
        else:
            self.rect.right = width - 5
        self.add(all_sprites)


all_sprites = pygame.sprite.Group()
all_spr = pygame.sprite.Group()
vert_bord_l = pygame.sprite.Group()
vert_bord_r = pygame.sprite.Group()
horiz_bord = pygame.sprite.Group()

down = Border(horiz_bord, "horiz.png")
l = Border(vert_bord_l, "vert.png")
r = Border(vert_bord_r, "vert.png")

flag = True

while running:
    screen.fill((255, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                active = Block()
                '''i = choice(range(2))
                if i == 0:
                    active = BlockI()
                else:
                    active = BlockO()'''
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                active.run("l")
            elif event.key == pygame.K_RIGHT:
                active.run("r")
    for i in all_spr:
        i.update()
    all_spr.draw(screen)
    all_sprites.draw(screen)
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()