import pygame
import requests
import sys
import os


def show_map(z, ll_spn=None, map_type="map", add_params=None):
    if ll_spn:
        map_request = f"http://static-maps.yandex.ru/1.x/?{ll_spn}&l={map_type}&z={z}"
    else:
        map_request = f"http://static-maps.yandex.ru/1.x/?l={map_type}&z={z}"

    if add_params:
        map_request += "&" + add_params
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    # Запишем полученное изображение в файл.
    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)
    return map_file
    # Инициализируем pygame


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    running = True
    clock = pygame.time.Clock()

    update = True
    z = 8
    lat = 37.6139
    lon = 55.7536
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                update = True
                if event.key == pygame.K_PAGEUP:
                    z += 1
                elif event.key == pygame.K_PAGEDOWN:
                    z -= 1
                if event.key == pygame.K_LEFT:
                    lat -= 1 / 2 ** (z - 6)
                if event.key == pygame.K_UP:
                    lon += 1 / 2 ** (z - 6)
                if event.key == pygame.K_DOWN:
                    lon -= 1 / 2 ** (z - 6)
                if event.key == pygame.K_RIGHT:
                    lat += 1 / 2 ** (z - 6)
        if update:
            update = False
            if z > 21:
                z = 21
            if z < 1:
                z = 1
            if lon < -85:
                lon = -85
            if lon > 85:
                lon = 85

            map_file = show_map(z, f"ll={lat},{lon}")
            screen.blit(pygame.image.load(map_file), (0, 0))
        clock.tick(60)
        pygame.display.flip()

    pygame.quit()
    os.remove(map_file)
