import pygame as pg
from functions import loadAssets

blockSize = 64
assets = loadAssets("assets/blocks", scale=blockSize/16)

defaultPort = 5050
header = 8

massSize = 16

massSendStyle = "{'type': 'Mass', 'Mass': ((0, 0), {(0, 0): (x, y, name)})}"