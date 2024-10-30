import pygame, settings
from nodes import create_nodes_list


def paint(nodes: list):
    screen.fill("#1F1F1F1F")

    for node in nodes:
        for receiver in nodes:
            if node.is_reachable(receiver):
                pygame.draw.line(
                    screen,
                    "#666666",
                    (node.pos_x, node.pos_y),
                    (receiver.pos_x, receiver.pos_y),
                )
    for node in nodes:
        if node.is_gate == True:
            pygame.draw.circle(screen, "#12c211", (node.pos_x, node.pos_y), 5)
        else:
            pygame.draw.circle(screen, "#dddddd", (node.pos_x, node.pos_y), 5)

    pygame.display.flip()


def move(node):
    if node.energy > 0:
        node.pos_x += node.move_x
        node.pos_y += node.move_y
        if node.pos_x <= 0 or node.pos_x >= settings.WIDTH:
            node.move_x *= -1
        if node.pos_y <= 0 or node.pos_y >= settings.HEIGHT:
            node.move_y *= -1


pygame.init()
nodes = create_nodes_list(settings.COUNT)

screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
clock = pygame.time.Clock()
running = True

while running:
    # Events check
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for node in nodes:
        move(node)

    paint(nodes)

    clock.tick(settings.FPS)

pygame.quit()
