import os
import json
import plistlib
from PIL import Image
from enum import Enum


class ResName(str, Enum):
    ENEMY = "enemies_jungle-hd"


class ResourceHolderMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ResourceHolder(dict, metaclass=ResourceHolderMeta):
    def __init__(self, path="./Resources"):
        super().__init__()
        self.path = path
        self.canibal = None

    @staticmethod
    def load_images_sequence(info, img, prefix, start, end, flip=False):
        ret = []
        for idx in range(start, end + 1):
            if prefix % idx in info:
                img_info = info[prefix % idx]
                image = ResourceHolder.load_image(img, img_info)
                if flip:
                    ret.append(image.transpose(Image.TRANSPOSE))
                else:
                    ret.append(image)
            else:
                print("Cannot find ", prefix % idx)
        return ret

    @staticmethod
    def load_image(img: Image.Image, img_info: dict) -> Image.Image:
        img_box = img_info["textureRect"]
        img_box = [int(x) for x in img_box.replace('{', '').replace('}', '').replace(' ', '').split(',')]
        img_box = [img_box[0], img_box[1], img_box[0] + img_box[2], img_box[1] + img_box[3]]
        image = img.crop(img_box)
        if img_info["textureRotated"]:
            image = image.rotate(180)
        return image

    @staticmethod
    def load_res(res_name):
        fname = os.path.join(os.getenv("RESOURCE_PATH"), f"{res_name}.plist")
        img = Image.open(os.path.join(os.getenv("RESOURCE_PATH"), f"{res_name}.png"))

        with open(fname, "rb") as file:
            plist = plistlib.load(file)
            return plist, img

    @staticmethod
    def _load_enemy(res_dir:str="enemies_jungle-hd", name:str="Canibal") -> dict:
        info, img = ResourceHolder.load_res(res_dir)
        sprite_dict = {k: v for k, v in info['frames'].items() if f"{name}_" in k}
        for k, v in sprite_dict.copy().items():
            aliases = v["aliases"]
            for alias in aliases:
                sprite_dict[alias] = v.copy()
                sprite_dict[alias].pop("aliases")
            sprite_dict[k].pop("aliases")

        sprite_info = None
        with open(os.path.join(os.getenv("RESOURCE_PATH"), "object_sprite.json")) as f:
            sprite_info = json.load(f)[name]

        action = "runleft"
        left_seq = ResourceHolder.load_images_sequence(sprite_dict, img,
                                                       sprite_info[action]["prefix"],
                                                       sprite_info[action]["start"],
                                                       sprite_info[action]["end"],
                                                       True)
        action = "runright"
        right_seq = ResourceHolder.load_images_sequence(sprite_dict, img,
                                                        sprite_info[action]["prefix"],
                                                        sprite_info[action]["start"],
                                                        sprite_info[action]["end"])
        action = "runup"
        up_seq = ResourceHolder.load_images_sequence(sprite_dict, img,
                                                     sprite_info[action]["prefix"],
                                                     sprite_info[action]["start"],
                                                     sprite_info[action]["end"])
        action = "rundown"
        down_seq = ResourceHolder.load_images_sequence(sprite_dict, img,
                                                       sprite_info[action]["prefix"],
                                                       sprite_info[action]["start"],
                                                       sprite_info[action]["end"])
        action = "death"
        death_seq = ResourceHolder.load_images_sequence(sprite_dict, img,
                                                        sprite_info[action]["prefix"],
                                                        sprite_info[action]["start"],
                                                        sprite_info[action]["end"])
        action = "attack"
        attack_seq = ResourceHolder.load_images_sequence(sprite_dict, img,
                                                         sprite_info[action]["prefix"],
                                                         sprite_info[action]["start"],
                                                         sprite_info[action]["end"])
        return {
            "left": left_seq,
            "right": right_seq,
            "up": up_seq,
            "down": down_seq,
            "death": death_seq,
            "attack": attack_seq,
            "delay": float(sprite_info[action]["delay"])
        }

    def get_enemy(self, name : str) -> Image.Image:
        if name not in self.keys():
            self.update({name: self._load_enemy(name=name)})
        return self.get(name)
ResourceHolder()



if __name__ == '__main__':
    ResourceHolder().get_enemy("Canibal")
    ResourceHolder()["Canibal"]['down'][0].show()