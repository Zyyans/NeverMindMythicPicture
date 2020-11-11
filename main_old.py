from Settings import PictureSettings, TextureSettings

from json import load
from os import system
from pathlib import Path
from PIL import Image
from shutil import rmtree


def title():
    system('cls')
    print('\n  NeverMindMythicPicture v2.4\n  Author: Hodo7am, Zyyans.\n  ')


def get_color(raw_color):
    color = '#'
    for value in raw_color[:3]:
        color += str(hex(int(value)))[-2:].replace('x', '0')
    return color.upper()


def cut(path, setiings, gif_dir_path):
    img = Image.open(path)
    try:
        i = 0
        while True:
            i += 1
            temp = img.convert('RGB') if setiings.suffix == '.jpg' else img.convert('RGBA')
            temp.resize((round(img.size[0] / setiings.scale), round(img.size[1] / setiings.scale)))
            temp.save(gif_dir_path / (path.stem + str(i).zfill(4) + setiings.suffix))
            img.seek(i)
    except EOFError:
        pass


def magic(path, size, scale=False):

    temp = Image.open(path).convert('RGB') if path.suffix == '.jpg' else Image.open(path).convert('RGBA')
    pixel, sx, sy = temp.load(), *temp.size
    temp.close()

    if scale:
        mode = 'RGB' if path.suffix == '.jpg' else 'RGBA'
        new_pixel = Image.new(mode, (int(sx / size), int(sy / size))).load()

    for ix in range(0, sx, size):
        for iy in range(0, sy, size):
            stack = []
            for x in range(0, size):
                for y in range(0, size):
                    if ix + x < sx and iy + y < sy:
                        stack.append(pixel[ix + x, iy + y])
            most = max(stack, key=stack.count)
            if scale:
                x, y = int(ix / size), int(iy / size)
                if x < int(sx / size) - 1 and y < int(sy / size) - 1:
                    new_pixel[x, y] = most
            else:
                for x in range(0, size):
                    for y in range(0, size):
                        if ix + x < sx and iy + y < sy:
                            pixel[ix + x, iy + y] = most

    return new_pixel, int(sx / size), int(sy / size) if scale else pixel, sx, sy


def build(path, settings):

    if settings.magic != 1:
        pixel, sx, sy = magic(path, settings.magic, settings.magic_scale)
    else:
        temp = Image.open(path).convert('RGB') if path.suffix == '.jpg' else Image.open(path).convert('RGBA')
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
                    xo, yo = round((sx / 2 - x) / 10, 1), round((sy / 2 - y) / 10, 1)
                else:
                    xo, yo = round((y - sy / 2) / 10, 1), round((sy / 2 - x) / 10, 1)
            else:
                xo, yo = round((sx / 2 - x) / 10, 1), round((sy / 2 - y) / 10, 1)
                if settings.face in ['W', 'N']:
                    xo = -xo

            texts.append(text % (settings.particle, color, xo * settings.density, yo * settings.density))

    return texts


def picture_main():

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
        if paths:
            if dir_path.glob('*.gif'):
                gif = True
            input(f'  已找到 {len(paths)} 张图片.\n  按回车键以开始处理.\n  ')
            break
        input('  未找到任何图片.\n  按回车键以重新查找.\n  ')

    title()
    mode = input('  1. 精确模式 - 以不同的参数分别处理每张图片.'
                 '\n  2. 批量模式 - 以相同的参数按顺序处理所有图片, 并整合在同一技能组中.'
                 '\n     * 顺序 - 第一关键字: 后缀名(默认: JPG, PNG, GIF), 第二优先级: 字典序.'
                 '\n  请输入你需要的处理模式 >> ')
    while mode not in ['1', '2']:
        mode = input('  输入有误, 请重新输入 >> ')

    skill_path = Path().cwd() / 'Skills'
    skill_path.mkdir(exist_ok=True)

    if mode == '1':
        for path in paths:
            if path.suffix == '.gif':
                settings = PictureSettings(True).ask(path, True)
                gif_dir_path = path.parent / path.stem
                gif_dir_path.mkdir(exist_ok=True)
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
                settings = PictureSettings().ask(path)
                with open(f'{skill_path / settings.name}.yml', 'w', encoding='utf-8') as yml:
                    yml.write(f'{settings.name}:\n    Skills:\n' + '\n'.join(build(path, settings)) + '\n')
    else:
        settings = PictureSettings(gif, True).ask(gif=True, batch=True)
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
            yml.write(f'{settings.name}:\n    Skills:\n' + '\n'.join(texts) + '\n')

    input('\n  所有图片处理完成, 请到 Skills 文件夹获取生成的技能.\n  按回车键以退出.')


def texture_main():

    title()
    print('  !!! 本功能只适用于规则排列的 voxel 材质.')

    dir_path = Path().cwd() / 'Textures'
    dir_path.mkdir(exist_ok=True)
    input('\n  初始化完成.'
          '\n  请在 Textures 文件夹中放入你需要处理的材质.'
          '\n  请将 JSON 文件与对应的 PNG 文件命名为同一名称.'
          '\n  例: Zyyans.json, Zyyans.png.'
          '\n  按回车键以继续.'
          '\n  ')

    while True:
        json_paths = [path for path in dir_path.glob('*.json')]
        png_paths = [path for path in dir_path.glob('*.png')]
        if not len(json_paths) and not len(png_paths):
            input('  未找到任何材质.\n  按回车键以重新查找.\n  ')
            continue
        if len(json_paths) != len(png_paths):
            input('  文件无法对应.\n  请在确认文件正确后按回车键以继续.\n  ')
            continue
        temp = [path.stem for path in png_paths]
        for path in json_paths:
            if path.stem not in temp:
                input('  文件无法对应.\n  请在确认文件正确后按回车键以继续.\n  ')
                continue
        input(f'  已找到 {len(json_paths)} 个材质.\n  按回车键以开始处理.\n  ')
        break

    skill_path = Path().cwd() / 'Skills'
    skill_path.mkdir(exist_ok=True)

    for json_path in json_paths:

        settings = TextureSettings().ask(json_path)

        error = False
        text = '    - effect:particles{p=%s;a=1;c=%s;forwardOffset=%.1f;sideOffset=%.1f;yOffset=%.1f}'
        texts = []

        json = load(json_path.open('r'))
        temp = Image.open(json_path.parent / (json_path.stem + '.png'))
        pixel = temp.convert('RGBA').load()
        temp.close()

        for element in json['elements']:

            fx, fy, fz = [round(num / settings.size) for num in element['from']]
            tx, ty, tz = [round(num / settings.size) for num in element['to']]

            colors = []
            uvs = [[round(pos * settings.scale) for pos in face['uv']] for face in element['faces'].values()]
            for uv in uvs:
                [[colors.append(pixel[px, py]) for py in range(uv[1], uv[3])] for px in range(uv[0], uv[2])]
            try:
                color = get_color(max(colors, key=colors.count))
            except ValueError:
                error = True
                input('\n  参数或 PNG 图片存在错误, 取色发生问题, 运行中止.\n  按下回车键以跳过本张图片.')
                break

            for x in range(fx, tx):
                for y in range(fy, ty):
                    for z in range(fz, tz):
                        texts.append(text % (settings.particle, color, round(x * settings.density / 10, 1),
                                             round(y * settings.density / 10, 1), round(z * settings.density / 10, 1)))

        if not error:
            with open(f'{skill_path / settings.name}.yml', 'w', encoding='utf-8') as yml:
                yml.write(f'{settings.name}:\n    Skills:\n' + '\n'.join(texts) + '\n')

    input('\n  所有材质处理完成, 请到 Skills 文件夹获取生成的技能.\n  按回车键以退出.')


if __name__ == '__main__':

    title()
    func = input('  1. 图片转粒子.'
                 '\n  2. 材质转粒子.'
                 '\n  请选择你需要的功能 >> ')
    while func not in ['1', '2']:
        func = input('  输入有误, 请重新输入 >> ')

    if func == '1':
        picture_main()
    else:
        texture_main()
