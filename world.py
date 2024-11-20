
import pygame as pg
from perlin_noise import PerlinNoise
from assets import massSize, blockSize
from objects import Block

def createMass(noise: PerlinNoise, mass_cords: tuple[int, int], terrainStability: float, terrainVariation: int):
    objects = {}

    # create terrain
    for x in range(round(mass_cords[0] * massSize), round((mass_cords[0] + 1) * massSize)):
        for y in range(round(mass_cords[1] * massSize), round((mass_cords[1] + 1) * massSize)):
            if noise((x * terrainStability, 0)) * terrainVariation + 8 < y:
                objects[x, y] = Block(x * blockSize, y * blockSize, "Stone")

    return objects
