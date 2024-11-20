import pygame as pg
from functions import loadAssets

blockSize = 32
assets = loadAssets("assets/blocks", scale=blockSize/16)

playerSize = blockSize - blockSize*0.1, blockSize*2 - blockSize*0.1
playerImage = "Player.png"
assets["Player"] = pg.transform.scale(pg.image.load(f"assets/{playerImage}"), playerSize)

defaultPort = 5050
header = 8

massSize = 16

massSendStyle = "{'type': 'Mass', 'Mass': ((0, 0), Blocks)}"