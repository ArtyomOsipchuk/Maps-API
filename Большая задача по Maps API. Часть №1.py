import os
import sys

import pygame
import requests


def get_click(coords):
    global l
    print(coords)
    x, y = coords
    if 0 < y < 25:
        if 450 < x < 500:
            l = 'map'
        if 500 < x < 550:
            l = 'sat'
        if 550 < x < 600:
            l = 'sat,skl'


def render():
    global spn, coords, map_file, l
    response = None
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={','.join(str(i) for i in coords)}&spn={','.join(str(i) for i in spn)}&l={l}"
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    # Запишем полученное изображение в файл.
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    screen = pygame.display.set_mode((600, 450))
    # Рисуем картинку, загружаемую из только что созданного файла.
    screen.blit(pygame.image.load(map_file), (0, 0))
    # Переключаем экран и ждем закрытия окна.
    pygame.draw.rect(screen, pygame.Color(0, 0, 0), ((450, 0), (600, 25)), 0)
    pygame.draw.rect(screen, pygame.Color(255, 255, 255), ((450, 0), (500, 25)), 1)
    pygame.draw.rect(screen, pygame.Color(255, 255, 255), ((500, 0), (550, 25)), 1)
    pygame.draw.rect(screen, pygame.Color(255, 255, 255), ((550, 0), (600, 25)), 1)
    pygame.font.init()
    font = pygame.font.Font(None, 25)
    text = font.render("map", 1, (255, 255, 255))
    screen.blit(text, (455, 5))
    font = pygame.font.Font(None, 25)
    text = font.render("sat", 1, (255, 255, 255))
    screen.blit(text, (510, 5))
    font = pygame.font.Font(None, 25)
    text = font.render("hyb", 1, (255, 255, 255))
    screen.blit(text, (555, 5))
    screen.convert_alpha()
    pygame.display.flip()


spn = (0.002, 0.002)
coords = (37.530887, 55.703118)
l = 'map'
render()
pygame.init()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_PAGEDOWN]:
            if spn[0] + 0.5 <= 19:
                spn = (spn[0] + 0.5, spn[1] + 0.5)
                render()
        if keys[pygame.K_PAGEUP]:
            if spn[0] - 0.5 >= 0.0017:
                spn = (spn[0] - 0.5, spn[1] - 0.5)
                render()
        if keys[pygame.K_RIGHT]:
            coords = (coords[0] + 0.5, coords[1])
            render()
        if keys[pygame.K_UP]:
            if coords[1] + 0.5 <= 84.836623:
                coords = (coords[0], coords[1] + 0.5)
                render()
        if keys[pygame.K_DOWN]:
            if coords[1] + 0.5 >= -85.052864:
                coords = (coords[0], coords[1] - 0.5)
                render()
        if keys[pygame.K_LEFT]:
            coords = (coords[0] - 0.5, coords[1])
            render()
        if event.type == pygame.MOUSEBUTTONUP:
            get_click(event.pos)
            render()
    pygame.display.flip()
pygame.quit()
os.remove(map_file)
