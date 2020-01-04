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
    font = pygame.font.Font(None, 50)
    for let in range(len("TeTris")):
        text = font.render("TeTris"[let], 1, (choice(range(50, 255)), choice(range(50, 255)), choice(range(50, 255))))
        text_x = 145 + let * 50
        text_y = 50
        screen.blit(text, (text_x, text_y))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                terminate()
                pos = event.pos
                game()
        pygame.display.flip()
        clock.tick(FPS)


def game():
    pass


FPS = 50
clock = pygame.time.Clock()
running = True
menu()


pygame.quit()