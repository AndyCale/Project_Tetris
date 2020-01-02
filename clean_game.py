import pygame
import os


pygame.init()
size = width, height = 490, 500
screen = pygame.display.set_mode(size)

fps = 60
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


class Mountain(pygame.sprite.Sprite):
    image = load_image("horiz.png", -1, -1)

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Mountain.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        #self.mask = pygame.mask.from_surface(self.image)
        # располагаем горы внизу
        self.rect.bottom = height - 30


class Landing(pygame.sprite.Sprite):
    image = load_image("block_l.png", (60, 0))

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = Landing.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        # если ещё в небе
        #self.rect = self.rect.move(0, 1)
        if not pygame.sprite.collide_mask(self, mountain):
            self.rect = self.rect.move(0, 1)


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2, group):
        super().__init__(group)
        self.image = pygame.Surface([x2 - x1 + 1, y2 - y1 + 1])
        self.rect = pygame.Rect(x1, y1, x2 - x1 + 1, y2 - y1 + 1)


all_sprites = pygame.sprite.Group()
mountain = Mountain()

vert_bord_l = pygame.sprite.Group()
vert_bord_r = pygame.sprite.Group()
horiz_bord = pygame.sprite.Group()

down = Border(5, height - 5, width - 5, height - 5, horiz_bord)
l = Border(5, 5, 5, height - 5, vert_bord_l)
r = Border(width - 5, 5, width - 5, height - 5, vert_bord_r)

while running:
    screen.fill((255, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            Landing(event.pos)
    all_sprites.update()
    all_sprites.draw(screen)
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()