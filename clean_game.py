import pygame
import os
from random import choice
from PIL import Image
from time import perf_counter


pygame.init()
size = (900, 800)
width, height = 615, 800
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


def next_block():
    img = load_image(choice(["block_l.png", "block_s.png", "block_t.png", "block_o.png", "block_i.png"]))
    color = pygame.Color(choice(["red", "blue", "orange", "yellow", "green", "pink", "purple"]))
    if choice([0, 1]):
        img = pygame.transform.flip(img, 1, 0)
    color_block(img, color)
    rect = pygame.Rect(256, 0, 150, 200)
    return img, rect


class Block(pygame.sprite.Sprite):
    def __init__(self, img=None, rect=None, nxt=None):
        super().__init__(all_blocks)
        if img is None:
            self.image, self.rect = nxt[0], nxt[1]
        else:
            self.image = img
            self.rect = pygame.Rect(rect[0], rect[1], rect[2], rect[3])
        self.image, self.rect = self.cut()[0], pygame.Rect(self.cut()[1])
        color_key = (0, 0, 0, 255)
        self.image.set_colorkey(color_key)
        self.mask = pygame.mask.from_surface(self.image)
        self.image, self.rect = self.cut()[0], pygame.Rect(self.cut()[1])
        color_key = (0, 0, 0, 255)
        self.image.set_colorkey(color_key)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        global flag
        if not pygame.sprite.collide_mask(self, down) and\
                (not any([pygame.sprite.collide_mask(self, i) not in ((0, 0), None) for i in all_blocks]) or
                 len([1 for i in all_blocks if pygame.sprite.collide_mask(self, i) != None]) == 1):
            self.rect[1] += speed
        else:
            cells = []
            for i in pygame.sprite.spritecollide(self, points, False):
                if pygame.sprite.collide_mask(self, i):
                    cells.append(pnt[i])
            board.add(cells)
            flag = True

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
                (len([1 for i in all_blocks if pygame.sprite.collide_mask(self, i) is not None and self.rect[1] + self.rect[3] < i.rect[1] + i.rect[3]]) == 0):
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
        '''for i in range(w):
            print("\n")
            for j in range(h):
                #print(i, j, w, h)
                #print(0 if self.image.get_at((j, i)) == (0, 0, 0) else 1, end=" ")
                k = 0 if self.image.get_at((i, j)) == (0, 0, 0) else 1'''
        if w - r - q > 0 and h - t - e > 0:
            cropped = pygame.Surface((w - r - q, h - t - e))
            cropped.blit(self.image, (0, 0), (q, e, w - r - q, h - t - e))
            return cropped, (self.rect[0] + q, self.rect[1] + e, w - r - q, h - t - e)


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
        global score

        for cell in cells:
            self.board[cell[0]][cell[1]] = 1
        for line in range(len(self.board)):
            if all(self.board[line]):
                score += 100
                self.delete_line(line)
                print("\n".join([" ".join(list(map(str, i))) for i in self.board]))
                print(1)
                for i in range(line, 0, -1):
                    self.board[i] = self.board[i - 1]
                print("\n".join([" ".join(list(map(str, i))) for i in self.board]))
        for i in range(len(self.board)):
            print(end="\n")
            for j in range(len(self.board[0])):
                print(self.board[i][j], end=" ")

    def delete_line(self, line):
        line_spr = Line(line * 50 + 25 + height % 50)
        for block in pygame.sprite.spritecollide(line_spr, all_blocks, False):
            if line_spr.rect[1] - block.rect[1] > 50 and block.rect[1] + block.rect[3] - line_spr.rect[1] > 50:
                print(1, block.rect[2], (line_spr.rect[1] - block.rect[1]) // 50 * 50)
                cropped_bl_1 = pygame.Surface((block.rect[2], (line_spr.rect[1] - block.rect[1]) // 50 * 50))
                cropped_bl_1.blit(block.image, (0, 0), (0, 0, block.rect[2], (line_spr.rect[1] - block.rect[1]) // 50 * 50))
                Block(cropped_bl_1, (block.rect[0], block.rect[1], block.rect[2], (line_spr.rect[1] - block.rect[1]) // 50 * 50))
                cropped_bl_2 = pygame.Surface((block.rect[2], (block.rect[1] + block.rect[3] - line_spr.rect[1]) // 50 * 50))
                cropped_bl_2.blit(block.image, (0, 0), (0, (line_spr.rect[1] // 50 + 1) * 50, block.rect[2], (block.rect[1] + block.rect[3] - line_spr.rect[1]) % 50 * 50))
                Block(cropped_bl_2, (block.rect[0], (line_spr.rect[1] // 50 + 1) * 50, block.rect[2], (block.rect[1] + block.rect[3] - line_spr.rect[1]) // 50 * 50))
                all_blocks.remove(block)
            elif line_spr.rect[1] - block.rect[1] > 50:
                print(2, block.rect[2], (line_spr.rect[1] - block.rect[1]) // 50 * 50)
                cropped_bl = pygame.Surface((block.rect[2], (line_spr.rect[1] - block.rect[1]) // 50 * 50))
                cropped_bl.blit(block.image, (0, 0), (0, 0, block.rect[2], (line_spr.rect[1] - block.rect[1]) // 50 * 50))
                Block(cropped_bl, (block.rect[0], block.rect[1], block.rect[2], (line_spr.rect[1] - block.rect[1]) // 50 * 50))
                all_blocks.remove(block)
            elif block.rect[1] + block.rect[3] - line_spr.rect[1] > 50:
                print(3, block.rect[2], (block.rect[1] + block.rect[3] - line_spr.rect[1]) // 50 * 50)
                cropped_bl = pygame.Surface((block.rect[2], (block.rect[1] + block.rect[3] - line_spr.rect[1]) // 50 * 50))
                cropped_bl.blit(block.image, (0, 0), (0, (line_spr.rect[1] // 50 + 1) * 50, block.rect[2], (block.rect[1] + block.rect[3] - line_spr.rect[1]) // 50 * 50))
                Block(cropped_bl, (block.rect[0], (line_spr.rect[1] // 50 + 1) * 50, block.rect[2], (block.rect[1] + block.rect[3] - line_spr.rect[1]) // 50 * 50))
                all_blocks.remove(block)
            else:
                all_blocks.remove(block)
        for i in all_blocks:
            if i != active:
                i.run_down()
        lines.empty()


class Point(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__(group)
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
points_vis = pygame.sprite.Group()
next_qroup_block = pygame.sprite.Group()

pnt = {}
for i in range(width // 50):
    for j in range(height // 50):
        pnt[Point(i * 50 + 25 + width % 50, j * 50 + 25 + height % 50, points)] = (j, i)

for i in range(width // 50 + 1):
    for j in range(height // 50 + 1):
        Point(i * 50 + 5, j * 50 - 5, points_vis)

down = Border(horiz_bord, "horiz.png")
l = Border(vert_bord_l, "vert.png")
r = Border(vert_bord_r, "vert.png")

flag = True
active = 0
k = 1
speed = 1
score = 0
time = perf_counter()
time_pause = 0
next_image = next_block()
game = True
active_menu = ""
time_for_pause = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game:
                    game = False
                    time_pause = perf_counter()
                else:
                    game = True
                    time += perf_counter() - time_pause
                    active_menu = ""
            if event.key == pygame.K_LEFT and game:
                active.run("l")
            if event.key == pygame.K_RIGHT and game:
                active.run("r")
            if event.key == pygame.K_SPACE and game:
                active.run_down()
            if event.key == pygame.K_DOWN and game:
                active.image = pygame.transform.rotate(active.image, 90)
                active.rect[2], active.rect[3] = active.rect[3], active.rect[2]
                active.mask = pygame.mask.from_surface(active.image)
                if len([1 for i in all_blocks if pygame.sprite.collide_mask(active, i) is not None]) > 1:
                    active.image = pygame.transform.rotate(active.image, -90)
                    active.rect[2], active.rect[3] = active.rect[3], active.rect[2]
                    active.mask = pygame.mask.from_surface(active.image)
                else:
                    while pygame.sprite.collide_mask(active, down) is not None or\
                            len([1 for i in all_blocks if pygame.sprite.collide_mask(active, i) is not None]) > 1:
                        active.rect[1] -= 1
                    while pygame.sprite.collide_mask(active, l) is not None:
                        active.rect[0] += 50
                    while pygame.sprite.collide_mask(active, r) is not None:
                        active.rect[0] -= 50
            if event.key == pygame.K_UP and game:
                active.image = pygame.transform.rotate(active.image, -90)
                active.rect[2], active.rect[3] = active.rect[3], active.rect[2]
                active.mask = pygame.mask.from_surface(active.image)
                if len([1 for i in all_blocks if pygame.sprite.collide_mask(active, i) is not None]) > 1:
                    active.image = pygame.transform.rotate(active.image, 90)
                    active.rect[2], active.rect[3] = active.rect[3], active.rect[2]
                    active.mask = pygame.mask.from_surface(active.image)
                else:
                    while pygame.sprite.collide_mask(active, down) is not None or len(
                            [1 for i in all_blocks if pygame.sprite.collide_mask(active, i) is not None]) > 1:
                        active.rect[1] -= 1
                    while pygame.sprite.collide_mask(active, l) is not None:
                        active.rect[0] += 50
                    while pygame.sprite.collide_mask(active, r) is not None:
                        active.rect[0] -= 50

        if not game:
            if active_menu == "":
                pygame.draw.rect(screen, (100, 100, 100), (size[0] // 2 - 165, size[1] // 2 - 200, 330, 400))
                pygame.draw.rect(screen, (255, 255, 255), (size[0] // 2 - 165, size[1] // 2 - 200, 330, 400), 1)

                font = pygame.font.Font(None, 70)
                text = font.render("Пауза", 1, (20, 20, 20))
                text_x = size[0] // 2 - text.get_width() // 2
                text_y = 230
                screen.blit(text, (text_x, text_y))

                font = pygame.font.Font(None, 50)

                for i in range(4):
                    pygame.draw.rect(screen,
                                     ((140, 200, 200), (200, 140, 200), (200, 200, 140), (140, 200, 140))[i],
                                     (310, 300 + i * 70, 280, 50))
                    pygame.draw.rect(screen, (0, 0, 0), (310, 300 + i * 70, 280, 50), 1)

                    text = font.render(["Продолжить", "Перезапустить", "Помощь", "Главное меню"][i], 1,
                                       (40, 40, 40))
                    text_x = size[0] // 2 - text.get_width() // 2
                    text_y = 308 + i * 70
                    screen.blit(text, (text_x, text_y))

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if 310 <= pos[0] <= 590 and 300 <= pos[1] <= 350 and active_menu == "":
                    active_menu = ""
                    game = True
                    time += perf_counter() - time_pause
                elif 310 <= pos[0] <= 590 and 370 <= pos[1] <= 420 and active_menu == "":
                    active_menu = "replay"
                elif 310 <= pos[0] <= 590 and 440 <= pos[1] <= 490 and active_menu == "":
                    pass
                    #active_menu = "help"
                    #rules()
                elif 310 <= pos[0] <= 590 and 510 <= pos[1] <= 560 and active_menu == "":
                    active_menu = "exit"
                elif 310 <= pos[0] <= 590 and 370 <= pos[1] <= 420 and active_menu in ["exit", "replay"]:
                    if active_menu == "exit":
                        running = False
                        # terminated()
                    else:
                        pass
                        # как-то перезапускать игру
                elif 310 <= pos[0] <= 590 and 440 <= pos[1] <= 490 and active_menu in ["exit", "replay"]:
                    active_menu = ""

                    screen.fill((0, 0, 0))
                    all_blocks.draw(screen)
                    all_sprites.draw(screen)
                    points_vis.draw(screen)
                    lines.draw(screen)

                    pygame.draw.rect(screen, (50, 50, 50), (width, 0, size[0] - width, height))
                    pygame.draw.rect(screen, (100, 100, 100), (width + (size[0] - width) // 2 - 80, 100, 160, 160))
                    pygame.draw.rect(screen, (100, 100, 100), (width + (size[0] - width) // 2 - 110, 360, 220, 50))
                    pygame.draw.rect(screen, (100, 100, 100), (width + (size[0] - width) // 2 - 110, 510, 220, 50))
                    pygame.draw.rect(screen, (100, 100, 100), (width + (size[0] - width) // 2 - 110, 660, 220, 50))
                    pygame.draw.rect(screen, (255, 255, 255), (width + (size[0] - width) // 2 - 80, 100, 160, 160), 1)
                    pygame.draw.rect(screen, (255, 255, 255), (width + (size[0] - width) // 2 - 110, 360, 220, 50), 1)
                    pygame.draw.rect(screen, (255, 255, 255), (width + (size[0] - width) // 2 - 110, 510, 220, 50), 1)
                    pygame.draw.rect(screen, (255, 255, 255), (width + (size[0] - width) // 2 - 110, 660, 220, 50), 1)

                    font = pygame.font.Font(None, 50)

                    if len(time_for_pause) != 0:
                        mint, sec, mil = time_for_pause
                    else:
                        mint, sec, mil = "00", "00", "00"

                    text = font.render(mint + ":" + sec + ":" + mil, 1, (255, 255, 255))
                    text_x = 715
                    text_y = 370
                    screen.blit(text, (text_x, text_y))
                    text = font.render(str(score), 1, (255, 255, 255))
                    text_x = 854 - text.get_width()
                    text_y = 520
                    screen.blit(text, (text_x, text_y))

                    font = pygame.font.Font(None, 70)
                    text = font.render("Далее:", 1, (0, 0, 0))
                    text_x = width + (size[0] - width) // 2 - 85
                    text_y = 35
                    screen.blit(text, (text_x, text_y))

                    for i in range(3):
                        text = font.render(["Время:", "Очки:", "Рекорд:"][i], 1, (0, 0, 0))
                        text_x = width + (size[0] - width) // 2 - 100
                        text_y = 300 + i * 150
                        screen.blit(text, (text_x, text_y))

                    next_min = pygame.transform.scale(next_image[0], (150, 150))
                    screen.blit(next_min, (width + (size[0] - width) // 2 - 80 + 5, 105))

                    pygame.draw.rect(screen, (100, 100, 100), (size[0] // 2 - 165, size[1] // 2 - 200, 330, 400))
                    pygame.draw.rect(screen, (255, 255, 255), (size[0] // 2 - 165, size[1] // 2 - 200, 330, 400), 1)

                    font = pygame.font.Font(None, 70)
                    text = font.render("Пауза", 1, (20, 20, 20))
                    text_x = size[0] // 2 - text.get_width() // 2
                    text_y = 230
                    screen.blit(text, (text_x, text_y))

                    font = pygame.font.Font(None, 50)

                    for i in range(4):
                        pygame.draw.rect(screen,
                                         ((140, 200, 200), (200, 140, 200), (200, 200, 140), (140, 200, 140))[i],
                                         (310, 300 + i * 70, 280, 50))
                        pygame.draw.rect(screen, (0, 0, 0), (310, 300 + i * 70, 280, 50), 1)

                        text = font.render(["Продолжить", "Перезапустить", "Помощь", "Главное меню"][i], 1,
                                           (40, 40, 40))
                        text_x = size[0] // 2 - text.get_width() // 2
                        text_y = 308 + i * 70
                        screen.blit(text, (text_x, text_y))

            if pygame.mouse.get_focused():
                pos = pygame.mouse.get_pos()
                font = pygame.font.Font(None, 50)

                if 310 <= pos[0] <= 590 and 300 <= pos[1] <= 350:
                    pygame.draw.rect(screen, (140, 250, 250), (310, 300, 280, 50))
                    pygame.draw.rect(screen, (0, 0, 0), (310, 300, 280, 50), 1)
                    text = font.render("Продолжить", 1, (40, 40, 40))
                    text_x = size[0] // 2 - text.get_width() // 2
                    text_y = 308
                    screen.blit(text, (text_x, text_y))

                elif 310 <= pos[0] <= 590 and 370 <= pos[1] <= 420:
                    pygame.draw.rect(screen, (250, 140, 250), (310, 370, 280, 50))
                    pygame.draw.rect(screen, (0, 0, 0), (310, 370, 280, 50), 1)
                    text = font.render("Перезапустить", 1, (40, 40, 40))
                    text_x = size[0] // 2 - text.get_width() // 2
                    text_y = 378
                    screen.blit(text, (text_x, text_y))

                elif 310 <= pos[0] <= 590 and 440 <= pos[1] <= 490:
                    pygame.draw.rect(screen, (250, 250, 140), (310, 440, 280, 50))
                    pygame.draw.rect(screen, (0, 0, 0), (310, 440, 280, 50), 1)
                    text = font.render("Помощь", 1, (40, 40, 40))
                    text_x = size[0] // 2 - text.get_width() // 2
                    text_y = 448
                    screen.blit(text, (text_x, text_y))

                elif 310 <= pos[0] <= 590 and 510 <= pos[1] <= 560:
                    pygame.draw.rect(screen, (140, 250, 140), (310, 510, 280, 50))
                    pygame.draw.rect(screen, (0, 0, 0), (310, 510, 280, 50), 1)
                    text = font.render("Главное меню", 1, (40, 40, 40))
                    text_x = size[0] // 2 - text.get_width() // 2
                    text_y = 518
                    screen.blit(text, (text_x, text_y))

                if active_menu == "replay" or active_menu == "exit":
                    pygame.draw.rect(screen, (100, 100, 100), (size[0] // 2 - 240, size[1] // 2 - 130, 480, 260))
                    pygame.draw.rect(screen, (255, 255, 255), (size[0] // 2 - 240, size[1] // 2 - 130, 480, 260), 1)

                    for i in range(2):
                        pygame.draw.rect(screen, ((140, 200, 140), (200, 140, 200))[i], (310 + i * 180, 450, 100, 50))
                        pygame.draw.rect(screen, (0, 0, 0), (310 + i * 180, 450, 100, 50), 1)

                        text = font.render(["Да", "Нет"][i], 1, (40, 40, 40))
                        text_x = 335 + i * 175
                        text_y = 457 + 2 * i
                        screen.blit(text, (text_x, text_y))

                    if 310 <= pos[0] <= 410 and 450 <= pos[1] <= 500:
                        pygame.draw.rect(screen, (140, 250, 140), (310, 450, 100, 50))
                        pygame.draw.rect(screen, (0, 0, 0), (310, 450, 100, 50), 1)

                        text = font.render("Да", 1, (40, 40, 40))
                        text_x = 335
                        text_y = 457
                        screen.blit(text, (text_x, text_y))

                    elif 490 <= pos[0] <= 590 and 450 <= pos[1] <= 500:
                        pygame.draw.rect(screen, (250, 140, 250), (490, 450, 100, 50))
                        pygame.draw.rect(screen, (0, 0, 0), (490, 450, 100, 50), 1)

                        text = font.render("Нет", 1, (40, 40, 40))
                        text_x = 510
                        text_y = 459
                        screen.blit(text, (text_x, text_y))

            if active_menu == "replay":
                font = pygame.font.Font(None, 50)
                for i in range(3):
                    text = font.render(("Вы уверены, что хотите", "перезапустить игру? Ваш", "прогресс будет потерян")[i], 1, (20, 20, 20))
                    text_x = size[0] // 2 - text.get_width() // 2
                    text_y = 300 + 40 * i
                    screen.blit(text, (text_x, text_y))

            if active_menu == "exit":
                font = pygame.font.Font(None, 50)
                for i in range(3):
                    text = font.render(("Вы уверены, что хотите", "выйти из игры? Ваш", "прогресс будет потерян")[i], 1, (20, 20, 20))
                    text_x = size[0] // 2 - text.get_width() // 2
                    text_y = 300 + 40 * i
                    screen.blit(text, (text_x, text_y))

    if game:
        screen.fill((0, 0, 0))
        if flag:
            active = Block(None, None, next_image)
            next_image = next_block()
            flag = False
            if len([1 for i in all_blocks if pygame.sprite.collide_mask(active, i) is not None]) > 1:
                running = False
            else:
                score += 15
        for i in all_blocks:
                if i != active:
                    i.run_down()
        '''cropped = pygame.Surface((200, 200))
        cropped.blit(active.image, (0, 0), (0, 0, 150, int(str(active.image).split("(")[1].split("x")[1]) - 50))
        screen.blit(cropped, (0, 0))'''
        active.update()
        all_blocks.draw(screen)
        all_sprites.draw(screen)
        points_vis.draw(screen)
        lines.draw(screen)

        pygame.draw.rect(screen, (50, 50, 50), (width, 0, size[0] - width, height))
        pygame.draw.rect(screen, (100, 100, 100), (width + (size[0] - width) // 2 - 80, 100, 160, 160))
        pygame.draw.rect(screen, (100, 100, 100), (width + (size[0] - width) // 2 - 110, 360, 220, 50))
        pygame.draw.rect(screen, (100, 100, 100), (width + (size[0] - width) // 2 - 110, 510, 220, 50))
        pygame.draw.rect(screen, (100, 100, 100), (width + (size[0] - width) // 2 - 110, 660, 220, 50))
        pygame.draw.rect(screen, (255, 255, 255), (width + (size[0] - width) // 2 - 80, 100, 160, 160), 1)
        pygame.draw.rect(screen, (255, 255, 255), (width + (size[0] - width) // 2 - 110, 360, 220, 50), 1)
        pygame.draw.rect(screen, (255, 255, 255), (width + (size[0] - width) // 2 - 110, 510, 220, 50), 1)
        pygame.draw.rect(screen, (255, 255, 255), (width + (size[0] - width) // 2 - 110, 660, 220, 50), 1)

        mint = str(int(perf_counter() - time) // 60).rjust(2, "0")
        sec = str(int(perf_counter() - time) % 60).rjust(2, "0")
        mil = str(int((perf_counter() - time) * 100 % 100)).rjust(2, "0")

        time_for_pause = [mint, sec, mil]

        font = pygame.font.Font(None, 50)

        text = font.render(mint + ":" + sec + ":" + mil, 1, (255, 255, 255))
        text_x = 715
        text_y = 370
        screen.blit(text, (text_x, text_y))
        text = font.render(str(score), 1, (255, 255, 255))
        text_x = 854 - text.get_width()
        text_y = 520
        screen.blit(text, (text_x, text_y))

        font = pygame.font.Font(None, 70)
        text = font.render("Далее:", 1, (0, 0, 0))
        text_x = width + (size[0] - width) // 2 - 85
        text_y = 35
        screen.blit(text, (text_x, text_y))
        for i in range(3):
            text = font.render(["Время:", "Очки:", "Рекорд:"][i], 1, (0, 0, 0))
            text_x = width + (size[0] - width) // 2 - 100
            text_y = 300 + i * 150
            screen.blit(text, (text_x, text_y))

        next_min = pygame.transform.scale(next_image[0], (150, 150))
        screen.blit(next_min, (width + (size[0] - width) // 2 - 80 + 5, 105))

    clock.tick(fps)
    pygame.display.flip()
pygame.quit()