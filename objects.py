import pygame as pg
from assets import assets, blockSize


class Block:
    def __init__(self, x, y, name: str):
        self.rect = pg.Rect(x, y, blockSize, blockSize)
        self.name = name

    def display(self, window: pg.Surface, x_offset: int, y_offset: int):
        window.blit(assets[self.name], (self.rect.x, self.rect.y))

def collide(obj, player):
    return obj.rect.colliderect(player.rect)
