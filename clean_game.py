import pygame
import os
from random import choice


pygame.init()
size = width, height = 615, 500
screen = pygame.display.set_mode(size)

fps = 50
clock = pygame.time.Clock()
running = True


def load_image(name, pos=(0, 0), colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is None:
        colorkey = image.get_at(pos)
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def color_block(block, color):
    w, h = block.get_size()
    for x in range(w):
        for y in range(h):
            if block.get_at((x, y))[:3] != (0, 0, 0):
                block.set_at((x, y), color)


class Block(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_spr)
        self.image = load_image(choice(["block_l.png", "block_s.png", "block_t.png", "block_o.png", "block_i.png"]),
                                (0, 0))
        color = pygame.Color(choice(["red", "blue", "orange", "yellow", "green", "pink", "purple"]))
        if choice([0, 1]):
            self.image = pygame.transform.flip(self.image, 1, 0)
        color_block(self.image, color)
        self.rect = pygame.Rect(256, 0, 100, 150)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.top = self.rect[1]

    def update(self):
        global flag
        if not pygame.sprite.collide_mask(self, down) and\
                (not any([pygame.sprite.collide_mask(self, i) not in ((0, 0), None) for i in all_spr]) or
                 len([1 for i in all_spr if pygame.sprite.collide_mask(self, i) != None]) == 1):
            self.rect[1] += 1
        else:
            flag = True

    def run(self, s):
        if s == "l":
            if s == "l" and not pygame.sprite.collide_mask(self, l) and\
                (not any([pygame.sprite.collide_mask(self, i) not in ((0, 0), None) for i in all_spr]) or
                 len([1 for i in all_spr if pygame.sprite.collide_mask(self, i) != None]) == 1):
                self.rect[0] -= 50
            if pygame.sprite.collide_mask(self, l) != None or\
                    len([1 for i in all_spr if pygame.sprite.collide_mask(self, i) != None]) > 1:
                self.rect[0] += 50
        else:
            if s == "r" and not pygame.sprite.collide_mask(self, r) and\
                (not any([pygame.sprite.collide_mask(self, i) not in ((0, 0), None) for i in all_spr]) or
                 len([1 for i in all_spr if pygame.sprite.collide_mask(self, i) != None]) == 1):
                self.rect[0] += 50
            if pygame.sprite.collide_mask(self, r) != None or\
                    len([1 for i in all_spr if pygame.sprite.collide_mask(self, i) != None]) > 1:
                self.rect[0] -= 50

    def run_down(self):
        while not pygame.sprite.collide_mask(self, down) and\
                (not any([pygame.sprite.collide_mask(self, i) not in ((0, 0), None) for i in all_spr]) or
                 len([1 for i in all_spr if pygame.sprite.collide_mask(self, i) != None]) == 1):
            self.rect[1] += 1

    def rotate(self, angle):
        pygame.transform.rotate(self.image, angle)
        if pygame.sprite.collide_mask(self, l) != None or \
                    len([1 for i in all_spr if pygame.sprite.collide_mask(self, i) != None]) > 1:
            self.rect[0] += 50
            print(1)
        else:
            print(pygame.sprite.collide_mask(self, l) != None,
                  len([1 for i in all_spr if pygame.sprite.collide_mask(self, i) != None]) > 1)
        if pygame.sprite.collide_mask(self, r) != None or \
                len([1 for i in all_spr if pygame.sprite.collide_mask(self, i) != None]) > 1:
            self.rect[0] -= 50
            print(2)
        else:
            print(pygame.sprite.collide_mask(self, r) != None,
                  len([1 for i in all_spr if pygame.sprite.collide_mask(self, i) != None]) > 1)


class Border(pygame.sprite.Sprite):
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
active = 0

while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                active.run("l")
            if event.key == pygame.K_RIGHT:
                active.run("r")
            if event.key == pygame.K_SPACE:
                active.run_down()
            if event.key == pygame.K_DOWN:
                active.image = pygame.transform.rotate(active.image, 90)
                active.rect[2], active.rect[3] = active.rect[3], active.rect[2]
                active.mask = pygame.mask.from_surface(active.image)
                if pygame.sprite.collide_mask(active, l) != None or \
                        len([1 for i in all_spr if pygame.sprite.collide_mask(active, i) != None]) > 1:
                    active.rect[0] += 50
                if pygame.sprite.collide_mask(active, r) != None or \
                        len([1 for i in all_spr if pygame.sprite.collide_mask(active, i) != None]) > 1:
                    active.rect[0] -= 50
                while pygame.sprite.collide_mask(active, down) != None or len(
                        [1 for i in all_spr if pygame.sprite.collide_mask(active, i) != None]) > 1:
                    active.rect[1] -= 1
            if event.key == pygame.K_UP:
                active.image = pygame.transform.rotate(active.image, -90)
                active.rect[2], active.rect[3] = active.rect[3], active.rect[2]
                active.mask = pygame.mask.from_surface(active.image)
                print(active.mask)
                if pygame.sprite.collide_mask(active, l) != None or \
                        len([1 for i in all_spr if pygame.sprite.collide_mask(active, i) != None]) > 1:
                    active.rect[0] += 50
                if pygame.sprite.collide_mask(active, r) != None or \
                        len([1 for i in all_spr if pygame.sprite.collide_mask(active, i) != None]) > 1:
                    active.rect[0] -= 50
                while pygame.sprite.collide_mask(active, down) != None or len(
                        [1 for i in all_spr if pygame.sprite.collide_mask(active, i) != None]) > 1:
                    active.rect[1] -= 1

    if flag:
        active = Block()
        flag = False
    active.update()
    all_spr.draw(screen)
    all_sprites.draw(screen)
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()