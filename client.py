from random import randint

from game import Client, sendData
from objects import Block


class GameClient(Client):
    def __init__(
            self,
            resolution: tuple[int, int],
            name: str,
            ip: str,
            fps: int = 60,
            background: tuple[int, int, int] = (255, 255, 255),
    ):
        super().__init__(resolution, name, ip, fps, background)

        self.x_offset, self.y_offset = 0, 0
        self.mass = {}

    def display(self):
        for mass in self.mass:
            for block in self.mass[mass]:
                self.mass[mass][block].display(self.window, self.x_offset, self.y_offset)


    def handleReceivedData(self, data):
        if data["Type"] == "Mass":
            blocks = {a: Block(*args) for a, args in data["Mass"][1]}
            self.mass[data["Mass"][0]] = blocks

    def tick(self) -> None:
        if randint(0, self.fps) == 0:
            sendData(self.connection, {"Allocation": []})

GameClient((900, 500), "Client", "Local").start()