from PIL import Image
from pathlib import Path


class Base:

    def __init__(self):

        self.path = Path.cwd()
        for sub_path in ["Pictures", "Textures"]:
            (self.path / sub_path).mkdir(exist_ok=True)


class Picture:

    def __init__(self, path):

        self.path = Path(path)

        self.image = Image.open(self.path)


    @property
    def width(self):
        return self.image.width

    @property
    def height(self):
        return self.image.height

    @property
    def pixel(self, x, y):
        return self.pixels[(x, y)]


    def pixel_init(self):
        self.pixels = self.converted.load()


    def convert(self):

        convert_mode = {
            ".jpg": "RGB",
            ".png": "RGBA"
        }

        self.converted = self.image.convert(convert_mode[self.path.suffix])


    def magic(self):


    @staticmethod
    def get_color(raw):
        color = '#'
        for value in raw[:3]:
            color += str(hex(int(value)))[-2:].replace('x', '0')
        return color.upper()


class GIF(Picture):

    def __init__(self):
        
        super().__init__()


temp = Picture("icon.jpg")
print(temp.width, temp.height)
