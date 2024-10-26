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
        self.vision_radius = int(vision_radius * energy / 100)
        self.energy = energy
        self.send_buffer: list = list()  # queue
        self.receive_buffer: set = set()  # set

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
        if self.send_buffer == []:
            return  # if there is no packages to send, stop
        if self.send_buffer[0] not in receiver.receive_buffer:
            receiver.send_buffer.append(self.send_buffer[0])
            receiver.receive_buffer.add(self.send_buffer[0])

    def send_to_all(self, nodes: list["Node"]) -> None:
        """Sends package to all than delete it and downgrades energy"""
        if self.send_buffer == []:
            return  # if there is no packages to send, stop
        sended = 0
        for receiver in nodes:
            if self.is_reachable(receiver):
                self.send(receiver)
                sended += 1
        if sended > 1:
            self.energy -= 5
            self.vision_radius = int(self.vision_radius * self.energy / 100)
            self.send_buffer.pop(0)


def create_nodes_list(count: int) -> list[Node]:
    """Creates list of Nodes"""
    list = []
    for i in range(count):
        list.append(
            Node(
                (random.randint(0, settings.WIDTH), random.randint(0, settings.HEIGHT)),
                (random.randint(-5, 5), random.randint(-5, 5)),
                id=i,
            )
        )
    return list


def fill_packages(nodes: list["Node"]) -> None:
    """Fill all nodes with 1 uniq package"""
    for node in nodes:
        node.send_buffer.append(random.getrandbits(16))
        node.receive_buffer.add(random.getrandbits(16))


def info(nodes: list["Node"]) -> None:
    """Prints all the info about nodes"""
    for node in nodes:
        print(f"Node {node.id}: ")
        print(
            f" (x, y): ({node.pos_x}, {node.pos_y})\
            \n energy: {node.energy}\
            \n receive_buff: {node.receive_buffer}\
            \n send_buff: {node.send_buffer}\n"
        )
