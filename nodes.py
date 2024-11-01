import settings
import random


class Node:
    def __init__(
        self,
        coordinates: tuple[int],
        move: tuple[int],
        vision_radius: int = settings.VISION_RADIUS,
        energy=100,
        id: int = 0,
    ) -> None:
        self.id = id
        self.pos_x, self.pos_y = coordinates
        self.move_x, self.move_y = move
        self.energy = energy
        self.vision_radius = int(vision_radius * self.energy / 100)
        self.send_buffer: list = list()  # queue
        self.receive_buffer: set = set()  # set
        self.order = 3

    def __str__(self) -> str:
        return f"Node {self.id}: \
            \n (x, y): ({self.pos_x}, {self.pos_y})\
            \n energy: {self.energy}\
            \n receive_buff: {self.receive_buffer}\
            \n send_buff: {self.send_buffer}\n"

    def to_gate(self):
        self.order = 0
        self.receive_buffer.clear()
        self.send_buffer.clear()
        self.vision_radius = 0
        self.move_x, self.move_y = (0, 0)
        self.pos_x, self.pos_y = (settings.WIDTH / 2, settings.HEIGHT / 2)

    def to_router(self, quarter):
        self.order = 1
        self.vision_radius = 0
        self.move_x, self.move_y = (0, 0)
        self.pos_x, self.pos_y = (settings.WIDTH / 4, settings.HEIGHT / 4)
        if quarter == 2 or quarter == 4:
            self.pos_y = settings.HEIGHT - self.pos_y
        if quarter == 3 or quarter == 4:
            self.pos_x = settings.WIDTH - self.pos_x

    def get_packages(self, msgs: list[str]) -> None:
        """Add packages from nowhere"""
        for msg in msgs:
            self.send_buffer.append(msg)
            self.receive_buffer.add(msg)

    def is_reachable(self, receiver: "Node") -> bool:
        """Checks if the receiver is reachable"""
        return (receiver.pos_x - self.pos_x) ** 2 + (
            receiver.pos_y - self.pos_y
        ) ** 2 <= self.vision_radius**2

    def send(self, receiver: "Node") -> None:
        """Sends package to one receiver"""
        if self.send_buffer == [] or self.energy <= 0:
            return
        if self.send_buffer[0] not in receiver.receive_buffer:
            receiver.send_buffer.append(self.send_buffer[0])
            receiver.receive_buffer.add(self.send_buffer[0])
        self.send_buffer.pop(0)
        

    def send_to_all(self, nodes: list["Node"]) -> None:
        """Sends package to all than delete it and downgrades energy"""
        if self.order == 0:
            self.send_buffer.clear()
        if self.order == 1:
            for receiver in nodes:
                if receiver.order == 0:
                    self.send(receiver)

        if self.order == 3:
            if (
                self.pos_x <= settings.WIDTH / 4 * 3
                and self.pos_x >= settings.WIDTH / 4
                and self.pos_y <= settings.HEIGHT / 4 * 3
                and self.pos_y >= settings.HEIGHT / 4
            ):
                for receiver in nodes:
                    if receiver.order == 0:
                        self.send(receiver)
            else:
                self.vision_radius = 0
                found = False
                while found == False:
                    self.vision_radius += 1
                    for receiver in nodes:
                        if receiver.order == 1 and self.is_reachable(receiver):
                            self.send(receiver)
                            found = True

            self.energy -= settings.PRICE
            if self.energy <= 0:
                self.energy = 0
        


def create_nodes_list(count: int) -> list[Node]:
    """Creates list of Nodes"""
    list = []
    for i in range(count):
        list.append(
            Node(
                (random.randint(0, settings.WIDTH), random.randint(0, settings.HEIGHT)),
                (random.randint(-5, 5), random.randint(-5, 5)),
                id=i,
                energy=random.randint(20, 100),
            )
        )
    return list


def fill_packages(nodes: list["Node"], num=1) -> None:
    """Fill all nodes with NUM uniq package"""
    for i in range(num):
        for node in nodes:
            pack = random.getrandbits(4)
            node.send_buffer.append(pack)
            node.receive_buffer.add(pack)
