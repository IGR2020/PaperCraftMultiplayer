import socket
from threading import Thread

import pygame as pg

from assets import defaultPort, header
from functions import loadStream, saveStream


class Client:
    def __init__(
            self,
            resolution: tuple[int, int],
            name: str,
            ip: str,
            fps: int = 60,
            background: tuple[int, int, int] = (255, 255, 255),
    ):
        self.width, self.height = resolution
        self.name = name
        self.window = pg.display.set_mode(resolution, flags=pg.RESIZABLE)
        self.fps = fps
        self.clock = pg.time.Clock()
        self.run = True
        self.background = background
        pg.display.set_caption(name)

        self.deltaTime = 0
        self.serverIp = ip
        if ip == "Local":
            self.serverIp = socket.gethostbyname(socket.gethostname())
        self.connection = socket.socket()


    def receiveData(self):
        self.connection.connect((self.serverIp, defaultPort))

        while self.run:
            data = getData(self.connection)
            if data == "Invalid":
                continue
            self.handleReceivedData(data)

    def handleReceivedData(self, data):
        ...

    def tick(self) -> None: ...

    def display(self) -> None:
        ...

    def event(self, event: pg.event.Event) -> None: ...

    def debug(self):
        print(self.deltaTime)

    def videoResize(self): ...

    def quit(self): ...

    def quitEvent(self): ...

    def start(self):
        Thread(target=self.receiveData).start()

        while self.run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quitEvent()
                    self.run = False
                if event.type == pg.KEYDOWN and event.key == pg.K_F3:
                    self.debug()
                if event.type == pg.VIDEORESIZE:
                    self.width, self.height = event.dict["size"]
                    self.videoResize()
                self.event(event)

            self.deltaTime = self.clock.tick(self.fps) / 16
            if self.deltaTime > 1.2:
                print("[Graphics] Low FPS")
            self.tick()
            self.window.fill(self.background)
            self.display()
            pg.display.update()

        pg.quit()
        return self.quit()

class Server:
    def __init__(self):
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = defaultPort

        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((self.ip, self.port))

        self.clientData = {}
        self.run = True


    def clientJoinHandler(self):
        self.serverSocket.listen()

        while self.run:

            connection, address = self.serverSocket.accept()
            self.clientData[address] = {}
            self.clientData[address]["Socket"] = connection
            self.assignClientData(address)
            Thread(target=self.packetReceiver, args=(address,)).start()

    def assignClientData(self, address): ...

    def tick(self): ...

    def packetReceiver(self, address):
        connection = self.clientData[address]["Socket"]

        while self.run:
            data = getData(connection)
            if data == "Invalid":
                continue
            if data == "Quit":
                del self.clientData[address]
                return
            self.handleSentPacket(data, address)

        return

    def handleSentPacket(self, data, address):
        ...

    def start(self):
        Thread(target=self.clientJoinHandler).start()

        while self.run:
            self.tick()



def sendData(connection, data):
    try:
        data = saveStream(data)
        dataSize = str(len(data)).encode()
        if len(dataSize) > header:
            raise ValueError("Data Size Too Large")
        dataSize += (header - len(dataSize)) * " ".encode()
        connection.send(dataSize)
        connection.send(data)
    except ConnectionAbortedError and ConnectionResetError:
        return "Invalid"

def getData(connection):
    try:
        dataSize = connection.recv(header)
        dataSize = int(dataSize.decode())
        formatedData = connection.recv(dataSize)
        return loadStream(formatedData)
    except:
        return "Invalid"
