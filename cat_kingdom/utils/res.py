import os
from PIL import Image
from enum import Enum
import plistlib
import cv2
import numpy as np
import json
import pygame


class ResName(str, Enum):
    ENEMY = "enemies_jungle-hd"


class ResourceHolder:
    def __init__(self, path="./Resources"):
        self.path = path
        self.canibal = None

    @staticmethod
    def load_images_sequence(info, img, prefix, start, end, flip=False):
        ret = []
        for idx in range(start, end + 1):
            if prefix % idx in info:
                img_info = info[prefix % idx]
                if flip:
                    ret.append(pygame.transform.flip(ResourceHolder.load_image(img, img_info), True, False))
                else:
                    ret.append(ResourceHolder.load_image(img, img_info))
            else:
                # print("Cannot find ", prefix % idx)
                pass
        return ret

    @staticmethod
    def load_image(img, img_info):
        img_box = img_info["textureRect"]
        img_box = [int(x) for x in img_box.replace('{', '').replace('}', '').replace(' ', '').split(',')]
        img_box = [img_box[0], img_box[1], img_box[0] + img_box[2], img_box[1] + img_box[3]]
        image = img.crop(img_box)
        if img_info["textureRotated"]:
            image = image.rotate(90)
        return pygame.image.fromstring(image.tobytes(), image.size, image.mode)

    @staticmethod
    def load_res(res_name):
        fname = os.path.join(os.getenv("RESOURCE_PATH"), f"{res_name}.plist")
        img = Image.open(os.path.join(os.getenv("RESOURCE_PATH"), f"{res_name}.png"))

        with open(fname, "rb") as file:
            plist = plistlib.load(file)
            return plist, img

    def load_path(self, level):
        fname = os.path.join(self.path, f"level{level}_paths.plist")
        with open(fname, "rb") as file:
            plist = plistlib.load(file)
            return plist['paths']


if __name__ == '__main__':
    res = ResourceHolder()
    res.load_canibal()
