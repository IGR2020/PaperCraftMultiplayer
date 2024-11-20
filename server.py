from perlin_noise import PerlinNoise

from game import Server, sendData
from time import sleep, time

from objects import Player
from world import createMass


class GameServer(Server):
    def __init__(self):
        super().__init__()

        self.mass = {}
        self.noise = PerlinNoise()

    def handleSentPacket(self, data, address):
        if data["Type"] == "Allocation":
            self.clientData[address]["Allocation"] = data["Allocation"]

    def assignClientData(self, address):
        self.clientData[address]["Allocation"] = []
        self.clientData[address]["Player"] = Player(0, -30, "Player")

    def tick(self):

        addresses = list(self.clientData.keys())
        for address in addresses:
            for allocation in self.clientData[address]["Allocation"]:
                if not allocation in self.mass.keys():
                    self.mass[allocation] = createMass(self.noise, allocation, 0.02, 30)
                try:
                    sendData(self.clientData[address]["Socket"], {"Mass": (allocation, self.mass[allocation]), "Type": "Mass"})
                except KeyError:
                    pass

GameServer().start()