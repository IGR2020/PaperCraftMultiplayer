from perlin_noise import PerlinNoise

from game import Server, sendData
from time import sleep

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

    def tick(self):
        sleep(1)
        for address in self.clientData:
            for allocation in self.clientData[address]["Allocation"]:
                if not allocation in self.mass.keys():
                    self.mass[allocation] = createMass(self.noise, allocation, 0.02, 30)
                output = sendData(self.clientData[address]["Socket"], {"Mass": (allocation, self.mass[allocation]), "Type": "Mass"})
                if output == "Invalid":
                    del self.clientData[address]
                    break
            else:
                continue
            break

GameServer().start()