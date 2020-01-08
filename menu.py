import pygame
import os
import sys
from random import choice


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
                    print(1)
                    size = width, height = 550, 550
                    screen = pygame.display.set_mode(size)
                    screen.fill((0, 0, 0))

                    for let in range(len("TeTris")):
                        font = pygame.font.Font(None, 90)
                        text = font.render("TeTris"[let], 1, (color_let[let]))
                        text_x = 95 + let * 70
                        text_y = 60
                        screen.blit(text, (text_x, text_y))

                elif 180 <= pos[0] <= 370 and 250 <= pos[1] <= 298:
                    print("Рекорды")
                elif 180 <= pos[0] <= 370 and 315 <= pos[1] <= 363:
                    print("Об игре")
                elif 180 <= pos[0] <= 370 and 380 <= pos[1] <= 428:
                    print(2)
                    ex = True

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


menu()
pygame.quit()
