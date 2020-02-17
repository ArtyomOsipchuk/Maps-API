import os
import sys

import pygame
import requests

api_server = "http://static-maps.yandex.ru/1.x/"

lon = "37.530887"
lat = "55.703118"
delta = "0.002"

params = {
    "ll": ",".join([lon, lat]),
    "spn": ",".join([delta, delta]),
    "l": "map"
}
response = requests.get(api_server, params=params)

if not response:
    print("Ошибка выполнения запроса:")
    print(map_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

if params = { 
    "ll": ",".join([lon, lat]),
    "spn": ",".join([delta, delta]),
    "l": "map"}:
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
if params = {
    "ll": ",".join([lon, lat]),
    "spn": ",".join([delta, delta]),
    "l": "sat"}:
        sat_file = "sat.jpg"
        with open(sat_file, "wb") as file:
            file.write(response.content)
if params = {
    "ll": ",".join([lon, lat]),
    "spn": ",".join([delta, delta]),
    "l": "sat, skl"}:
        sat_skl_file = "sat.jpg", "skl.png"
        with open(sat_skl_file, "wb") as file:
            file.write(response.content)

pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()

os.remove(map_file) 