from game import Server, sendData
from time import sleep

class GameServer(Server):
    def __init__(self):
        super().__init__()

        self.mass = {}

    def handleSentPacket(self, data, address):
        if data["Type"] == "Allocation":
            self.clientData[address]["Allocation"] = data["Allocation"]

    def assignClientData(self, address):
        self.clientData[address]["Allocation"] = []

    def tick(self):
        sleep(1)
        for address in self.clientData:
            for allocation in self.clientData["Allocation"]:
                ...


GameServer().start()