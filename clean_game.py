import pygame
import os
from random import choice
from PIL import Image


pygame.init()
size = width, height = 615, 800
screen = pygame.display.set_mode(size)

fps = 50
clock = pygame.time.Clock()
running = True


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is None:
        colorkey = (0, 0, 0, 255)
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
    def __init__(self, img=-1, rct=-1):
        super().__init__(all_blocks)
        #self.name =
        if img == -1:
            self.image = load_image(choice(["block_l.png", "block_s.png", "block_t.png", "block_o.png", "block_i.png"]))
            color = pygame.Color(choice(["red", "blue", "orange", "yellow", "green", "pink", "purple"]))
            if choice([0, 1]):
                self.image = pygame.transform.flip(self.image, 1, 0)
            color_block(self.image, color)
            self.rect = pygame.Rect(256, 0, 150, 200)
        else:
            self.image = img
            colorkey = (0, 0, 0, 255)
            self.image.set_colorkey(colorkey)
            self.rect = pygame.Rect(rct[0], rct[1], rct[2], rct[3])
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        global flag
        if not pygame.sprite.collide_mask(self, down) and\
                (not any([pygame.sprite.collide_mask(self, i) not in ((0, 0), None) for i in all_blocks]) or
                 len([1 for i in all_blocks if pygame.sprite.collide_mask(self, i) != None]) == 1):
            self.rect[1] += 1
        else:
            cells = []
            for i in pygame.sprite.spritecollide(self, points, False):
                if pygame.sprite.collide_mask(self, i):
                    cells.append(pnt[i])
            board.add(cells)
            flag = True
            for i in all_blocks:
                print(i.rect, i.mask, i.image)

    def run(self, s):
        if s == "l":
            if s == "l" and not pygame.sprite.collide_mask(self, l) and\
                (not any([pygame.sprite.collide_mask(self, i) not in ((0, 0), None) for i in all_blocks]) or
                 len([1 for i in all_blocks if pygame.sprite.collide_mask(self, i) != None]) == 1):
                self.rect[0] -= 50
            if pygame.sprite.collide_mask(self, l) != None or\
                    len([1 for i in all_blocks if pygame.sprite.collide_mask(self, i) != None]) > 1:
                self.rect[0] += 50
        else:
            if s == "r" and not pygame.sprite.collide_mask(self, r) and\
                (not any([pygame.sprite.collide_mask(self, i) not in ((0, 0), None) for i in all_blocks]) or
                 len([1 for i in all_blocks if pygame.sprite.collide_mask(self, i) != None]) == 1):
                self.rect[0] += 50
            if pygame.sprite.collide_mask(self, r) != None or\
                    len([1 for i in all_blocks if pygame.sprite.collide_mask(self, i) != None]) > 1:
                self.rect[0] -= 50

    def run_down(self):
        while not pygame.sprite.collide_mask(self, down) and\
                (not any([pygame.sprite.collide_mask(self, i) not in ((0, 0), None) for i in all_blocks]) or
                 len([1 for i in all_blocks if pygame.sprite.collide_mask(self, i) != None]) == 1):
            '''print(self.rect, pygame.sprite.collide_mask(self, down),
                  any([pygame.sprite.collide_mask(self, i) not in ((0, 0), None) for i in all_blocks]),
                  len([1 for i in all_blocks if pygame.sprite.collide_mask(self, i) != None]) == 1)'''
            self.rect[1] += 1

    def cut(self):
        w, h = self.image.get_size()
        q, e, r, t = 0, 0, 0, 0
        while all([self.image.get_at((q, y))[:3] == (0, 0, 0) for y in range(h)]) and q < w - 1:
            q += 1
        while all([self.image.get_at((x, e))[:3] == (0, 0, 0) for x in range(w)]) and e < h - 1:
            e += 1
        while all([self.image.get_at((w - r - 1, y))[:3] == (0, 0, 0) for y in range(h)]) and r < w - 1:
            r += 1
        while all([self.image.get_at((x, h - t - 1))[:3] == (0, 0, 0) for x in range(w)]) and t < h - 1:
            t += 1
        cropped = pygame.Surface((w - r - q, h - t - e))
        cropped.blit(self.image, (0, 0), (q, e, w - r, h - t))
        return cropped


class Border(pygame.sprite.Sprite):
    def __init__(self, group, im):
        super().__init__(group)
        self.image = load_image(im, -1)
        self.rect = self.image.get_rect()
        if group == horiz_bord:
            self.rect.bottom = height - 5
        elif group == vert_bord_l:
            self.rect.left = 5
        else:
            self.rect.right = width - 5
        self.add(all_sprites)


class Board:
    def __init__(self, wid, hei):
        self.board = [[0] * wid for _ in range(hei)]

    def add(self, cells):
        for cell in cells:
            self.board[cell[0]][cell[1]] = 1
        for line in range(len(self.board)):
            if all(self.board[line]):
                self.delete_line(line)
                print("\n".join([" ".join(list(map(str, i))) for i in self.board]))
                print(1)
                for i in range(line, 0, -1):
                    self.board[i] = self.board[i - 1]
                print("\n".join([" ".join(list(map(str, i))) for i in self.board]))

    def delete_line(self, line):
        line_spr = Line(line * 50 + 25 + height % 50)
        #print(line_spr.rect)
        for block in pygame.sprite.spritecollide(line_spr, all_blocks, False):
            #print(1, block.rect)
            if line_spr.rect[1] - block.rect[1] > 50 and block.rect[1] + block.rect[3] - line_spr.rect[1] > 50:
                print(1, block.rect[2], (line_spr.rect[1] - block.rect[1]) // 50 * 50)
            elif line_spr.rect[1] - block.rect[1] > 50:
                print(2, block.rect[2], (line_spr.rect[1] - block.rect[1]) // 50 * 50)
                #cropped = pygame.sprite.Sprite
                cropped = pygame.Surface((block.rect[2], (line_spr.rect[1] - block.rect[1]) // 50 * 50))
                cropped.blit(block.image, (0, 0), (0, 0, block.rect[2], (line_spr.rect[1] - block.rect[1]) // 50 * 50))
                Block(cropped, (block.rect[0], block.rect[1], block.rect[2], (line_spr.rect[1] - block.rect[1]) // 50 * 50))
                all_blocks.remove(block)
            elif block.rect[1] + block.rect[3] - line_spr.rect[1] > 50:
                print(3, block.rect[2], (block.rect[1] + block.rect[3] - line_spr.rect[1]) % 50 * 50)
            else:
                all_blocks.remove(block)
                '''cropped_one = pygame.Surface((block.rect[2], (line_spr.rect[1] - block.rect[1]) // 50 * 50))
                cropped_two = pygame.Surface((200, 200))
                
            cropped.add(all_sprites)
            cropped = pygame.Surface((200, 200))
            cropped.blit(active.image, (0, 0), (0, 0, 150, int(str(active.image).split("(")[1].split("x")[1]) - 50))
            screen.blit(cropped, (0, 0))
            all_blocks.remove(block)'''
        lines.empty()


class Point(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(points)
        self.image = pygame.Surface((2, 2), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"), (1, 1), 1)
        self.rect = pygame.Rect(x, y, 2, 2)


class Line(pygame.sprite.Sprite):
    def __init__(self, line):
        super().__init__(lines)
        self.image = pygame.Surface([width, 1])
        self.rect = pygame.Rect(0, line, width, 1)


image = Image.new("RGB", (width, 1), (0, 0, 0))
pix = image.load()
for i in range(width):
    pix[i, 0] = (0, 0, 0)
image.save("data//horiz.png")
image = Image.new("RGB", (1, height), (0, 0, 0))
pix = image.load()
for j in range(height):
    pix[0, j] = (0, 0, 0)
image.save("data//vert.png")


all_sprites = pygame.sprite.Group()
all_blocks = pygame.sprite.Group()
vert_bord_l = pygame.sprite.Group()
vert_bord_r = pygame.sprite.Group()
horiz_bord = pygame.sprite.Group()
board = Board(width // 50, height // 50)
points = pygame.sprite.Group()
lines = pygame.sprite.Group()

pnt = {}
for i in range(width // 50):
    for j in range(height // 50):
        pnt[Point(i * 50 + 25 + width % 50, j * 50 + 25 + height % 50)] = (j, i)

down = Border(horiz_bord, "horiz.png")
l = Border(vert_bord_l, "vert.png")
r = Border(vert_bord_r, "vert.png")

flag = True
active = 0
k = 1

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
                while pygame.sprite.collide_mask(active, l) != None or \
                        len([1 for i in all_blocks if pygame.sprite.collide_mask(active, i) != None]) > 1:
                    active.rect[0] += 50
                while pygame.sprite.collide_mask(active, r) != None or \
                        len([1 for i in all_blocks if pygame.sprite.collide_mask(active, i) != None]) > 1:
                    active.rect[0] -= 50
                while pygame.sprite.collide_mask(active, down) != None or len(
                        [1 for i in all_blocks if pygame.sprite.collide_mask(active, i) != None]) > 1:
                    active.rect[1] -= 1
            if event.key == pygame.K_UP:
                active.image = pygame.transform.rotate(active.image, -90)
                active.rect[2], active.rect[3] = active.rect[3], active.rect[2]
                active.mask = pygame.mask.from_surface(active.image)
                while pygame.sprite.collide_mask(active, l) != None or \
                        len([1 for i in all_blocks if pygame.sprite.collide_mask(active, i) != None]) > 1:
                    active.rect[0] += 50
                while pygame.sprite.collide_mask(active, r) != None or \
                        len([1 for i in all_blocks if pygame.sprite.collide_mask(active, i) != None]) > 1:
                    active.rect[0] -= 50
                while pygame.sprite.collide_mask(active, down) != None or len(
                        [1 for i in all_blocks if pygame.sprite.collide_mask(active, i) != None]) > 1:
                    active.rect[1] -= 1

    if flag:
        active = Block()
        active.image = active.cut()
        colorkey = (0, 0, 0, 255)
        active.image.set_colorkey(colorkey)
        active.mask = pygame.mask.from_surface(active.image)
        active.rect[2] = int(str(active.image).split("(")[1].split("x")[0])
        active.rect[3] = int(str(active.image).split("(")[1].split("x")[1])
        flag = False
        for i in all_blocks:
            if i != active:
                i.run_down()
                i.cut()
    cropped = pygame.Surface((200, 200))
    cropped.blit(active.image, (0, 0), (0, 0, 150, int(str(active.image).split("(")[1].split("x")[1]) - 50))
    screen.blit(cropped, (0, 0))
    active.update()
    all_blocks.draw(screen)
    all_sprites.draw(screen)
    points.draw(screen)
    lines.draw(screen)
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()