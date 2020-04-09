from Settings import Settings

from collections import Counter
from math import ceil
from os import system
from pathlib import Path
from PIL import Image
from shutil import rmtree


def title():
    system('cls')
    print('\n  NeverMindMythicPicture v2.4\n  Author: Hodo7am, Zyyans.\n  ')


def get_color(rcolor):
    color = '#'
    for value in rcolor[:3]:
        color += str(hex(int(value)))[-2:].replace('x', '0')
    return color.upper()


def cut(path, setiings, gif_dir_path):
    img = Image.open(path)
    try:
        i = 0
        while True:
            temp = img.convert('RGB') if setiings.suffix == '.jpg' else img.convert('RGBA')
            temp.resize((round(img.size[0] / setiings.scale), round(img.size[1] / setiings.scale)))
            temp.save(gif_dir_path / (path.stem + str(i).zfill(4) + setiings.suffix))
            i += 1
            img.seek(i)
    except EOFError:
        pass


def magic(path, size, scale=False):
    temp = Image.open(path).convert('RGB') if path.suffix == '.jpg' else Image.open(path).convert('RGBA')
    pixel, sx, sy = temp.load(), *temp.size

    if scale:
        mode = 'RGB' if path.suffix == '.jpg' else 'RGBA'
        temp = Image.new(mode, (int(sx / size), int(sy / size)))
        new_pixel = temp.load()

    for ix in range(0, sx, size):
        for iy in range(0, sy, size):
            stack = []
            for x in range(0, size):
                for y in range(0, size):
                    if ix + x < sx and iy + y < sy:
                        stack.append(pixel[ix + x, iy + y])
            most = Counter(stack).most_common(1)[0][0]
            if scale:

                x, y = int(ix / size), int(iy / size)
                if x > int(sx / size) - 1 or y > int(sy / size) - 1:
                    continue
                new_pixel[x, y] = most
            else:
                for x in range(0, size):
                    for y in range(0, size):
                        if ix + x < sx and iy + y < sy:
                            pixel[ix + x, iy + y] = most

    if scale:
        return new_pixel, int(sx / size), int(sy / size)
    return pixel, sx, sy


def build(path, settings):
    if settings.magic != 1:
        pixel, sx, sy = magic(path, settings.magic, True) if settings.magic_scale else magic(path, settings.magic)
    else:
        temp = Image.open(path).convert('RGBA')
        pixel, sx, sy = temp.load(), *temp.size
        temp.close()

    text = {
        '1': '    - effect:particles{p=%s;a=1;c=%s;forwardOffset=%.1f;sideOffset=%.1f}',
        '2': {
            'E': '    - effect:particles{p=%s;a=1;c=%s;forwardOffset=%.1f;yOffset=%.1f}',
            'W': '    - effect:particles{p=%s;a=1;c=%s;forwardOffset=%.1f;yOffset=%.1f}',
            'S': '    - effect:particles{p=%s;a=1;c=%s;sideOffset=%.1f;yOffset=%.1f}',
            'N': '    - effect:particles{p=%s;a=1;c=%s;sideOffset=%.1f;yOffset=%.1f}'
        }
    }[settings.type]
    if settings.type == '2':
        text = text[settings.face]
    texts = []

    for x in range(0, sx, settings.clarity):
        for y in range(0, sy, settings.clarity):
            if path.suffix == '.png' and not pixel[x, y][3]:
                continue
            color = get_color(pixel[x, y])
            if color in settings.ignore:
                continue

            if settings.type == '1':
                if settings.face in ['E', 'W']:
                    xo = round((sx / 2 - x) / 10, 1)
                    yo = round((sy / 2 - y) / 10, 1)
                else:
                    xo = round((y - sy / 2) / 10, 1)
                    yo = round((sy / 2 - x) / 10, 1)
            else:
                xo = round((sx / 2 - x) / 10, 1)
                yo = round((sy / 2 - y) / 10, 1)
                if settings.face in ['W', 'N']:
                    xo = -xo
            texts.append(text % (settings.particle, color, xo, yo))
    return texts


if __name__ == '__main__':

    title()
    dir_path = Path().cwd() / 'Pictures'
    dir_path.mkdir(exist_ok=True)
    input('  初始化完成.'
          '\n  请在 Pictures 文件夹中放入你需要处理的图片.'
          '\n  仅支持 JPG, PNG 和 GIF 格式的图片.'
          '\n  按回车键以继续.'
          '\n  ')

    gif = False
    while True:
        paths = []
        for fe in ['*.jpg', '*.png', '*.gif']:
            paths.extend([path for path in dir_path.glob(fe)])
        if not paths:
            input('  未找到任何图片.\n  按回车键以重新查找.\n  ')
            continue
        if dir_path.glob('*.gif'):
            gif = True
        input(f'  已找到 {len(paths)} 张图片.\n  按回车键以开始处理.\n  ')
        break

    title()
    mode = input('  1. 精确模式 - 以不同的参数分别处理每张图片.'
                 '\n  2. 批量模式 - 以相同的参数按顺序处理所有图片, 并整合在同一技能组中.'
                 '\n     * 顺序 - 第一关键字: 后缀名(默认: JPG, PNG, GIF), 第二优先级: 字典序.'
                 '\n  请输入你需要的处理模式 >> ')
    while True:
        if mode in ['1', '2']:
            break
        else:
            mode = input('  输入有误, 请重新输入 >> ')

    skill_path = Path().cwd() / 'Skills'
    skill_path.mkdir(exist_ok=True)

    if mode == '1':
        for path in paths:
            if path.suffix == '.gif':
                gif_dir_path = path.parent / path.stem
                gif_dir_path.mkdir(exist_ok=True)

                settings = Settings().ask(path, True)
                cut(path, settings, gif_dir_path)

                with open(f'{skill_path / settings.name}.yml', 'w', encoding='utf-8') as yml:
                    i = 0
                    texts = []
                    for sub_path in gif_dir_path.glob(f'*{settings.suffix}'):
                        name = settings.name + str(i).zfill(4)
                        yml.write(f'{name}:\n    Skills:\n' + '\n'.join(build(sub_path, settings)) + '\n')
                        texts.append('    - skill{s=%s}\n    - delay %s' % (name, settings.delay))
                        i += 1
                    yml.write(f'{settings.name}:\n    Skills:\n' + '\n'.join(texts) + '\n')
                    rmtree(gif_dir_path)
            else:
                settings = Settings().ask(path)
                with open(f'{skill_path / settings.name}.yml', 'w', encoding='utf-8') as yml:
                    yml.write(f'{settings.name}:\n    Skills:\n' + '\n'.join(build(path, settings)) + '\n')
    else:
        settings = Settings(gif=gif, batch=True).ask(gif=True, batch=True)
        with open(f'{skill_path / settings.name}.yml', 'w', encoding='utf-8') as yml:
            i = 0
            texts = []
            for path in paths:
                if path.suffix == '.gif':
                    gif_dir_path = path.parent / path.stem
                    gif_dir_path.mkdir(exist_ok=True)

                    cut(path, settings, gif_dir_path)

                    for sub_path in gif_dir_path.glob('*' + settings.suffix):
                        name = settings.name + str(i).zfill(4)
                        yml.write(f'{name}:\n    Skills:\n' + '\n'.join(build(sub_path, settings)) + '\n')
                        texts.append('    - skill{s=%s}\n    - delay %s' % (name, settings.global_delay))
                        i += 1
                else:
                    name = settings.name + str(i).zfill(4)
                    yml.write(f'{name}:\n    Skills:\n' + '\n'.join(build(path, settings)) + '\n')
                    texts.append('    - skill{s=%s}\n    - delay %s' % (name, settings.global_delay))
                    i += 1
            yml.write(f'{settings.name}:\n    Skills:\n' + '\n'.join(texts))

    input('\n  所有图片处理完成.\n  按回车键以退出...')
