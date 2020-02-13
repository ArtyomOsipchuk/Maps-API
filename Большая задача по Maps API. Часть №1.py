import os
import sys

import pygame
import requests


def render():
    global spn, coords, map_file
    response = None
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={','.join(str(i) for i in coords)}&spn={','.join(str(i) for i in spn)}&l=map"
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
    pygame.display.flip()


spn = (0.002, 0.002)
coords = (37.530887, 55.703118)
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
            coords = (coords[0], coords[1] + 0.5)
            render()
        if keys[pygame.K_DOWN]:
            coords = (coords[0], coords[1] - 0.5)
            render()
        if keys[pygame.K_LEFT]:
            coords = (coords[0] - 0.5, coords[1])
            render()
    pygame.display.flip()
pygame.quit()
os.remove(map_file)
