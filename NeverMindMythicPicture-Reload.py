import re
import shutil
from pathlib import Path

from PIL import Image

# to do list
# 指定中心点

message = {
    "illegal": "  输入不合法, 请重新输入 >> "
}


def is_float(value):
    try:
        float(value)
        return True
    except:
        return False


def input_check(string, mode, condition=None):
    """检测输入, 限制输入内容."""
    target = input(string)
    while (mode == "in" and target != "" and target in condition) or (
            mode == "not_equal" and target != condition) or (
            mode == "digit" and target.isdigit()) or (
            mode == "float" and is_float(target)):
        target = input(message["illegal"])
    return target


class Pic():

    def __init__(self, path):
        self.path = path
        self.file = Image.open(path)
        self.pixel = self.file.convert("RGBA").load()
        self.size_x, self.size_y = self.file.size

    def get_color(self, x, y):
        """获取指定像素格式化后的RGB颜色."""
        color = '#'
        for value in self.pixel[x, y][:3]:
            color += str(hex(value))[3:].zfill(2)
        return color


class Gif(Pic):

    def __init__(self, path):
        Pic.__init__(self, path)

    def cut(self, remove_cover=False, scale=1, suffix=".png"):
        """GIF逐帧分解."""
        dir_path = self.path.with_name(self.path.stem)
        shutil.rmtree(dir_path, True)
        dir_path.mkdir()
        try:
            count = 1 if remove_cover else 0
            while True:
                self.file.seek(count)
                self.file.convert("RGBA")
                self.file.resize((round(self.size_x * scale),
                                  round(self.size_y * scale)), Image.ANTIALIAS)
                self.file.save(dir_path / (self.path.stem +
                                           str(count).zfill(4) + suffix))
                count += 1
        except EOFError:
            pass


path = [path for path in Path().cwd().glob("*.gif")][0]
Gif(path).cut(False)
