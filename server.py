from game import Server, sendData


class GameServer(Server):
    def handleSentPacket(self, data, address):
        sendData(self.clientData[address]["Socket"], "Hello!")

GameServer().start()