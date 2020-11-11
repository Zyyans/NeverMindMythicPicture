from PIL import Image
from pathlib import Path


class NM_Base:

    def __init__(self):

        self.path = Path.cwd()


class NM_Picture:

    def __init__(self, path):

        self.path = Path(path)


        picture = Image.open(self.path)

        convert_mode = {
            ".jpg": "RGB",
            ".png": "RGBA"
        }
        converted_picture = picture.convert(self.path.suffix)
