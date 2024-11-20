import pygame as pg
from assets import assets, blockSize, playerSize, massSize, playerSprintSpeed, maxPlayerSpeed


class Block:
    def __init__(self, x: int, y: int, name: str):
        self.rect = pg.Rect(x, y, blockSize, blockSize)
        self.name = name

    def display(self, window: pg.Surface, x_offset: int, y_offset: int):
        window.blit(assets[self.name], (self.rect.x - x_offset, self.rect.y - y_offset))


class Player:
    def __init__(self, x: int, y: int, name: str, playerId: str):
        self.rect = pg.Rect(x, y, playerSize[0], playerSize[1])
        self.name = name
        self.x_vel = 0
        self.y_vel = 0
        self.id = playerId
        self.jumpCount = 0

    def display(self, window: pg.Surface, x_offset: int, y_offset: int):
        window.blit(assets[self.name], (self.rect.x - x_offset, self.rect.y - y_offset))

    def script(self):
        try:
            self.x_vel -= self.x_vel / abs(self.x_vel) * 0.5
            print(self.x_vel)
        except ZeroDivisionError:
            self.x_vel = 0
        self.y_vel += 0.2

        keys = pg.key.get_pressed()
        if keys[pg.K_a] and self.x_vel > -playerSprintSpeed:
            self.x_vel -= 3
        if keys[pg.K_d] and self.x_vel < playerSprintSpeed:
            self.x_vel += 3
        if keys[pg.K_SPACE] and self.jumpCount == 0:
            self.jump()

        self.x_vel = max(min(self.x_vel, maxPlayerSpeed), -maxPlayerSpeed)

    def jump(self):
        self.y_vel = -5
        self.jumpCount = 1
        self.x_vel *= 1.5

    def land(self):
        self.y_vel = 0
        self.jumpCount = 0

    def hitHead(self):
        self.y_vel = 0

    def collide(self, mass: dict[tuple[int, int], dict[tuple[int, int], Block]], allocation: list[tuple[int, int]]):

        self.rect.x += self.x_vel
        for massKey in allocation:
            try:
                blockKeys = mass[massKey].keys()
            except KeyError:
                break
            for blockKey in blockKeys:
                try:
                    obj = mass[massKey][blockKey]
                    if collide(obj, self):
                        if self.x_vel > 0:
                            self.rect.right = obj.rect.left
                        else:
                            self.rect.left = obj.rect.right
                        break
                except KeyError:
                    break

        self.rect.y += self.y_vel
        for massKey in allocation:
            try:
                blockKeys = mass[massKey].keys()
            except KeyError:
                break
            for blockKey in blockKeys:
                try:
                    obj = mass[massKey][blockKey]
                    if collide(obj, self):
                        if self.y_vel > 0:
                            self.rect.bottom = obj.rect.top
                            self.land()
                        else:
                            self.rect.top = obj.rect.bottom
                            self.hitHead()
                        break
                except KeyError:
                    break


def collide(obj, player):
    return obj.rect.colliderect(player.rect)
