import pygame, settings
from nodes import create_nodes_list, fill_packages


def paint(nodes: list):
    screen.fill("#1F1F1F1F")

    for node in nodes:
        for receiver in nodes:
            if node.energy > 0 and receiver.energy > 0:
                if node.is_reachable(receiver):
                    pygame.draw.line(
                        screen,
                        "#666666",
                        (node.pos_x, node.pos_y),
                        (receiver.pos_x, receiver.pos_y),
                    )
    for node in nodes:
        if node.is_gate:
            pygame.draw.circle(screen, "#12c211", (node.pos_x, node.pos_y), 5)
        else:
            if node.energy <= 0:
                pygame.draw.circle(screen, "#353535", (node.pos_x, node.pos_y), 5)
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

fill_packages(nodes, 3)

nodes[0].is_gate = True
nodes[0].receive_buffer.clear()
nodes[0].send_buffer.clear()
nodes[0].vision_radius = 0
nodes[0].move_x, nodes[0].move_y = (0, 0)
nodes[0].pos_x, nodes[0].pos_y = (settings.WIDTH/2, settings.HEIGHT/2)


screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
clock = pygame.time.Clock()
running = True

round = False
start_ticks = pygame.time.get_ticks()

while running:
    # Events check
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and round == False:
                round = True
                for node in nodes:
                    node.send_to_all(nodes)
                    print(node)
                start_ticks = pygame.time.get_ticks()
    if round:
        for node in nodes:
            move(node)
        paint(nodes)
    seconds = (pygame.time.get_ticks() - start_ticks) / 1000
    if seconds > 1:
        round = False

    clock.tick(settings.FPS)

pygame.quit()
