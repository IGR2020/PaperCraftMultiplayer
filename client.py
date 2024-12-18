from random import randint
from threading import Thread
from time import sleep


from assets import blockSize, massSize, defaultPlayerArgs
from game import Client, sendData
from objects import Block, Player
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

        self.player = Player(*defaultPlayerArgs, "ClientRun")
        self.allPlayers = []

        self.playerId = None

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
             self.y_offset // blockSize // massSize + 1)]

    def display(self):
        massKeys = list(self.mass.keys())
        for mass in massKeys:
            blockKeys = list(self.mass[mass].keys())
            for block in blockKeys:
                try:
                    self.mass[mass][block].display(self.window, self.x_offset, self.y_offset)
                except KeyError:
                    pass

        for player in self.allPlayers:
            player.display(self.window, self.x_offset, self.y_offset)

        self.player.display(self.window, self.x_offset, self.y_offset)

    def quit(self):
        sendData(self.connection, "Quit")
        sleep(0.1)
        self.connection.close()

    def handleReceivedData(self, data):
        if data["Type"] == "Mass":
            self.mass[data["Mass"][0]] = data["Mass"][1]
        elif data["Type"] == "Players":
            self.allPlayers: list[Player] = data["Players"]

            if self.playerId is not None:
                for player in self.allPlayers:
                    if player.id == self.playerId:
                        self.allPlayers.remove(player)
                        break

            else:
                for player in self.allPlayers:
                    if player.rect.topleft == self.player.rect.topleft:
                        self.playerId = player.id
                        self.allPlayers.remove(player)
                        break

    def tick(self) -> None:
        Thread(target=sendData, args=(self.connection, {"Allocation": self.allocation, "Type": "Allocation"})).start()
        Thread(target=sendData, args=(self.connection, {"Type": "Player", "Player": self.player})).start()

        self.player.script()
        self.player.collide(self.mass, self.allocation)

        mouseDown = pg.mouse.get_pressed()
        mouseX, mouseY = pg.mouse.get_pos()
        mouseX += self.x_offset
        mouseY += self.y_offset

        if True in mouseDown:
            massAddress, blockAddress = (mouseX // blockSize // massSize, mouseY // blockSize // massSize), (
                mouseX // blockSize, mouseY // blockSize)

            if mouseDown[0]:
                Thread(target=sendData, args=(self.connection, {"Type": "Left Click", "Address": (massAddress, blockAddress)})).start()

            if mouseDown[2]:
                Thread(target=sendData, args=(self.connection, {"Type": "Right Click", "Address": (massAddress, blockAddress)})).start()

        self.x_offset, self.y_offset = self.player.rect.centerx - self.width/2, self.player.rect.centery - self.height/2

        self.allocation = [
            (self.player.rect.centerx // blockSize // massSize,
             self.player.rect.centery // blockSize // massSize),
            (self.player.rect.centerx // blockSize // massSize + 1,
             self.player.rect.centery // blockSize // massSize),
            (self.player.rect.centerx // blockSize // massSize - 1,
             self.player.rect.centery // blockSize // massSize),
            (self.player.rect.centerx // blockSize // massSize - 1,
             self.player.rect.centery // blockSize // massSize - 1),
            (self.player.rect.centerx // blockSize // massSize + 1,
             self.player.rect.centery // blockSize // massSize - 1),
            (self.player.rect.centerx // blockSize // massSize,
             self.player.rect.centery // blockSize // massSize - 1),
            (self.player.rect.centerx // blockSize // massSize - 1,
             self.player.rect.centery // blockSize // massSize + 1),
            (self.player.rect.centerx // blockSize // massSize + 1,
             self.player.rect.centery // blockSize // massSize + 1),
            (self.player.rect.centerx // blockSize // massSize,
             self.player.rect.centery // blockSize // massSize + 1), ]

GameClient((900, 500), "Client", "Local").start()
