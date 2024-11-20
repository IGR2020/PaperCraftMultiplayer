from perlin_noise import PerlinNoise

from assets import defaultPlayerArgs, blockSize
from game import Server, sendData

from objects import Player, Block
from world import createMass


class GameServer(Server):
    def __init__(self):
        super().__init__()

        self.mass = {}
        self.noise = PerlinNoise()

        self.tickStep = 0

        self.updatedMass = []

    def handleSentPacket(self, data, address):
        if data["Type"] == "Allocation":
            self.clientData[address]["Allocation"] = data["Allocation"]
        elif data["Type"] == "Player":
            self.clientData[address]["Player"] = data["Player"]
            self.clientData[address]["Player"].id = address
        elif data["Type"] == "Left Click":
            try:
                del self.mass[data["Address"][0]][data["Address"][1]]
                self.updatedMass.append(data["Address"][0])
            except KeyError:
                pass
        elif data["Type"] == "Right Click":
            try:
                self.mass[data["Address"][0]][data["Address"][1]]
            except KeyError:
                try:
                    self.mass[data["Address"][0]][data["Address"][1]] = Block(data["Address"][1][0]*blockSize, data["Address"][1][1]*blockSize, "Stone")
                    self.updatedMass.append(data["Address"][0])
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
            try:
                for allocation in self.clientData[address]["Allocation"]:
                    try:
                        self.mass[allocation]
                    except KeyError:
                        self.mass[allocation] = createMass(self.noise, allocation, 0.02, 30)
                        self.updatedMass.append(allocation)
                    if allocation in self.updatedMass:
                        sendData(self.clientData[address]["Socket"], {"Mass": (allocation, self.mass[allocation]), "Type": "Mass"})
            except KeyError:
                pass
        self.updatedMass = []
        self.tickStep = 0

GameServer().start()