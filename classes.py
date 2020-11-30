from PIL import Image
from pathlib import Path


class Base:

    def __init__(self):

        self.path = Path('.')
        self.pic_dir_path = self.path / "Pictures"
        self.tex_dir_path = self.path / "Textures"

        self.pic_dir_path.mkdir(exist_ok=True)
        self.tex_dir_path.mkdir(exist_ok=True)
    
    def get_pic_paths(self):

        self.pic_paths = []
        for suffix in ["gif", "jpg", "png"]:
            for path in self.pic_dir_path.glob("*." + suffix):
                self.pic_paths.append(path)
        return len(self.pic_paths) if self.pic_paths else False

    def get_tex_paths(self):  # 待优化

        json_paths = [path for path in self.tex_dir_path.glob("*.json")]
        png_paths = [path for path in self.tex_dir_path.glob("*.png")]

        json_stems = [path.stem for path in json_paths]
        if json_stems != [path.stem for path in png_paths]:
            return False

        self.tex_paths = []
        for i in range(len(json_stems)):
            self.tex_paths.append({json_stems[i]: (json_paths[i], png_paths[i])})
        return len(json_stems)


class Picture:

    def __init__(self, path):

        self.path = Path(path)

        self.image = Image.open(self.path)


    @property
    def width(self):
        return self.image.width


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


base = Base()
print(base.get_tex_paths())
