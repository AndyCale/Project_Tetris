import pygame
import os
import sys
from random import choice


pygame.init()
size = width, height = 550, 550
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is None:
        colorkey = image.get_at((0, 0))
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
        clock.tick(FPS)


def menu():
    screen.fill((0, 0, 0))

    for let in range(len("TeTris")):
        font = pygame.font.Font(None, 90)
        text = font.render("TeTris"[let], 1, (choice(range(50, 255)), choice(range(50, 255)), choice(range(50, 255))))
        text_x = 95 + let * 70
        text_y = 60
        screen.blit(text, (text_x, text_y))

    color = []

    for word in range(len(["Играть", "Рекорды", "Об игре", "Выйти"])):
        font = pygame.font.Font(None, 40)
        text = font.render(["Играть", "Рекорды", "Об игре", "Выйти"][word], 1, (0, 0, 0))
        text_x = width // 2 - text.get_width() // 2
        text_y = 195 + word * 65
        text_w = text.get_width()
        text_h = text.get_height()
        color.append((choice(range(50, 255)), choice(range(50, 255)), choice(range(50, 255))))
        pygame.draw.rect(screen, color[-1],
                         (width // 2 - 95, text_y - 10, 190, text_h + 20))
        pygame.draw.rect(screen, (255, 255, 255), (width // 2 - 95, text_y - 10, 190, text_h + 20), 1)
        screen.blit(text, (text_x, text_y))
        print(width // 2 - 95, text_y - 10, 190, text_h + 20, text_x, text_y)

    # Имя игрока - Здрасте игрок

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if 180 <= pos[0] <= 370 and 185 <= pos[1] <= 233:
                    game()
                    print(1)
                elif 180 <= pos[0] <= 370 and 250 <= pos[1] <= 298:
                    print("Рекорды")
                elif 180 <= pos[0] <= 370 and 315 <= pos[1] <= 363:
                    print("Об игре")
                elif 180 <= pos[0] <= 370 and 380 <= pos[1] <= 428:
                    print(2)
                    terminate()
            elif pygame.mouse.get_focused():

                pos = pygame.mouse.get_pos()
                if 180 <= pos[0] <= 370 and 185 <= pos[1] <= 233:
                    font = pygame.font.Font(None, 40)
                    text = font.render("Играть", 1, (0, 0, 0))
                    pygame.draw.rect(screen, (color[0][0] + 30 if color[0][0] + 30 <= 255 else 255,
                                              color[0][1] + 30 if color[0][1] + 30 <= 255 else 255,
                                              color[0][2] + 30 if color[0][2] + 30 <= 255 else 255),
                                     (180, 185, 190, 48))
                    pygame.draw.rect(screen, (255, 255, 255), (180, 185, 190, 48), 1)
                    screen.blit(text, (229, 195))
                elif 180 <= pos[0] <= 370 and 250 <= pos[1] <= 298:
                    font = pygame.font.Font(None, 40)
                    text = font.render("Рекорды", 1, (0, 0, 0))
                    pygame.draw.rect(screen, (color[1][0] + 30 if color[1][0] + 30 <= 255 else 255,
                                              color[1][1] + 30 if color[1][1] + 30 <= 255 else 255,
                                              color[1][2] + 30 if color[1][2] + 30 <= 255 else 255),
                                     (180, 250, 190, 48))
                    pygame.draw.rect(screen, (255, 255, 255), (180, 250, 190, 48), 1)
                    screen.blit(text, (212, 260))
                elif 180 <= pos[0] <= 370 and 315 <= pos[1] <= 363:
                    font = pygame.font.Font(None, 40)
                    text = font.render("Об игре", 1, (0, 0, 0))
                    pygame.draw.rect(screen, (color[2][0] + 30 if color[2][0] + 30 <= 255 else 255,
                                              color[2][1] + 30 if color[2][1] + 30 <= 255 else 255,
                                              color[2][2] + 30 if color[2][2] + 30 <= 255 else 255),
                                     (180, 315, 190, 48))
                    pygame.draw.rect(screen, (255, 255, 255), (180, 315, 190, 48), 1)
                    screen.blit(text, (222, 325))
                elif 180 <= pos[0] <= 370 and 380 <= pos[1] <= 428:
                    font = pygame.font.Font(None, 40)
                    text = font.render("Выйти", 1, (0, 0, 0))
                    pygame.draw.rect(screen, (color[3][0] + 30 if color[3][0] + 30 <= 255 else 255,
                                              color[3][1] + 30 if color[3][1] + 30 <= 255 else 255,
                                              color[3][2] + 30 if color[3][2] + 30 <= 255 else 255),
                                     (180, 380, 190, 48))
                    pygame.draw.rect(screen, (255, 255, 255), (180, 380, 190, 48), 1)
                    screen.blit(text, (230, 390))
                else:
                    font = pygame.font.Font(None, 40)
                    text = font.render("Играть", 1, (0, 0, 0))
                    pygame.draw.rect(screen, color[0], (180, 185, 190, 48))
                    pygame.draw.rect(screen, (255, 255, 255), (180, 185, 190, 48), 1)
                    screen.blit(text, (229, 195))
                    font = pygame.font.Font(None, 40)
                    text = font.render("Рекорды", 1, (0, 0, 0))
                    pygame.draw.rect(screen, color[1], (180, 250, 190, 48))
                    pygame.draw.rect(screen, (255, 255, 255), (180, 250, 190, 48), 1)
                    screen.blit(text, (212, 260))
                    font = pygame.font.Font(None, 40)
                    text = font.render("Об игре", 1, (0, 0, 0))
                    pygame.draw.rect(screen, color[2], (180, 315, 190, 48))
                    pygame.draw.rect(screen, (255, 255, 255), (180, 315, 190, 48), 1)
                    screen.blit(text, (222, 325))
                    font = pygame.font.Font(None, 40)
                    text = font.render("Выйти", 1, (0, 0, 0))
                    pygame.draw.rect(screen, color[3], (180, 380, 190, 48))
                    pygame.draw.rect(screen, (255, 255, 255), (180, 380, 190, 48), 1)
                    screen.blit(text, (230, 390))

        pygame.display.flip()
        clock.tick(FPS)


def game():
    pass


FPS = 50
clock = pygame.time.Clock()
running = True
menu()


pygame.quit()