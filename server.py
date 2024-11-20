from perlin_noise import PerlinNoise

from assets import defaultPlayerArgs
from game import Server, sendData
from time import sleep, time

from objects import Player
from world import createMass


class GameServer(Server):
    def __init__(self):
        super().__init__()

        self.mass = {}
        self.noise = PerlinNoise()

        self.tickStep = 0

    def handleSentPacket(self, data, address):
        if data["Type"] == "Allocation":
            self.clientData[address]["Allocation"] = data["Allocation"]
        elif data["Type"] == "Player":
            self.clientData[address]["Player"] = data["Player"]
            self.clientData[address]["Player"].id = address
        elif data["Type"] == "Left Click":
            try:
                del self.mass[data["Address"][0]][data["Address"][1]]
            except KeyError:
                pass

    def assignClientData(self, address):
        self.clientData[address]["Allocation"] = []
        self.clientData[address]["Player"] = Player(*defaultPlayerArgs, address)

    def tick(self):
        self.tickStep += 1

        addresses = list(self.clientData.keys())
        for address in addresses:
            try:
                output = sendData(self.clientData[address]["Socket"], {"Type": "Players", "Players": [self.clientData[client]["Player"] for client in addresses]})
                if output == "Invalid":
                    del self.clientData[address]
            except KeyError:
                pass

        if self.tickStep % 5 != 0:
            return

        for address in addresses:
            for allocation in self.clientData[address]["Allocation"]:
                if not allocation in self.mass.keys():
                    self.mass[allocation] = createMass(self.noise, allocation, 0.02, 30)
                try:
                    sendData(self.clientData[address]["Socket"], {"Mass": (allocation, self.mass[allocation]), "Type": "Mass"})
                except KeyError:
                    pass

        self.tickStep = 0

GameServer().start()