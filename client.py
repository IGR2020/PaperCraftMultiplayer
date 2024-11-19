from random import randint
from threading import Thread

from assets import blockSize, massSize
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

        self.allocation = [
            (self.x_offset // blockSize // massSize,
             self.y_offset // blockSize // massSize),
            (self.x_offset // blockSize // massSize + 1,
             self.y_offset // blockSize // massSize),
            (self.x_offset // blockSize // massSize - 1,
             self.y_offset // blockSize // massSize),
            (self.x_offset // blockSize // massSize - 1,
             self.y_offset // blockSize // massSize - 1),
            (self.x_offset // blockSize // massSize + 1,
             self.y_offset // blockSize // massSize - 1),
            (self.x_offset // blockSize // massSize,
             self.y_offset // blockSize // massSize - 1),
            (self.x_offset // blockSize // massSize - 1,
             self.y_offset // blockSize // massSize + 1),
            (self.x_offset // blockSize // massSize + 1,
             self.y_offset // blockSize // massSize + 1),
            (self.x_offset // blockSize // massSize,
             self.y_offset // blockSize // massSize + 1), ]

    def display(self):
        massKeys = list(self.mass.keys())
        for mass in massKeys:
            blockKeys = list(self.mass[mass].keys())
            for block in blockKeys:
                self.mass[mass][block].display(self.window, self.x_offset, self.y_offset)

    def quit(self):
        self.connection.close()

    def handleReceivedData(self, data):
        if data["Type"] == "Mass":
            self.mass[data["Mass"][0]] = data["Mass"][1]

    def tick(self) -> None:
        if randint(0, self.fps) == 0:
            sendData(self.connection, {"Allocation": self.allocation, "Type": "Allocation"})

        mouseDown = pg.mouse.get_pressed()
        relX, relY = pg.mouse.get_rel()
        if True in mouseDown:
            self.x_offset -= relX
            self.y_offset -= relY

        self.allocation = [
            (self.x_offset // blockSize // massSize,
             self.y_offset // blockSize // massSize),
            (self.x_offset // blockSize // massSize + 1,
             self.y_offset // blockSize // massSize),
            (self.x_offset // blockSize // massSize - 1,
             self.y_offset // blockSize // massSize),
            (self.x_offset // blockSize // massSize - 1,
             self.y_offset // blockSize // massSize - 1),
            (self.x_offset // blockSize // massSize + 1,
             self.y_offset // blockSize // massSize - 1),
            (self.x_offset // blockSize // massSize,
             self.y_offset // blockSize // massSize - 1),
            (self.x_offset // blockSize // massSize - 1,
             self.y_offset // blockSize // massSize + 1),
            (self.x_offset // blockSize // massSize + 1,
             self.y_offset // blockSize // massSize + 1),
            (self.x_offset // blockSize // massSize,
             self.y_offset // blockSize // massSize + 1), ]

GameClient((900, 500), "Client", "Local").start()
