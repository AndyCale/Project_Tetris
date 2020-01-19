import pygame
import os
import sys
from random import choice
import sqlite3


pygame.init()
size = width, height = 550, 550
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


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "Тетрис"]

    fon = pygame.transform.scale(load_image('pict.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 80)
    text_coord = 100
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 80
        intro_rect.top = text_coord
        intro_rect.x = 140
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(fps)


def draw_button(word, color):
    font = pygame.font.Font(None, 40)
    text = font.render(["Играть", "Рекорды", "Об игре", "Выйти"][word], 1, (0, 0, 0))
    text_x = width // 2 - text.get_width() // 2
    text_y = 195 + word * 65
    # text_w = text.get_width()
    text_h = text.get_height()
    pygame.draw.rect(screen, color,
                     (width // 2 - 95, text_y - 10, 190, text_h + 20))
    pygame.draw.rect(screen, (255, 255, 255), (width // 2 - 95, text_y - 10, 190, text_h + 20), 1)
    screen.blit(text, (text_x, text_y))


def menu():
    global screen, size, width, height

    screen.fill((0, 0, 0))

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

    # Имя игрока - Здрасте игрок
    ex = False
    pos = (0, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ex = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                ex = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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
                    game()
                elif 180 <= pos[0] <= 370 and 250 <= pos[1] <= 298:
                    print("Рекорды")
                elif 180 <= pos[0] <= 370 and 315 <= pos[1] <= 363:
                    rules()
                elif 180 <= pos[0] <= 370 and 380 <= pos[1] <= 428:
                    print(2)
                    ex = True

                size = width, height = 550, 550
                screen = pygame.display.set_mode(size)
                screen.fill((0, 0, 0))

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

            elif pygame.mouse.get_focused():
                pos = pygame.mouse.get_pos()

            if True:
                if ex:
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


def game():
    size = width, height = 615, 700
    screen = pygame.display.set_mode(size)

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
            if not pygame.sprite.collide_mask(self, down) and \
                    (not any([pygame.sprite.collide_mask(self, i) not in ((0, 0), None) for i in all_spr]) or
                     len([1 for i in all_spr if pygame.sprite.collide_mask(self, i) != None]) == 1):
                self.rect[1] += 1
                return False
            else:
                return True

        def run(self, s):
            if s == "l":
                if s == "l" and not pygame.sprite.collide_mask(self, l) and \
                        (not any([pygame.sprite.collide_mask(self, i) not in ((0, 0), None) for i in all_spr]) or
                         len([1 for i in all_spr if pygame.sprite.collide_mask(self, i) != None]) == 1):
                    self.rect[0] -= 50
                if pygame.sprite.collide_mask(self, l) != None or \
                        len([1 for i in all_spr if pygame.sprite.collide_mask(self, i) != None]) > 1:
                    self.rect[0] += 50
            else:
                if s == "r" and not pygame.sprite.collide_mask(self, r) and \
                        (not any([pygame.sprite.collide_mask(self, i) not in ((0, 0), None) for i in all_spr]) or
                         len([1 for i in all_spr if pygame.sprite.collide_mask(self, i) != None]) == 1):
                    self.rect[0] += 50
                if pygame.sprite.collide_mask(self, r) != None or \
                        len([1 for i in all_spr if pygame.sprite.collide_mask(self, i) != None]) > 1:
                    self.rect[0] -= 50

        def run_down(self):
            while not pygame.sprite.collide_mask(self, down) and \
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
    running = True

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
        flag = active.update()
        all_spr.draw(screen)
        all_sprites.draw(screen)
        clock.tick(fps)
        pygame.display.flip()


def rules():
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
    size_rul = 720, 830
    screen_rul = pygame.display.set_mode(size_rul)
    screen_rul.fill((40, 40, 40))
    running_rec = True
    con = sqlite3.connect("records.db")
    cur = con.cursor()
    result = cur.execute("SELECT * FROM records").fetchall()
    sorting = "time"
    if sorting == "time":
        result = sorted(result, key=lambda x: x[2])[::-1]
    else:
        result = sorted(result, key=lambda x: x[3])[::-1]
    print(result)

    while running_rec:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_rec = False
        sorting = "time"
        if sorting == "time":
            result = sorted(result, key=lambda x: x[2])[::-1]
        else:
            result = sorted(result, key=lambda x: x[3])[::-1]

        #for i in range

        for i in range(len(result)):
            font = pygame.font.Font(None, 60)
            text = font.render("Далее:", 1, (218, 241, 228))
            text_x = width + (size[0] - width) // 2 - 85
            text_y = 35
            screen.blit(text, (text_x, text_y))


        clock.tick(60)
        pygame.display.flip()
    con.commit()
    con.close()


#start_screen()
#menu()
records()
pygame.quit()
