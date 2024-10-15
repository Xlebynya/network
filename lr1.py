import pygame
import settings
from nodes import Node
import numpy

pygame.init()
screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))


nodes_arr = [
    Node(
        numpy.random.randint(1, settings.WIDTH),
        numpy.random.randint(1, settings.HEIGHT),
        move=(
            numpy.random.uniform(-1, 1),
            numpy.random.uniform(-1, 1),
        ),
    )
    for i in range(settings.COUNT)
]

clock = pygame.time.Clock()

# Цикл игры
running = True

round = False
start_ticks = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        # проверить закрытие окна
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and round == False:
                round = True
                start_ticks = pygame.time.get_ticks()


    screen.fill("#1F1F1F1F")
    clock.tick(settings.FPS)

    # ЛАБА
    if round:
        # движения
        for node in nodes_arr:
            node.x += node.movex
            node.y += node.movey
            if node.x >= settings.WIDTH or node.x <= 0:
                node.movex *= -1
            if node.y >= settings.HEIGHT or node.y <= 0:
                node.movey *= -1
            for i in nodes_arr:
                # если в радиусе
                if (i.x - node.x) ** 2 + (i.y - node.y) ** 2 <= node.radius**2:
                    # Отправка соседу

                    pygame.draw.line(
                        screen,
                        (255, 255, 255, 10),
                        (i.x, i.y),
                        (node.x, node.y),
                        width=1,
                    )
            pygame.draw.circle(screen, "#dddddd", (node.x, node.y), 6)
        pygame.display.flip()
    seconds = (pygame.time.get_ticks() - start_ticks) / 1000
    if seconds > 1:
        round = False

    # КОНЕЦ ЛАБЫ

    # после отрисовки всего, переворачиваем экран

# Конец
pygame.quit()
