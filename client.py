from random import randint

from game import Client, sendData


class GameClient(Client):
    def handleReceivedData(self, data):
        print(data)

    def tick(self) -> None:
        if randint(0, self.fps) == 0:
            sendData(self.connection, "Testy")

GameClient((900, 500), "Client", "Local").start()