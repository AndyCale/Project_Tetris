import pygame
import os
import sys
from random import choice
import sqlite3
from PIL import Image
from time import perf_counter


pygame.init()
size = width, height = 550, 550
screen = pygame.display.set_mode(size)
pygame.display.set_caption('TeTris')
"""инизиализация Pygame"""

fps = 50
clock = pygame.time.Clock()


def load_image(name, pos=(0, 0), colors_key=None):
    # функция для загрузки картинок из папки data
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colors_key is None:
        colors_key = image.get_at(pos)
        image.set_colorkey(colors_key)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    """заставка перед меню игры"""
    fon = pygame.transform.scale(load_image('pict.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 120)
    text = font.render("TeTris", 1, (255, 255, 255))
    text_x = width // 2 - text.get_width() // 2
    text_y = 400
    screen.blit(text, (text_x, text_y))

    while True:
        """показывается, пока мы не нажмем любую клавишу мыши или клавиатуры"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(fps)


def draw_button(word, color):
    """функция рисования кнопок для меню"""
    font = pygame.font.Font(None, 40)
    text = font.render(["Играть", "Рекорды", "Об игре", "Выйти"][word], 1, (0, 0, 0))
    text_x = width // 2 - text.get_width() // 2
    text_y = 195 + word * 65
    text_h = text.get_height()
    pygame.draw.rect(screen, color,
                     (width // 2 - 95, text_y - 10, 190, text_h + 20))
    pygame.draw.rect(screen, (255, 255, 255), (width // 2 - 95, text_y - 10, 190, text_h + 20), 1)
    screen.blit(text, (text_x, text_y))


def menu():
    global screen, size, width, height
    """начальное меню игры"""

    screen.fill((0, 0, 0))
    fon = pygame.transform.scale(load_image('pict2.jpg'), (width, height))
    screen.blit(fon, (0, 0))

    color_let = []
    for let in range(len("TeTris")):
        font = pygame.font.Font(None, 90)
        color_let.append((choice(range(50, 255)), choice(range(50, 255)), choice(range(50, 255))))
        text = font.render("TeTris"[let], 1, color_let[let])
        text_x = 95 + let * 70
        text_y = 60
        screen.blit(text, (text_x, text_y))

    color = []

    for word in range(len(["Играть", "Рекорды", "Об игре", "Выйти"])):
        color.append((choice(range(50, 255)), choice(range(50, 255)), choice(range(50, 255))))
        draw_button(word, color[-1])

    ex = False
    pos = (0, 0)

    while True:
        """пока мы не выберем, что хотим увидеть, перед нами будет меню"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ex = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                ex = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                """если мы кликнули куда-то мышкой, то вот возможные реакции, в зависимости от того, куда мы кликнули"""
                pos = event.pos
                if ex:
                    if 200 <= pos[0] <= 250 and 290 <= pos[1] <= 320:
                        terminate()
                    elif 300 <= pos[0] <= 350 and 290 <= pos[1] <= 320:
                        ex = False
                        screen.fill((0, 0, 0))

                        for let in range(len("TeTris")):
                            font = pygame.font.Font(None, 90)
                            text = font.render("TeTris"[let], 1, (color_let[let]))
                            text_x = 95 + let * 70
                            text_y = 60
                            screen.blit(text, (text_x, text_y))

                        for word in range(len(["Играть", "Рекорды", "Об игре", "Выйти"])):
                            draw_button(word, color[word])

                elif 180 <= pos[0] <= 370 and 185 <= pos[1] <= 233:
                    re_pl = game_run()
                    while re_pl is not None:
                        re_pl = game_run()
                elif 180 <= pos[0] <= 370 and 250 <= pos[1] <= 298:
                    records()
                elif 180 <= pos[0] <= 370 and 315 <= pos[1] <= 363:
                    rules()
                elif 180 <= pos[0] <= 370 and 380 <= pos[1] <= 428:
                    ex = True

                size = width, height = 550, 550
                screen = pygame.display.set_mode(size)
                screen.fill((0, 0, 0))
                fon = pygame.transform.scale(load_image('pict2.jpg'), (width, height))
                screen.blit(fon, (0, 0))

                for let in range(len("TeTris")):
                    font = pygame.font.Font(None, 90)
                    text = font.render("TeTris"[let], 1, (color_let[let]))
                    text_x = 95 + let * 70
                    text_y = 60
                    screen.blit(text, (text_x, text_y))

                draw_button(0, (color[0][0] if color[0][0] <= 255 else 255,
                                color[0][1] if color[0][1] <= 255 else 255,
                                color[0][2] if color[0][2] <= 255 else 255))
                draw_button(1, (color[1][0] if color[1][0] <= 255 else 255,
                                color[1][1] if color[1][1] <= 255 else 255,
                                color[1][2] if color[1][2] <= 255 else 255))
                draw_button(2, (color[2][0] if color[2][0] <= 255 else 255,
                                color[2][1] if color[2][1] <= 255 else 255,
                                color[2][2] if color[2][2] <= 255 else 255))
                draw_button(3, (color[3][0] if color[3][0] <= 255 else 255,
                                color[3][1] if color[3][1] <= 255 else 255,
                                color[3][2] if color[3][2] <= 255 else 255))

                """после завершения игры/просмотра правил или рекордов у нас вновь прорисовывается меню"""

            elif pygame.mouse.get_focused():
                pos = pygame.mouse.get_pos()

            if ex:
                """если мы нажали, что хотим выйти, переда нами появляется уточнение, точно ли мы этого хотим,
                кнопочки становятся неного светлее, если навести на них мышкой"""
                pygame.draw.rect(screen, (50, 50, 50),
                                 (width // 2 - 155, height // 2 - 75, 310, 150))
                pygame.draw.rect(screen, (255, 255, 255), (width // 2 - 155, height // 2 - 75, 310, 150), 1)
                font = pygame.font.Font(None, 26)
                text = font.render("Вы уверены, что хотите выйти?", 1, (200, 200, 200))
                text_x = width // 2 - text.get_width() // 2
                text_y = height // 2 - text.get_height() // 2 - 30
                screen.blit(text, (text_x, text_y))
                if 200 <= pos[0] <= 250 and 290 <= pos[1] <= 320:
                    for i in range(2):
                        font = pygame.font.Font(None, 26)
                        text = font.render(["Да", "Нет"][i], 1, (0, 0, 0))
                        pygame.draw.rect(screen, (210, 210, 210) if i == 0 else (170, 170, 170),
                                         (200 + 100 * i, 290, 50, 30))
                        pygame.draw.rect(screen, (0, 0, 0), (200 + 100 * i, 290, 50, 30), 1)
                        screen.blit(text, (200 + 100 * i + 10, 290 + 5))
                elif 300 <= pos[0] <= 350 and 290 <= pos[1] <= 320:
                    for i in range(2):
                        font = pygame.font.Font(None, 26)
                        text = font.render(["Да", "Нет"][i], 1, (0, 0, 0))
                        pygame.draw.rect(screen, (210, 210, 210) if i == 1 else (170, 170, 170),
                                         (200 + 100 * i, 290, 50, 30))
                        pygame.draw.rect(screen, (0, 0, 0), (200 + 100 * i, 290, 50, 30), 1)
                        screen.blit(text, (200 + 100 * i + 10, 290 + 5))
                else:
                    for i in range(2):
                        font = pygame.font.Font(None, 26)
                        text = font.render(["Да", "Нет"][i], 1, (0, 0, 0))
                        pygame.draw.rect(screen, (170, 170, 170), (200 + 100 * i, 290, 50, 30))
                        pygame.draw.rect(screen, (0, 0, 0), (200 + 100 * i, 290, 50, 30), 1)
                        screen.blit(text, (200 + 100 * i + 10, 290 + 5))

                """кнопочки должны становится светлее, если навести на них мышку"""
            elif 180 <= pos[0] <= 370 and 185 <= pos[1] <= 233:
                draw_button(0, (color[0][0] + 40 if color[0][0] + 40 <= 255 else 255,
                                color[0][1] + 40 if color[0][1] + 40 <= 255 else 255,
                                color[0][2] + 40 if color[0][2] + 40 <= 255 else 255))
            elif 180 <= pos[0] <= 370 and 250 <= pos[1] <= 298:
                draw_button(1, (color[1][0] + 40 if color[1][0] + 40 <= 255 else 255,
                                color[1][1] + 40 if color[1][1] + 40 <= 255 else 255,
                                color[1][2] + 40 if color[1][2] + 40 <= 255 else 255))
            elif 180 <= pos[0] <= 370 and 315 <= pos[1] <= 363:
                draw_button(2, (color[2][0] + 40 if color[2][0] + 40 <= 255 else 255,
                                color[2][1] + 40 if color[2][1] + 40 <= 255 else 255,
                                color[2][2] + 40 if color[2][2] + 40 <= 255 else 255))
            elif 180 <= pos[0] <= 370 and 380 <= pos[1] <= 428:
                draw_button(3, (color[3][0] + 40 if color[3][0] + 40 <= 255 else 255,
                                color[3][1] + 40 if color[3][1] + 40 <= 255 else 255,
                                color[3][2] + 40 if color[3][2] + 40 <= 255 else 255))
            else:
                draw_button(0, (color[0][0] if color[0][0] <= 255 else 255,
                                color[0][1] if color[0][1] <= 255 else 255,
                                color[0][2] if color[0][2] <= 255 else 255))
                draw_button(1, (color[1][0] if color[1][0] <= 255 else 255,
                                color[1][1] if color[1][1] <= 255 else 255,
                                color[1][2] if color[1][2] <= 255 else 255))
                draw_button(2, (color[2][0] if color[2][0] <= 255 else 255,
                                color[2][1] if color[2][1] <= 255 else 255,
                                color[2][2] if color[2][2] <= 255 else 255))
                draw_button(3, (color[3][0] if color[3][0] <= 255 else 255,
                                color[3][1] if color[3][1] <= 255 else 255,
                                color[3][2] if color[3][2] <= 255 else 255))

        pygame.display.flip()
        clock.tick(fps)


def game_run():
    global size, width, height, screen
    """сама игра"""

    size = (900, 800)
    width, height = 615, 800
    screen = pygame.display.set_mode(size)

    running = True

    def load_image_game(name_img, color_key=None):
        """загрузка картинок, но с другими параметрами, не как в основной программе"""
        fullname = os.path.join('data', name_img)
        pict = pygame.image.load(fullname).convert()
        if color_key is None:
            color_key = (0, 0, 0, 255)
            pict.set_colorkey(color_key)
        else:
            pict = pict.convert_alpha()
        return pict

    def color_block(block, color):
        """покраска блока в случайно выбранный цвет - изначально они белые"""
        w, h = block.get_size()
        for x in range(w):
            for y in range(h):
                if block.get_at((x, y))[:3] != (0, 0, 0):
                    block.set_at((x, y), color)

    def next_block():
        """создает следующий блок, чтобы рисовать его в окошке "следующий блок"""
        img = load_image_game(choice(["block_l.png", "block_s.png", "block_t.png", "block_o.png", "block_i.png"]))
        color = pygame.Color(choice(["red", "blue", "orange", "yellow", "green", "pink", "purple"]))
        if choice([0, 1]):
            img = pygame.transform.flip(img, 1, 0)
        color_block(img, color)
        rect = pygame.Rect(256, 0, 150, img.get_size()[1])
        return img, rect

    class Block(pygame.sprite.Sprite):
        """класс для реализации блоков"""
        def __init__(self, img=None, rect=None, nxt=None):
            super().__init__(all_blocks)
            """создание блока - либо по параметрам, переданным из "следующего блока", либо после обрезки блока в 
            резултате сбора полной горизонтальной линии"""
            if img is None:
                self.image, self.rect = nxt[0], nxt[1]
            else:
                self.image = img
                self.rect = pygame.Rect(rect[0], rect[1], rect[2], rect[3])
            ct = self.cut()
            if ct is not None:
                self.image, self.rect = ct[0], pygame.Rect(ct[1])
                color_key = (0, 0, 0, 255)
                self.image.set_colorkey(color_key)
                self.mask = pygame.mask.from_surface(self.image)
            else:
                all_blocks.remove(self)

        def update(self):
            """обновление местоположения блока - падает, пока может"""
            if not pygame.sprite.collide_mask(self, down) and \
                    (not any([pygame.sprite.collide_mask(self, o) not in ((0, 0), None) for o in all_blocks]) or
                     len([1 for o in all_blocks if pygame.sprite.collide_mask(self, o) is not None]) == 1):
                self.rect[1] += speed
            else:
                """если падать некуда, он передает "эстафету" следующему - параметр True"""
                cells = []
                for o in pygame.sprite.spritecollide(self, points, False):
                    if pygame.sprite.collide_mask(self, o):
                        cells.append(pnt[o])
                        """новый упавший блок вписываем на доску"""
                return True, board.add(cells)

        def run(self, s):
            """блок передвигается вправо или влево, пока это возможно, если так нажал игрок"""
            if s == "l":
                if s == "l" and not pygame.sprite.collide_mask(self, left) and \
                        (not any([pygame.sprite.collide_mask(self, o) not in ((0, 0), None) for o in all_blocks]) or
                         len([1 for o in all_blocks if pygame.sprite.collide_mask(self, o) is not None]) == 1):
                    self.rect[0] -= 50
                if pygame.sprite.collide_mask(self, left) is not None or \
                        len([1 for o in all_blocks if pygame.sprite.collide_mask(self, o) is not None]) > 1:
                    self.rect[0] += 50
            else:
                if s == "r" and not pygame.sprite.collide_mask(self, r) and \
                        (not any([pygame.sprite.collide_mask(self, o) not in ((0, 0), None) for o in all_blocks]) or
                         len([1 for o in all_blocks if pygame.sprite.collide_mask(self, o) is not None]) == 1):
                    self.rect[0] += 50
                if pygame.sprite.collide_mask(self, r) is not None or \
                        len([1 for o in all_blocks if pygame.sprite.collide_mask(self, o) is not None]) > 1:
                    self.rect[0] -= 50

        def run_down(self):
            """блок пададает до конца вниз, пока это возможно"""
            while not pygame.sprite.collide_mask(self, down) and \
                    (len([1 for o in all_blocks if
                          pygame.sprite.collide_mask(self, o) is not None and self.rect[1] + self.rect[3] < o.rect[1] +
                          o.rect[3]]) == 0):
                self.rect[1] += 1

        def cut(self):
            """обрезание картинки от фона, чтобы при обрезки блока не было пустых частей"""
            w, h = self.image.get_size()
            q, e, u, t = 0, 0, 0, 0
            while all([self.image.get_at((q, y))[:3] == (0, 0, 0) for y in range(h)]) and q < w - 1:
                q += 1
            while all([self.image.get_at((x, e))[:3] == (0, 0, 0) for x in range(w)]) and e < h - 1:
                e += 1
            while all([self.image.get_at((w - u - 1, y))[:3] == (0, 0, 0) for y in range(h)]) and u < w - 1:
                u += 1
            while all([self.image.get_at((x, h - t - 1))[:3] == (0, 0, 0) for x in range(w)]) and t < h - 1:
                t += 1
            cropped = pygame.Surface((w - u - q, h - t - e))
            cropped.blit(self.image, (0, 0), (q, e, w - u - q, h - t - e))
            return cropped, (self.rect[0] + q, self.rect[1] + e, w - u - q, h - t - e)

    class Board:
        """класс поля(доски игровой) - наличие блока помечаем 1, отсутсвие - 0"""
        def __init__(self, wid, hei):
            self.size = [wid, hei]
            self.board = [[0] * wid for _ in range(hei)]

        def add(self, cells):
            """функция добавления блока"""
            num = 0
            for cell in cells:
                self.board[cell[0]][cell[1]] = 1
            for line in range(len(self.board)):
                """проверяем, не собралась ли горизонтальная полоса"""
                if all(self.board[line]):
                    num += 1
                    """количество собранный полос для начисления очков"""
                    self.delete_line(line)
                    """обрезаем блоки - удаляем собранную линию"""
                    board.board = [[0] * board.size[0] for _ in range(board.size[1])]
                    """перезаполняем доску - записываем, где теперь находятся блоки"""
                    for block in all_blocks:
                        cells = []
                        for o in pygame.sprite.spritecollide(block, points, False):
                            if pygame.sprite.collide_mask(block, o):
                                cells.append(pnt[o])
                        for cell in cells:
                            board.board[cell[0]][cell[1]] = 1
            return num * 100

        def delete_line(self, line):
            """функция обрезания блоков, создаем линию на месте собранной полосы, все блоки, пересекающиеся с ней
             должны быть удалены или обрезаны"""
            line_spr = Line(line * 50 + 25 + height % 50)
            for block in pygame.sprite.spritecollide(line_spr, all_blocks, False):
                if line_spr.rect[1] - block.rect[1] > 50 and block.rect[1] + block.rect[3] - line_spr.rect[1] > 50:
                    cropped_bl_1 = pygame.Surface((block.rect[2], (line_spr.rect[1] - block.rect[1]) // 50 * 50))
                    cropped_bl_1.blit(block.image, (0, 0),
                                      (0, 0, block.rect[2], (line_spr.rect[1] - block.rect[1]) // 50 * 50))
                    Block(cropped_bl_1,
                          (block.rect[0], block.rect[1], block.rect[2], (line_spr.rect[1] - block.rect[1]) // 50 * 50))
                    cropped_bl_2 = pygame.Surface(
                        (block.rect[2], (block.rect[1] + block.rect[3] - line_spr.rect[1]) // 50 * 50))
                    cropped_bl_2.blit(block.image, (0, 0),
                                      (0, (line_spr.rect[1] // 50 - block.rect[1] // 50) * 50, block.rect[2],
                                       (block.rect[1] + block.rect[3] - line_spr.rect[1]) // 50 * 50))
                    Block(cropped_bl_2, (block.rect[0], (line_spr.rect[1] // 50 + 1) * 50 - 5, block.rect[2],
                                         (block.rect[1] + block.rect[3] - line_spr.rect[1]) // 50 * 50))
                    all_blocks.remove(block)
                elif line_spr.rect[1] - block.rect[1] > 50:
                    cropped_bl = pygame.Surface((block.rect[2], (line_spr.rect[1] - block.rect[1]) // 50 * 50))
                    cropped_bl.blit(block.image, (0, 0),
                                    (0, 0, block.rect[2], (line_spr.rect[1] - block.rect[1]) // 50 * 50))
                    Block(cropped_bl,
                          (block.rect[0], block.rect[1], block.rect[2], (line_spr.rect[1] - block.rect[1]) // 50 * 50))
                    all_blocks.remove(block)
                elif block.rect[1] + block.rect[3] - line_spr.rect[1] > 50:
                    cropped_bl = pygame.Surface(
                        (block.rect[2], (block.rect[1] + block.rect[3] - line_spr.rect[1]) // 50 * 50))
                    cropped_bl.blit(block.image, (0, 0), (0, 50, block.rect[2],
                                                          (block.rect[1] + block.rect[3] -
                                                           line_spr.rect[1]) // 50 * 50))
                    Block(cropped_bl, (block.rect[0], (line_spr.rect[1] // 50 + 1) * 50 - 5, block.rect[2],
                                       (block.rect[1] + block.rect[3] - line_spr.rect[1]) // 50 * 50))
                    all_blocks.remove(block)
                else:
                    all_blocks.remove(block)
            for block in all_blocks:
                if block != active:
                    block.run_down()
                """все новые блоки опускаем по возможности вниз, удаляем линию"""
            lines.empty()

    class Border(pygame.sprite.Sprite):
        """границы, за которые не может выезать блок"""
        def __init__(self, group, im):
            super().__init__(group)
            self.image = load_image_game(im, -1)
            self.rect = self.image.get_rect()
            if group == horiz_bord:
                self.rect.bottom = height
            elif group == vert_bord_l:
                self.rect.left = 5
            else:
                self.rect.right = width - 5
            self.add(all_sprites)

    class Point(pygame.sprite.Sprite):
        """для записывания наличия блока в той или иной клетке поля, и для удобства игрока"""
        def __init__(self, x, y, group):
            super().__init__(group)
            self.image = pygame.Surface((2, 2), pygame.SRCALPHA, 32)
            pygame.draw.circle(self.image, pygame.Color("red"), (1, 1), 1)
            self.rect = pygame.Rect(x, y, 2, 2)

    class Line(pygame.sprite.Sprite):
        """класс линии, с помощью которой удаляем собранную полосу"""
        def __init__(self, line):
            super().__init__(lines)
            self.image = pygame.Surface([width, 1])
            self.rect = pygame.Rect(0, line, width, 1)

    def name(time_g, score_g):
        """функция для написания никнейма"""
        nickname = ""
        running_name = True
        shift = False
        k = 0

        while running_name:
            k += 1
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    running_name = False
                if ev.type == pygame.KEYDOWN:
                    """реакция на нажатые кнопки"""
                    if ev.key == pygame.K_ESCAPE:
                        nickname = None
                        running_name = False
                    elif ev.key == pygame.K_LSHIFT or ev.key == pygame.K_RSHIFT:
                        shift = True
                    elif ev.key == pygame.K_SPACE and len(nickname) < 17:
                        nickname += " "
                    elif pygame.key.name(ev.key) in "qwertyuiopasdfghjklzxcvbnm1234567890-" and len(nickname) < 17:
                        if pygame.key.name(ev.key) == "-" and shift:
                            nickname += "_"
                        elif pygame.key.name(ev.key) != "-":
                            nickname += pygame.key.name(ev.key).upper() if shift else pygame.key.name(ev.key)
                    elif ev.key == pygame.K_BACKSPACE:
                        nickname = nickname[:-1]
                    elif ev.key == pygame.K_RETURN:
                        running_name = False
                elif ev.type == pygame.KEYUP:
                    if ev.key == pygame.K_LSHIFT or ev.key == pygame.K_RSHIFT:
                        shift = False

            pygame.draw.rect(screen, (189, 177, 140), (size[0] // 2 - 250, size[1] // 2 - 150, 500, 300))
            pygame.draw.rect(screen, (255, 255, 255), (size[0] // 2 - 250, size[1] // 2 - 150, 500, 300), 1)

            pygame.draw.rect(screen, (171, 160, 125), (size[0] // 2 - 150, size[1] // 2 + 50, 300, 40))
            pygame.draw.rect(screen, (0, 0, 0), (size[0] // 2 - 150, size[1] // 2 + 50, 300, 40), 1)

            f = pygame.font.Font(None, 40)

            for g in range(5):
                "что написал и выиграл игрок"
                t = f.render(["Ваш результат:", "Время: " + ":".join(time_g), "Очки: " + str(score_g),
                              "Введите свой никнейм", nickname][g], 1, (20, 20, 20))
                t_x = size[0] // 2 - t.get_width() // 2
                t_y = size[1] // 2 - 130 + g * 40 if g < 3 else size[1] // 2 + 10 + (g - 3) * 46
                screen.blit(t, (t_x, t_y))

            if k % 50 <= 25:
                """где пишет игрок"""
                nick = f.render(nickname, 1, (20, 20, 20))
                t = f.render("|", 1, (20, 20, 20))
                t_x = size[0] // 2 + nick.get_width() // 2 + 1
                t_y = size[1] // 2 + 56
                screen.blit(t, (t_x, t_y))

            if k % 40 <= 20:
                """мигающие подсказки для игрока"""
                f = pygame.font.Font(None, 33)
                t = f.render("Нажмите Enter для продолжения", 1, (20, 20, 20))
                t_x = size[0] // 2 - t.get_width() // 2
                t_y = 512
                screen.blit(t, (t_x, t_y))
            else:
                f = pygame.font.Font(None, 31)
                t = f.render("Нажмите Enter для продолжения", 1, (20, 20, 20))
                t_x = size[0] // 2 - t.get_width() // 2
                t_y = 512
                screen.blit(t, (t_x, t_y))

            clock.tick(60)
            pygame.display.flip()
        return nickname

    image = Image.new("RGB", (width, 5), (0, 0, 0))
    pix = image.load()
    for i in range(width):
        for j in range(5):
            pix[i, j] = (0, 0, 0)
    image.save("data//horiz.png")
    image = Image.new("RGB", (1, height), (0, 0, 0))
    pix = image.load()
    for j in range(height):
        pix[0, j] = (0, 0, 0)
    image.save("data//vert.png")
    """создаем картинки границ, за которые блок не может выйти"""

    board = Board(width // 50, height // 50)
    all_sprites = pygame.sprite.Group()
    all_blocks = pygame.sprite.Group()
    vert_bord_l = pygame.sprite.Group()
    vert_bord_r = pygame.sprite.Group()
    horiz_bord = pygame.sprite.Group()
    points = pygame.sprite.Group()
    lines = pygame.sprite.Group()
    points_vis = pygame.sprite.Group()
    """все нужные нам группы спрайтов"""

    pnt = {}
    for i in range(width // 50):
        for j in range(height // 50):
            pnt[Point(i * 50 + 25 + width % 50, j * 50 + 25 + height % 50, points)] = (j, i)

    for i in range(width // 50 + 1):
        for j in range(height // 50 + 1):
            Point(i * 50 + 5, j * 50 - 5, points_vis)
    """создаем точки - сначала нужные для программы, потом для удобства игрока"""

    down = Border(horiz_bord, "horiz.png")
    left = Border(vert_bord_l, "vert.png")
    r = Border(vert_bord_r, "vert.png")
    """создаем границы"""

    flag = True
    active = 0
    speed = 1
    score = 0
    time = perf_counter()
    time_pause = 0
    next_image = next_block()
    game = True
    loss = False
    active_menu = ""
    time_for_pause = []
    pos_loss = (-size[0], 0)
    pict_loss = load_image_game("gameover.jpg", -1)
    con = sqlite3.connect("records.db")
    cur = con.cursor()
    """задаем все нужные переменные"""

    while running:
        """если мы уже создали блок, то можно отрабатывать команды"""
        if type(active) != int:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN) and loss:
                    running = pos_loss = (0, 0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if game:
                            game = False
                            time_pause = perf_counter()
                        elif not loss:
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
                            while pygame.sprite.collide_mask(active, down) is not None or \
                                    len([1 for i in all_blocks if
                                         pygame.sprite.collide_mask(active, i) is not None]) > 1:
                                active.rect[1] -= 1
                            while pygame.sprite.collide_mask(active, left) is not None:
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
                            while pygame.sprite.collide_mask(active, left) is not None:
                                active.rect[0] += 50
                            while pygame.sprite.collide_mask(active, r) is not None:
                                active.rect[0] -= 50

                if not game and not loss:
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
                            rules()
                            size = (900, 800)
                            width, height = 615, 800
                            screen = pygame.display.set_mode(size)

                            active_menu = ""

                            screen.fill((0, 0, 0))
                            all_blocks.draw(screen)
                            all_sprites.draw(screen)
                            points_vis.draw(screen)
                            lines.draw(screen)

                            pygame.draw.rect(screen, (50, 50, 50), (width, 0, size[0] - width, height))
                            pygame.draw.rect(screen, (100, 100, 100),
                                             (width + (size[0] - width) // 2 - 80, 100, 160, 160))
                            pygame.draw.rect(screen, (100, 100, 100),
                                             (width + (size[0] - width) // 2 - 110, 360, 220, 50))
                            pygame.draw.rect(screen, (100, 100, 100),
                                             (width + (size[0] - width) // 2 - 110, 510, 220, 50))
                            pygame.draw.rect(screen, (100, 100, 100),
                                             (width + (size[0] - width) // 2 - 110, 660, 220, 50))
                            pygame.draw.rect(screen, (255, 255, 255),
                                             (width + (size[0] - width) // 2 - 80, 100, 160, 160), 1)
                            pygame.draw.rect(screen, (255, 255, 255),
                                             (width + (size[0] - width) // 2 - 110, 360, 220, 50), 1)
                            pygame.draw.rect(screen, (255, 255, 255),
                                             (width + (size[0] - width) // 2 - 110, 510, 220, 50), 1)
                            pygame.draw.rect(screen, (255, 255, 255),
                                             (width + (size[0] - width) // 2 - 110, 660, 220, 50), 1)

                            font = pygame.font.Font(None, 50)

                            if len(time_for_pause) != 0:
                                mint, sec, mil = time_for_pause
                            else:
                                mint, sec, mil = "00", "00", "00"

                            result = cur.execute("SELECT * FROM records").fetchall()
                            if len(result) > 0:
                                result = int(float(sorted(result, key=lambda x: x[2])[-1][2]))
                                mint_rec = str(result // 60).rjust(2, "0")
                                sec_rec = str(result % 60).rjust(2, "0")
                                mil_rec = str(result * 100 % 100).rjust(2, "0")
                            else:
                                mint_rec = "00"
                                sec_rec = "00"
                                mil_rec = "00"

                            records_for_pause = [mint_rec, sec_rec, mil_rec]

                            text = font.render(mint + ":" + sec + ":" + mil, 1, (255, 255, 255))
                            text_x = 715
                            text_y = 370
                            screen.blit(text, (text_x, text_y))
                            text = font.render(str(score), 1, (255, 255, 255))
                            text_x = 854 - text.get_width()
                            text_y = 520
                            screen.blit(text, (text_x, text_y))
                            text = font.render(":".join(records_for_pause), 1, (255, 255, 255))
                            text_x = 854 - text.get_width()
                            text_y = 670
                            screen.blit(text, (text_x, text_y))

                            font = pygame.font.Font(None, 70)
                            text = font.render("Далее:", 1, (218, 241, 228))
                            text_x = width + (size[0] - width) // 2 - 85
                            text_y = 35
                            screen.blit(text, (text_x, text_y))

                            for i in range(3):
                                text = font.render(["Время:", "Очки:", "Рекорд:"][i], 1, (218, 241, 228))
                                text_x = width + (size[0] - width) // 2 - 100
                                text_y = 300 + i * 150
                                screen.blit(text, (text_x, text_y))

                            next_min = pygame.transform.scale(next_image[0], (150, 150))
                            screen.blit(next_min, (width + (size[0] - width) // 2 - 80 + 5, 105))

                            pygame.draw.rect(screen, (100, 100, 100),
                                             (size[0] // 2 - 165, size[1] // 2 - 200, 330, 400))
                            pygame.draw.rect(screen, (255, 255, 255),
                                             (size[0] // 2 - 165, size[1] // 2 - 200, 330, 400), 1)

                            font = pygame.font.Font(None, 70)
                            text = font.render("Пауза", 1, (20, 20, 20))
                            text_x = size[0] // 2 - text.get_width() // 2
                            text_y = 230
                            screen.blit(text, (text_x, text_y))

                            font = pygame.font.Font(None, 50)

                            for i in range(4):
                                pygame.draw.rect(screen,
                                                 ((140, 200, 200), (200, 140, 200), (200, 200, 140), (140, 200, 140))[
                                                     i],
                                                 (310, 300 + i * 70, 280, 50))
                                pygame.draw.rect(screen, (0, 0, 0), (310, 300 + i * 70, 280, 50), 1)

                                text = font.render(["Продолжить", "Перезапустить", "Помощь", "Главное меню"][i], 1,
                                                   (40, 40, 40))
                                text_x = size[0] // 2 - text.get_width() // 2
                                text_y = 308 + i * 70
                                screen.blit(text, (text_x, text_y))

                        elif 310 <= pos[0] <= 590 and 510 <= pos[1] <= 560 and active_menu == "":
                            active_menu = "exit"
                        elif 310 <= pos[0] <= 410 and 450 <= pos[1] <= 500 and active_menu in ["exit", "replay"]:
                            if active_menu == "exit":
                                running = False
                            else:
                                running = False
                                # как-то перезапускать игру
                        elif 490 <= pos[0] <= 590 and 450 <= pos[1] <= 500 and active_menu in ["exit", "replay"]:
                            active_menu = ""

                            screen.fill((0, 0, 0))
                            all_blocks.draw(screen)
                            all_sprites.draw(screen)
                            points_vis.draw(screen)
                            lines.draw(screen)

                            pygame.draw.rect(screen, (50, 50, 50), (width, 0, size[0] - width, height))
                            pygame.draw.rect(screen, (100, 100, 100),
                                             (width + (size[0] - width) // 2 - 80, 100, 160, 160))
                            pygame.draw.rect(screen, (100, 100, 100),
                                             (width + (size[0] - width) // 2 - 110, 360, 220, 50))
                            pygame.draw.rect(screen, (100, 100, 100),
                                             (width + (size[0] - width) // 2 - 110, 510, 220, 50))
                            pygame.draw.rect(screen, (100, 100, 100),
                                             (width + (size[0] - width) // 2 - 110, 660, 220, 50))
                            pygame.draw.rect(screen, (255, 255, 255),
                                             (width + (size[0] - width) // 2 - 80, 100, 160, 160), 1)
                            pygame.draw.rect(screen, (255, 255, 255),
                                             (width + (size[0] - width) // 2 - 110, 360, 220, 50), 1)
                            pygame.draw.rect(screen, (255, 255, 255),
                                             (width + (size[0] - width) // 2 - 110, 510, 220, 50), 1)
                            pygame.draw.rect(screen, (255, 255, 255),
                                             (width + (size[0] - width) // 2 - 110, 660, 220, 50), 1)

                            font = pygame.font.Font(None, 50)

                            if len(time_for_pause) != 0:
                                mint, sec, mil = time_for_pause
                            else:
                                mint, sec, mil = "00", "00", "00"

                            result = cur.execute("SELECT * FROM records").fetchall()
                            if len(result) > 0:
                                result = int(float(sorted(result, key=lambda x: x[2])[-1][2]))
                                mint_rec = str(result // 60).rjust(2, "0")
                                sec_rec = str(result % 60).rjust(2, "0")
                                mil_rec = str(result * 100 % 100).rjust(2, "0")
                            else:
                                mint_rec = "00"
                                sec_rec = "00"
                                mil_rec = "00"

                            records_for_pause = [mint_rec, sec_rec, mil_rec]

                            text = font.render(mint + ":" + sec + ":" + mil, 1, (255, 255, 255))
                            text_x = 715
                            text_y = 370
                            screen.blit(text, (text_x, text_y))
                            text = font.render(str(score), 1, (255, 255, 255))
                            text_x = 854 - text.get_width()
                            text_y = 520
                            screen.blit(text, (text_x, text_y))
                            text = font.render(":".join(records_for_pause), 1, (255, 255, 255))
                            text_x = 854 - text.get_width()
                            text_y = 670
                            screen.blit(text, (text_x, text_y))

                            font = pygame.font.Font(None, 70)
                            text = font.render("Далее:", 1, (218, 241, 228))
                            text_x = width + (size[0] - width) // 2 - 85
                            text_y = 35
                            screen.blit(text, (text_x, text_y))

                            for i in range(3):
                                text = font.render(["Время:", "Очки:", "Рекорд:"][i], 1, (218, 241, 228))
                                text_x = width + (size[0] - width) // 2 - 100
                                text_y = 300 + i * 150
                                screen.blit(text, (text_x, text_y))

                            next_min = pygame.transform.scale(next_image[0], (150, 150))
                            screen.blit(next_min, (width + (size[0] - width) // 2 - 80 + 5, 105))

                            pygame.draw.rect(screen, (100, 100, 100),
                                             (size[0] // 2 - 165, size[1] // 2 - 200, 330, 400))
                            pygame.draw.rect(screen, (255, 255, 255),
                                             (size[0] // 2 - 165, size[1] // 2 - 200, 330, 400), 1)

                            font = pygame.font.Font(None, 70)
                            text = font.render("Пауза", 1, (20, 20, 20))
                            text_x = size[0] // 2 - text.get_width() // 2
                            text_y = 230
                            screen.blit(text, (text_x, text_y))

                            font = pygame.font.Font(None, 50)

                            for i in range(4):
                                pygame.draw.rect(screen,
                                                 ((140, 200, 200), (200, 140, 200), (200, 200, 140), (140, 200, 140))[
                                                     i],
                                                 (310, 300 + i * 70, 280, 50))
                                pygame.draw.rect(screen, (0, 0, 0), (310, 300 + i * 70, 280, 50), 1)

                                text = font.render(["Продолжить", "Перезапустить", "Помощь", "Главное меню"][i], 1,
                                                   (40, 40, 40))
                                text_x = size[0] // 2 - text.get_width() // 2
                                text_y = 308 + i * 70
                                screen.blit(text, (text_x, text_y))

                    if pygame.mouse.get_focused():
                        "кнопочки подсвечиваются, когда на них наводишь мышку"
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
                            pygame.draw.rect(screen, (100, 100, 100),
                                             (size[0] // 2 - 240, size[1] // 2 - 130, 480, 260))
                            pygame.draw.rect(screen, (255, 255, 255),
                                             (size[0] // 2 - 240, size[1] // 2 - 130, 480, 260), 1)

                            for i in range(2):
                                pygame.draw.rect(screen, ((140, 200, 140), (200, 140, 200))[i],
                                                 (310 + i * 180, 450, 100, 50))
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
                            text = font.render(("Вы уверены, что хотите", "перезапустить игру? Ваш",
                                                "прогресс будет потерян")[i], 1, (20, 20, 20))
                            text_x = size[0] // 2 - text.get_width() // 2
                            text_y = 300 + 40 * i
                            screen.blit(text, (text_x, text_y))

                    if active_menu == "exit":
                        font = pygame.font.Font(None, 50)
                        for i in range(3):
                            text = font.render(
                                ("Вы уверены, что хотите", "выйти из игры? Ваш", "прогресс будет потерян")[i],
                                1, (20, 20, 20))
                            text_x = size[0] // 2 - text.get_width() // 2
                            text_y = 300 + 40 * i
                            screen.blit(text, (text_x, text_y))

        if game:
            """если не нажата пауза"""
            screen.fill((0, 0, 0))
            if flag:
                """если нет активного блока - он упал уже или еще не создан - создаем"""
                active = Block(None, None, next_image)
                next_image = next_block()
                flag = False
                if len([1 for i in all_blocks if pygame.sprite.collide_mask(active, i) is not None]) > 1:
                    game = False
                    loss = True
                    """если при появление блока сразу есть пересечение - игра окончена"""
                else:
                    score += 15
            for i in all_blocks:
                if i != active:
                    i.run_down()
            """блоки обновляются, на экране рисуется все, что только может"""
            flag_or_score = active.update()
            if flag_or_score is not None and flag_or_score[0]:
                flag = True
            if flag_or_score is not None:
                score += flag_or_score[1]
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

            """вычисляется время, рекорды, тоже отражается на экране"""
            mint = str(int(perf_counter() - time) // 60).rjust(2, "0")
            sec = str(int(perf_counter() - time) % 60).rjust(2, "0")
            mil = str(int((perf_counter() - time) * 100 % 100)).rjust(2, "0")

            time_for_pause = [mint, sec, mil]

            result = cur.execute("SELECT * FROM records").fetchall()
            if len(result) > 0:
                result = int(float(sorted(result, key=lambda x: x[2])[-1][2]))
                mint_rec = str(result // 60).rjust(2, "0")
                sec_rec = str(result % 60).rjust(2, "0")
                mil_rec = str(result * 100 % 100).rjust(2, "0")
            else:
                mint_rec = "00"
                sec_rec = "00"
                mil_rec = "00"

            font = pygame.font.Font(None, 50)

            text = font.render(mint + ":" + sec + ":" + mil, 1, (255, 255, 255))
            text_x = 715
            text_y = 370
            screen.blit(text, (text_x, text_y))
            text = font.render(str(score), 1, (255, 255, 255))
            text_x = 854 - text.get_width()
            text_y = 520
            screen.blit(text, (text_x, text_y))
            text = font.render(mint_rec + ":" + sec_rec + ":" + mil_rec, 1, (255, 255, 255))
            text_x = 854 - text.get_width()
            text_y = 670
            screen.blit(text, (text_x, text_y))

            font = pygame.font.Font(None, 70)
            text = font.render("Далее:", 1, (218, 241, 228))
            text_x = width + (size[0] - width) // 2 - 85
            text_y = 35
            screen.blit(text, (text_x, text_y))
            for i in range(3):
                text = font.render(["Время:", "Очки:", "Рекорд:"][i], 1, (218, 241, 228))
                text_x = width + (size[0] - width) // 2 - 100
                text_y = 300 + i * 150
                screen.blit(text, (text_x, text_y))

            next_min = pygame.transform.scale(next_image[0], (150, 150))
            screen.blit(next_min, (width + (size[0] - width) // 2 - 80 + 5, 105))
            if int(time_for_pause[0]) >= 3:
                speed = 3
            elif int(time_for_pause[0]) >= 1:
                speed = 2
        if loss:
            """при проигрыше у нас неспешно выезжает заставка, после этого у игрока запрашиваем никнейм"""
            screen.blit(pict_loss, pos_loss)
            if pos_loss[0] >= 0:
                pos_loss = (0, 0)
                nick_name = name(time_for_pause, score)
                if nick_name is not None:
                    cur.execute("INSERT INTO Records(Nickname, Time, Score) VALUES('{}', {},"
                                " {})".format(nick_name, perf_counter() - time, score))

                running = False
            else:
                """выезжание "game_over"""
                pos_loss = (pos_loss[0] + 5, 0)
        clock.tick(fps)
        pygame.display.flip()

    con.commit()
    con.close()

    if active_menu == "replay":
        """если игрок нажал "перерграть" игра начинается сначала"""
        return "replay"


def rules():
    """правила"""
    size_rul = 720, 830
    screen_rul = pygame.display.set_mode(size_rul)
    screen_rul.fill((40, 40, 40))
    running_rul = True

    while running_rul:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_rul = False

        font = pygame.font.Font(None, 60)
        for i in range(4):
            text = font.render(["От автора программки", "Управление", "Правила", "История игры"][i], 1, (200, 255, 255))
            text_x = size_rul[0] // 2 - text.get_width() // 2
            text_y = 40 + 180 * i
            screen.blit(text, (text_x, text_y))

        for i in range(3):
            font = pygame.font.Font(None, 30)
            text = font.render(['При нажатие стрелочек "вправо" и "влево" блок двигается',
                                'по горизонтали, при "вверх" и "вниз" - поворачивается,',
                                'при нажатие на пробел падает до конца вниз'][i], 1, (230, 230, 230))
            text_x = size_rul[0] // 2 - text.get_width() // 2
            text_y = 280 + 30 * i
            screen.blit(text, (text_x, text_y))

        for i in range(3):
            font = pygame.font.Font(None, 30)
            text = font.render(['Правила такие же, как и в стандартном тетрисе - продержись',
                                'как можно дольше, собирая блоки в полные горизонтальные',
                                'полоски и освобождая тем самым место для новых'][i], 1, (230, 230, 230))
            text_x = size_rul[0] // 2 - text.get_width() // 2
            text_y = 460 + 30 * i
            screen.blit(text, (text_x, text_y))

        for i in range(3):
            font = pygame.font.Font(None, 30)
            text = font.render(['Меня зовут Быковская Александра и я сделала эту кривую',
                                'версию тетриса для проекта в Яндекс.Лицей. Я старалась,',
                                'поэтому очень надеюсь, что вам понравится. Приятной игры!'][i], 1, (230, 230, 230))
            text_x = size_rul[0] // 2 - text.get_width() // 2
            text_y = 100 + 30 * i
            screen.blit(text, (text_x, text_y))

        for i in range(5):
            font = pygame.font.Font(None, 30)
            text = font.render(['Тетрис впервые был изобретен советским программистом Алексеем',
                                'Пажитновым и выпущен 6 июня 1984 года. Идею он взял с игры',
                                '"Пентамино". Изначальная версия игры написана на Паскале для',
                                'копмьютера Электроника-60, но комерческая была уже выпущена',
                                'американской компанией Spectrum Holobyte'][i], 1, (230, 230, 230))
            text_x = size_rul[0] // 2 - text.get_width() // 2
            text_y = 640 + 30 * i
            screen.blit(text, (text_x, text_y))

        clock.tick(60)
        pygame.display.flip()


def records():
    """рекорды"""
    size_rul = 720, 930
    screen_rul = pygame.display.set_mode(size_rul)
    screen_rul.fill((40, 40, 40))

    running_rec = True
    con = sqlite3.connect("records.db")
    cur = con.cursor()
    result = cur.execute("SELECT * FROM records").fetchall()
    sorting = "time"
    result = sorted(result, key=lambda x: x[2])[::-1]
    clear = False

    while running_rec:
        screen_rul.fill((40, 40, 40))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_rec = False
            if event.type == pygame.MOUSEBUTTONDOWN and width + (size[0] - width) // 2 -\
                    110 <= event.pos[0] <= width + (size[0] - width) // 2 + 110 and 20 <= event.pos[1] <= 70:
                """игрок может выбрать, как сортировать рекорды"""
                if sorting == "time":
                    sorting = "score"
                    result = sorted(result, key=lambda x: x[3])[::-1]
                else:
                    sorting = "time"
                    result = sorted(result, key=lambda x: x[2])[::-1]
            elif event.type == pygame.MOUSEBUTTONDOWN and size_rul[0] // 2 -\
                    140 <= event.pos[0] <= size_rul[0] // 2 + 140 and 870 <= event.pos[1] <= 910:
                clear = True
            elif clear and event.type == pygame.MOUSEBUTTONDOWN and size_rul[0] // \
                    2 - 115 <= event.pos[0] <= size_rul[0] // 2 - 25 and size_rul[1] // \
                    2 + 27 <= event.pos[1] <= size_rul[1] // 2 + 77:
                con = sqlite3.connect("records.db")
                cur = con.cursor()

                cur.execute("DELETE from Records")
                result = cur.execute("SELECT * FROM records").fetchall()

                clear = False

            elif clear and event.type == pygame.MOUSEBUTTONDOWN and size_rul[0] //\
                    2 + 25 <= event.pos[0] <= size_rul[0] // 2 + 115 and size_rul[1] //\
                    2 + 27 <= event.pos[1] <= size_rul[1] // 2 + 77:
                clear = False

        number = 20 if len(result) > 20 else len(result)
        """показывается 20 лучших рекордов"""

        font = pygame.font.Font(None, 40)
        text = font.render("Сортировать по:", 1, (230, 230, 230))
        text_x = 30
        text_y = 30
        screen.blit(text, (text_x, text_y))

        pygame.draw.rect(screen, (231, 209, 187), (width + (size[0] - width) // 2 - 110, 20, 220, 50))
        pygame.draw.rect(screen, (255, 255, 255), (width + (size[0] - width) // 2 - 110, 20, 220, 50), 1)

        pygame.draw.rect(screen, (231, 209, 187), (size_rul[0] // 2 - 140, 870, 280, 40))
        pygame.draw.rect(screen, (255, 255, 255), (size_rul[0] // 2 - 140, 870, 280, 40), 1)

        text = font.render("Времени" if sorting == "time" else "Очкам", 1, (30, 30, 30))
        text_x = 550 - text.get_width() // 2
        text_y = 35
        screen.blit(text, (text_x, text_y))

        font = pygame.font.Font(None, 30)

        text = font.render("Стереть все рекорды", 1, (30, 30, 30))
        text_x = size_rul[0] // 2 - text.get_width() // 2
        text_y = 882
        screen.blit(text, (text_x, text_y))

        for i in range(number):
            for j in range(4):
                t = str(result[i][j])
                if j == 2:
                    t = int(float(t))
                    mint = str(t // 60).rjust(2, "0")
                    sec = str(t % 60).rjust(2, "0")
                    mil = str(t * 100 % 100).rjust(2, "0")
                    t = mint + ":" + sec + ":" + mil
                text = font.render(str(i + 1) if j == 0 else t, 1, (230, 230, 230))
                if j == 0:
                    text_x = 20
                if j == 1:
                    text_x = 70
                if j == 2:
                    text_x = 360
                if j == 3:
                    text_x = 550
                text_y = 155 + i * 35
                screen.blit(text, (text_x, text_y))

        font = pygame.font.Font(None, 40)
        for j in range(3):
            text = font.render(["Никнейм", "Время", "Очки"][j], 1, (230, 230, 230))
            if j == 0:
                text_x = 70
            if j == 1:
                text_x = 360
            if j == 2:
                text_x = 550
            text_y = 100
            screen.blit(text, (text_x, text_y))
            pygame.draw.line(screen, (255, 255, 255), (text_x - 10, 105), (text_x - 10, 840), 1)
        pygame.draw.line(screen, (255, 255, 255), (17, 135), (700, 135), 1)

        if clear:
            pygame.draw.rect(screen, (231, 209, 187), (size_rul[0] // 2 - 180, size_rul[1] // 2 - 100, 360, 200))
            pygame.draw.rect(screen, (255, 255, 255), (size_rul[0] // 2 - 180, size_rul[1] // 2 - 100, 360, 200), 1)
            pygame.draw.rect(screen, (150, 150, 150), (size_rul[0] // 2 - 115, size_rul[1] // 2 + 27, 90, 50))
            pygame.draw.rect(screen, (255, 255, 255), (size_rul[0] // 2 - 115, size_rul[1] // 2 + 27, 90, 50), 1)
            pygame.draw.rect(screen, (150, 150, 150), (size_rul[0] // 2 + 25, size_rul[1] // 2 + 27, 90, 50))
            pygame.draw.rect(screen, (255, 255, 255), (size_rul[0] // 2 + 25, size_rul[1] // 2 + 27, 90, 50), 1)

            font = pygame.font.Font(None, 40)
            for p in range(2):
                """стирание рекордов"""
                text = font.render(["Вы уверены, что хотите", "стереть все рекорды?"][p], 1, (30, 30, 30))
                text_x = size_rul[0] // 2 - text.get_width() // 2
                text_y = size_rul[1] // 2 - 80 + p * 40
                screen.blit(text, (text_x, text_y))

            for p in range(2):
                text = font.render(["Да", "Нет"][p], 1, (30, 30, 30))
                text_x = size_rul[0] // 2 - 90 + p * 135
                text_y = size_rul[1] // 2 + 40
                screen.blit(text, (text_x, text_y))

        clock.tick(60)
        pygame.display.flip()

    con.commit()
    con.close()


start_screen()
menu()
pygame.quit()
