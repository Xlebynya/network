import pygame, settings
from nodes import create_nodes_list, fill_packages


def paint(nodes: list):
    def clusterheadlines(nodes: list, clusterhead):
        if clusterhead == None:
            return
        for node in nodes:
            if node.energy > 0 and clusterhead.cluster == node.cluster:
                pygame.draw.line(
                    screen,
                    "#666666",
                    (node.pos_x, node.pos_y),
                    (clusterhead.pos_x, clusterhead.pos_y),
                )
            if node.is_gate:
                pygame.draw.line(
                            screen,
                            "#666666",
                            (node.pos_x, node.pos_y),
                            (clusterhead.pos_x, clusterhead.pos_y),
                        )

    screen.fill("#1F1F1F1F")
    pygame.draw.line(
        screen,
        "#cc2222",
        (0, settings.WIDTH / 2),
        (settings.HEIGHT, settings.WIDTH / 2),
    )
    pygame.draw.line(
        screen,
        "#cc2222",
        (settings.HEIGHT / 2, 0),
        (settings.HEIGHT / 2, settings.WIDTH),
    )

    clusterhead1, clusterhead2, clusterhead3, clusterhead4 = None, None, None, None 
    for node in nodes:
        if node.is_clusterhead:
            match (node.cluster):
                case 1:
                    clusterhead1 = node
                case 2:
                    clusterhead2 = node
                case 3:
                    clusterhead3 = node
                case 4:
                    clusterhead4 = node

    clusterheadlines(nodes, clusterhead1)
    clusterheadlines(nodes, clusterhead2)
    clusterheadlines(nodes, clusterhead3)
    clusterheadlines(nodes, clusterhead4)
    
    
    
    for node in nodes:
        if not node.is_gate and not node.is_clusterhead:
            if node.energy <= 0:
                pygame.draw.circle(screen, "#353535", (node.pos_x, node.pos_y), 3)
            else:
                pygame.draw.circle(screen, "#dddddd", (node.pos_x, node.pos_y), 5)
        elif node.is_gate:
            pygame.draw.circle(screen, "#12c212", (node.pos_x, node.pos_y), 7)
        elif node.is_clusterhead:
            pygame.draw.circle(screen, "#848430", (node.pos_x, node.pos_y), 5)

    pygame.display.flip()


def move(node):
    if node.energy > 0:
        node.pos_x += node.move_x
        node.pos_y += node.move_y
        if node.pos_x <= 0 or node.pos_x >= settings.WIDTH:
            node.move_x *= -1
        if node.pos_y <= 0 or node.pos_y >= settings.HEIGHT:
            node.move_y *= -1


def cluster_chosing(nodes: list):
    def clusterhead_choosing(cluster: list):
        if len(cluster) == 0:
            return
        clusterhead = cluster[0]
        for node in cluster:
            if node.energy > clusterhead.energy:
                clusterhead = node
        node.is_clusterhead = True

    cl1, cl2, cl3, cl4 = [], [], [], []
    for node in nodes:
        node.is_clusterhead = False
    for node in nodes:
        if node.energy > 0:
            if node.pos_x <= settings.WIDTH / 2:
                if node.pos_y <= settings.HEIGHT / 2:
                    node.cluster = 1
                    cl1.append(node)
                else:
                    node.cluster = 2
                    cl2.append(node)
            else:
                if node.pos_y <= settings.HEIGHT / 2:
                    node.cluster = 3
                    cl3.append(node)
                else:
                    node.cluster = 4
                    cl4.append(node)

    clusterhead_choosing(cl1)
    clusterhead_choosing(cl2)
    clusterhead_choosing(cl3)
    clusterhead_choosing(cl4)


pygame.init()
nodes = create_nodes_list(settings.COUNT)

fill_packages(nodes)

nodes[0].is_gate = True
nodes[0].receive_buffer.clear()
nodes[0].send_buffer.clear()
nodes[0].vision_radius = 0
nodes[0].move_x, nodes[0].move_y = (0, 0)
nodes[0].pos_x, nodes[0].pos_y = (settings.WIDTH / 2, settings.HEIGHT / 2)


screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
clock = pygame.time.Clock()
running = True

round = False
round_count = 0
start_ticks = pygame.time.get_ticks()

while running:
    # Events check
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and round == False:
                round_count += 1
                round = True
                for node in nodes:
                    node.send_to_all(nodes)
                    print(node)
                start_ticks = pygame.time.get_ticks()
    if round:
        cluster_chosing(nodes)
        for node in nodes:
            move(node)
        paint(nodes)
    seconds = (pygame.time.get_ticks() - start_ticks) / 1000
    if seconds > 1:
        round = False

    clock.tick(settings.FPS)

pygame.quit()
