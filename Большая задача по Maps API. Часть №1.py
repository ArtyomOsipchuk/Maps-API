import os
import sys
import requests
import pygame
import requests
import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QMainWindow, QInputDialog, QLineEdit, \
    QFileDialog, QTextEdit


class Searcher(QMainWindow):
    def __init__(self):
        global coordspt
        app = QApplication(sys.argv)
        self.address = ''
        super().__init__()
        self.setGeometry(300, 300, 300, 300)
        self.show()
        i, okBtnPressed = QInputDialog.getText(self, "Поиск",
                                               "Введите место")
        if okBtnPressed:
            self.address = i
        else:
            self.address = coordspt


def get_click(coo):
    global l, address, coords, coordspt
    print(coo)
    x, y = coo
    if 0 < y < 25:
        if 450 < x < 500:
            l = 'map'
        if 500 < x < 550:
            l = 'sat'
        if 550 < x < 600:
            l = 'sat,skl'
    elif 0 < y < 30 and 0 < x < 60:
        a = Searcher()
        address = a.address
        geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={address}&format=json"
        response = requests.get(geocoder_request)
        if response:
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            toponym_coodrinates = toponym["Point"]["pos"]
            a, b = toponym_coodrinates.split()
            coords = (float(a), float(b))
            coordspt = (float(a), float(b))
        else:
            print("Ошибка выполнения запроса:")
            print(geocoder_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
    elif 40 < y < 70 and 0 < x < 60:
        coordspt = 0


def render():
    global spn, coords, map_file, l, coordspt
    api_server = 'http://static-maps.yandex.ru/1.x/?'
    params = {
        "ll": ','.join(str(i) for i in coords),
        "spn": ','.join(str(i) for i in spn),
        "l": l
    }
    if coordspt:
        params['pt'] = ','.join(str(i) for i in coordspt)
    response = requests.get(api_server, params=params)
    # map_request = f"http://static-maps.yandex.ru/1.x/?ll={','.join(str(i) for i in coords)}&pt={','.join(str(i) for i in coordspt)}&spn={','.join(str(i) for i in spn)}&l={l}"
    # response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load(map_file), (0, 0))
    # смена режимов
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
    # поиск
    pygame.draw.rect(screen, pygame.Color(0, 0, 0), ((0, 0), (60, 30)), 0)
    pygame.draw.rect(screen, pygame.Color(255, 255, 255), ((0, 0), (60, 30)), 1)
    font = pygame.font.Font(None, 25)
    text = font.render("search", 1, (255, 255, 255))
    screen.blit(text, (2, 9))
    # сброс
    pygame.draw.rect(screen, pygame.Color(0, 0, 0), ((0, 40), (60, 45)), 0)
    pygame.draw.rect(screen, pygame.Color(255, 255, 255), ((0, 40), (60, 45)), 1)
    font = pygame.font.Font(None, 25)
    text = font.render("reset", 1, (255, 255, 255))
    screen.blit(text, (2, 42))
    pygame.display.flip()


spn = (0.002, 0.002)
coords = (37.530887, 55.703118)
coordspt = (37.530887, 55.703118)
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
