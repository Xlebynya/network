import pygame, settings
from nodes import create_nodes_list, fill_packages


def paint(nodes: list):
    def drawline(node, receiver):
        pygame.draw.line(
            screen,
            "#666666",
            (node.pos_x, node.pos_y),
            (receiver.pos_x, receiver.pos_y),
        )

    screen.fill("#1F1F1F1F")

    for node in nodes:
        if node.energy == 0:
                continue
        if (
            node.pos_x <= settings.WIDTH / 4 * 3
            and node.pos_x >= settings.WIDTH / 4
            and node.pos_y <= settings.HEIGHT / 4 * 3
            and node.pos_y >= settings.HEIGHT / 4
        ):
            for receiver in nodes:
                if receiver.order == 0:
                    drawline(node, receiver)

        else:
            
            node.vision_radius = 0
            found = False
            while found == False:
                node.vision_radius += 1
                for receiver in nodes:
                    if receiver.order == 1 and node.is_reachable(receiver):
                        drawline(node, receiver)
                        found = True

    for node in nodes:
        if node.order == 0:
            pygame.draw.circle(screen, "#12c212", (node.pos_x, node.pos_y), 5)
        if node.order == 1:
            pygame.draw.circle(screen, "#c21212", (node.pos_x, node.pos_y), 5)
        if node.order == 3:
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
nodes[0].to_gate()
nodes[1].to_router(1)
nodes[2].to_router(2)
nodes[3].to_router(3)
nodes[4].to_router(4)


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
