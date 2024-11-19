from random import randint
from threading import Thread

from game import Client, sendData
from objects import Block
import pygame as pg


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

    def quit(self):
        self.connection.close()

    def handleReceivedData(self, data):
        if data["Type"] == "Mass":
            self.mass[data["Mass"][0]] = data["Mass"][1]

    def tick(self) -> None:
        if randint(0, self.fps) == 0:
            sendData(self.connection, {"Allocation": [(0, 0), (1, 0), (-1, 0)], "Type": "Allocation"})

        mouseDown = pg.mouse.get_pressed()
        relX, relY = pg.mouse.get_rel()
        if True in mouseDown:
            self.x_offset -= relX
            self.y_offset -= relY

GameClient((900, 500), "Client", "Local").start()