import os
from PIL import Image
from enum import Enum
import plistlib
import cv2
import numpy as np


class ResName(str, Enum):
    ENEMY = "enemies_jungle-hd"


class ResourceHolder:
    def __init__(self, path="./Resources"):
        self.path = path
        self.canibal = None

    def load_canibal(self):
        info, img = self.load_res(ResName.ENEMY)
        canibal_dict = {k:v for k, v in info['frames'].items() if "Canibal_" in k}
        for k, v in canibal_dict.copy().items():
            aliases = v["aliases"]
            for alias in aliases:
                canibal_dict.update({alias: v.copy()})
                canibal_dict[alias].pop("aliases")
            canibal_dict[k].pop("aliases")
        left_seq = self.load_images_sequence(canibal_dict, img, "Canibal_0{:03}.png", 67, 77)

    def load_images_sequence(self, info, img, prefix, start, end):
        ret = []
        for idx in range(start, end + 1):
            if prefix.format(idx) in info:
                img_info = info[prefix.format(idx)]
                ret.append(self.load_image(img, img_info))
            else:
                print("Cannot find ", prefix.format(idx))
        return ret

    def load_image(self, img, img_info):
        img_box = img_info["textureRect"]
        img_box = [int(x) for x in img_box.replace('{', '').replace('}', '').replace(' ', '').split(',')]
        img_box = [img_box[0], img_box[1], img_box[0] + img_box[2], img_box[1] + img_box[3]]
        return img.crop(img_box)

    def load_res(self, res_name):
        fname = os.path.join(self.path, f"{res_name}.plist")
        img = Image.open(os.path.join(self.path, f"{res_name}.png"))

        with open(fname, "rb") as file:
            plist = plistlib.load(file)
            return plist, img


if __name__ == '__main__':
    res = ResourceHolder()
    res.load_canibal()
