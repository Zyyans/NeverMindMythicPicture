from Settings import Settings

from os import system
from pathlib import Path
from PIL import Image


def title():
    system('cls')
    print('\n  NeverMindMythicPicture v2.4'
          '\n  Author: Hodo7am, Zyyans.'
          '\n  ')


def get_color(rcolor):
    color = '#'
    for value in rcolor[:-1]:
        color += str(hex(int(value)))[-2:].replace('x', '0')
    return color.upper()


def cut(path, setiings, gif_dir_path):
    img = Image.open(path)
    try:
        i = 0
        while True:
            (img.convert('RGB') if setiings.suffix == '.jpg' else img.convert('RGBA')).resize(
                (round(img.size[0] / setiings.scale), round(img.size[1] / setiings.scale))).save(
                gif_dir_path / (path.stem + str(i).zfill(4) + setiings.suffix))
            i += 1
            img.seek(i)
    except EOFError:
        pass


def build(path, settings):
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
    skill_path = Path().cwd() / 'Skills'
    dir_path.mkdir(exist_ok=True)
    skill_path.mkdir(exist_ok=True)
    input('  初始化完成.'
          '\n  请在 Pictures 文件夹中放入你需要处理的图片.'
          '\n  仅支持 JPG, PNG 和 GIF 格式的图片.'
          '\n  按回车键以继续.'
          '\n  ')

    gif_mode = False
    while True:
        paths = []
        for fe in ['*.jpg', '*.png', '*.gif']:
            paths.extend([path for path in dir_path.glob(fe)])
        if not paths:
            input('  未找到任何图片.'
                  '\n  按回车键以重新查找.'
                  '\n  ')
            continue
        if dir_path.glob('*.gif'):
            gif_mode = True
        input(f'  已找到 {len(paths)} 张图片.'
               '\n  按回车键以开始处理.'
               '\n  ')
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

    if mode == '1':
        for path in paths:
            if path.suffix == '.gif':
                gif_dir_path = path.parent / path.stem
                gif_dir_path.mkdir(exist_ok=True)

                settings = Settings().ask(path, True, True)
                cut(path, settings, gif_dir_path)
                with open(f'{skill_path / settings.name}.yml', 'w', encoding='utf-8') as yml:
                    i = 0
                    for _path in gif_dir_path.glob('*' + settings.suffix):
                        yml.write(f'{settings.name + str(i).zfill(4)}:\n    Skills:\n'
                                  + '\n'.join(build(_path, settings)) + '\n')
                        i += 1
                    yml.write(f'{settings.name}:\n    Skills:\n')
                    for j in range(0, i):
                        yml.write('    - skill{s=%s}\n    - delay %s\n'
                                  % (settings.name + str(j).zfill(4), settings.delay))
            else:
                settings = Settings().ask(path, True)
                with open(f'{skill_path / settings.name}.yml', 'w', encoding='utf-8') as yml:
                    yml.write(f'{settings.name}:\n    Skills:\n' + '\n'.join(build(path, settings)) + '\n')

    else:
        settings = Settings(gif_mode=gif_mode, batch=True).ask(gif_mode=True, batch=True)
        with open(f'{skill_path / settings.name}.yml', 'w', encoding='utf-8') as yml:
            i = 0
            for path in paths:
                if path.suffix == '.gif':
                    gif_dir_path = path.parent / path.stem
                    gif_dir_path.mkdir(exist_ok=True)
                    cut(path, settings, gif_dir_path)

                    for _path in gif_dir_path.glob('*' + settings.suffix):
                        yml.write(f'{settings.name + str(i).zfill(4)}:\n    Skills:\n'
                                  + '\n'.join(build(_path, settings)) + '\n')
                        i += 1
                else:
                    yml.write(f'{settings.name + str(i).zfill(4)}:\n    Skills:\n'
                              + '\n'.join(build(path, settings)) + '\n')
                    i += 1
            yml.write(f'{settings.name}:\n    Skills:\n')
            for j in range(0, i):
                yml.write('    - skill{s=%s}\n    - delay %s\n'
                          % (settings.name + str(j).zfill(4), settings.global_delay))

    input('\n  所有图片处理完成.\n  按回车键以退出...')
