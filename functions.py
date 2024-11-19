import pygame as pg
from os import listdir
from os.path import isfile, isdir, join
import json
import pickle

def loadAssets(path, size: tuple[int, int] = None, scale: float = None, getSubDirsAsList=False, scaleifsize=None):
    sprites = {}
    for file in listdir(path):
        if getSubDirsAsList and isdir(join(path, file)):
            sprites[file.replace(".png", "")] = load_assets_list(
                join(path, file), size, scale
            )
            continue
        elif not isfile(join(path, file)):
            continue
        if size is None and scale is None:
            sprites[file.replace(".png", "")] = pg.image.load(join(path, file))
        elif scale is not None:
            image = pg.image.load(join(path, file))
            if scaleifsize and image.get_size() != scaleifsize:
                  sprites[file.replace(".png", "")] = image
                  continue
            sprites[file.replace(".png", "")] = pg.transform.scale_by(
                image, scale
            )
        else:
            sprites[file.replace(".png", "")] = pg.transform.scale(
                pg.image.load(join(path, file)), size
            )
    return sprites


def load_assets_list(path, size: tuple[int, int] = None, scale: float = None):
    sprites = []
    for file in listdir(path):
        if not isfile(join(path, file)):
            continue
        if size is None and scale is None:
            sprites.append(pg.image.load(join(path, file)))
        elif scale is not None:
            sprites.append(
                pg.transform.scale_by(pg.image.load(join(path, file)), scale)
            )
        else:
            sprites.append(pg.transform.scale(pg.image.load(join(path, file)), size))
    return sprites


def loadJson(path):
    with open(path) as file:
        data = json.load(file)
        file.close()
    return data

def saveData(data, path):
    with open(path, "wb") as file:
        pickle.dump(data, file)
        file.close()

def loadData(path):
    with open(path, "rb") as file:
        data = pickle.load(file)
        file.close()
    return data

def loadStream(stream):
    return pickle.loads(stream)

def saveStream(data):
    return pickle.dumps(data)
