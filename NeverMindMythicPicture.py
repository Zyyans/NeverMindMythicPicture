# -*- coding: utf-8 -*-

from pathlib import Path

from PIL import Image

msg = {
    "delay_text": "    - delay %s",
    "illegal": "  输入不合法, 请重新输入 >> ",
    "skill_part": ":\n    Skills:\n",
    "all_clarity": "\
        \n  清晰度指图片像素数与技能像素数的比值的算术平方根(1-3).\
        \n  请输入您想要的清晰度 >> ",
    "all_delay": "\
        \n  每个技能之间的延迟是(单位: 游戏刻) >> ",
    "all_done": "\
        \n  所有图片处理完毕.\
        \n  按回车键以退出...",
    "all_name": "\
        \n  请输入您想要的总技能组名称 >> ",
    "ask_done": "\
        \n  参数设置已完成.",
    "clarity": "\
        \n  本张图片尺寸为: 宽%d像素, 高%d像素.\
        \n  清晰度指图片像素数与技能像素数的比值的算术平方根(1-3).\
        \n  请输入您想要的清晰度 >> ",
    "delay": "\
        \n  每帧图片的技能之间的延迟是(单位: 游戏刻) >> ",
    "dir": "\
        \n  请将需要处理的图片放入Pictures文件夹内.\
        \n  本软件仅支持JPG, PNG和GIF格式的图片.\
        \n  按回车键以继续...",
    "done": "\
        \n  技能生成完毕.",
    "face": "\
        \n  图片朝向指图片%s对应的游戏内的方向.\
        \n  请输入相应的字母: E, W, S, N.\
        \n  请输入您想要的图片朝向 >> ",
    "head": "\
        \n  NeverMindMythicPicture v2.3.1\
        \n  Author: Hodo7am, Zyyans.\
        \n\
        \n  本软件将自动忽略PNG格式图片的纯白色像素.",
    "mode": "\
        \n  1.精确: 以不同参数分别处理每张图片.\
        \n  2.批量: 以相同参数按字典序处理所有图片, 并整合在同一技能组中(未完成).\
        \n  请输入您想要的处理模式 >> ",
    "name": "\
        \n  正在处理图片%s.\
        \n  请输入您想要的技能名称 >> ",
    "path_found": "\
        \n  已找到%d张图片.\
        \n  按回车键以开始处理...",
    "path_not_found": "\
        \n  未找到任何图片.\
        \n  按回车键以再次查找...",
    "scale": "\
        \n  本张图片尺寸为: 宽%d像素, 高%d像素.\
        \n  缩放比例指图片面积与技能面积的比值的算术平方根, 可带小数.\
        \n  请输入您想要的缩放比例 >> ",
    "sub_mode": "\
        \n  1.水平.\
        \n  2.竖直.\
        \n  请输入您想要的技能类型 >> ",
    "suffix": "\
        \n  检测到GIF图片.\
        \n  格式指将GIF图片切片后转化为JPG格式(1)或PNG格式(2).\
        \n  请输入您想要的格式的代号 >> ",
    "face_dict": {
        '1': "底部",
        '2': "正面"
    },
    "suffix_dict": {
        '1': "jpg",
        '2': "png"
    },
    "text_dict": {
        '1': "    - effect:particles{a=1;c=%s;forwardOffset=%.1f;sideOffset=%.1f}",
        '2': {
            "EW": "    - effect:particles{a=1;c=%s;forwardOffset=%.1f;yOffset=%.1f}",
            "SN": "    - effect:particles{a=1;c=%s;sideOffset=%.1f;yOffset=%.1f}"
        }
    },
}


def is_float(string):
    try:
        complex(string)
    except:
        return False
    return True


def get_color(raw_color):
    """获取颜色并转换格式."""
    color = '#'
    for value in raw_color[:-1]:
        color += str(hex(int(value)))[-2:].replace('x', '0')
    return color.upper()


def input_check(string, mode, condition=None):
    """检测输入, 限制输入内容."""
    target = input(string)
    while True:
        if (mode == "not_equal" and target != condition) or (
                mode == "in" and target != "" and target in condition) or (
                mode == "float" and is_float(target)) or (
                mode == "digit" and target.isdigit()):
            break
        else:
            target = input(msg["illegal"])
    return target


def get_pic_info(path):
    """获取图片的像素颜色和尺寸."""
    temp = Image.open(path).convert("RGBA")
    pixel, size_x, size_y = temp.load(), *temp.size
    temp.close()
    return pixel, size_x, size_y


def ask(path):
    """JPG, PNG格式图片参数设置."""
    temp = Image.open(path).convert("RGBA")
    size_x, size_y = temp.size[:2]
    temp.close()

    name = input_check(msg["name"] % path.name, "not_equal", "")
    mode = input_check(msg["sub_mode"], "in", "12")
    face = input_check(msg["face"] % msg["face_dict"][mode], "in", "EWSN")
    clarity = input_check(msg["clarity"] % (size_x, size_y), "in", "123")

    text = msg["text_dict"][mode]
    if mode == '2':
        text = text["EW"] if face == 'E' or face == 'W' else text["SN"]
    return name, mode, face, int(clarity), text


def gif_ask(pic_info, settings):
    """GIF格式图片参数设置."""
    size_x, size_y = pic_info[-2:]
    gif_dir_path = dir_path / path.stem
    gif_dir_path.mkdir(exist_ok=True)

    suffix = msg["suffix_dict"][input_check(msg["suffix"], "in", "12")]
    delay = input_check(msg["delay"], "digit")
    scale = float(input_check(msg["scale"] % (size_x, size_y), "float"))

    return gif_dir_path, suffix, delay, scale


def build(path, pixel, size_x, size_y, name, mode, face, clarity, text):
    """JPG, PNG格式图片技能生成."""
    text_list = []
    for x in range(0, size_x, clarity):
        for y in range(0, size_y, clarity):
            if not pixel[x, y][3]:
                continue
            color = get_color(pixel[x, y])
            if mode == '1': # 神奇代码, 别乱动.
                if face in "EW":
                    xo = round((size_x / 2 - x) / 10, 1)
                    yo = round((size_y / 2 - y) / 10, 1)
                else:
                    xo = round((y - size_y / 2) / 10, 1)
                    yo = round((size_y / 2 - x) / 10, 1)
                if face in "WN":
                    xo, yo = -xo, -yo
            else:
                xo = round((size_x / 2 - x) / 10, 1)
                yo = round((size_y / 2 - y) / 10, 1)
                if face in "WN":
                    xo = -xo
            text_list.append(text % (color, xo, yo))
    return text_list


def gif_build(path, pic_info, settings, gif_dir_path, suffix, delay, scale):
    """GIF图片切割, 生成技能并汇总."""
    size_x, size_y = pic_info[-2:]
    im = Image.open(path)

    try:
        i = 0
        while True:
            im.resize((round(size_x / scale), round(size_y / scale))).convert(
                "RGBA").save(gif_dir_path / (
                    "%s.%s" % (str(i).zfill(4), suffix)))
            i += 1
            im.seek(i)
    except EOFError:
        pass

    all_list = []
    gif_paths = [path for path in gif_dir_path.glob("*." + suffix)]
    for gif_path in gif_paths[1:]:
        text_list = build(gif_path, *get_pic_info(gif_path), *settings)
        all_list += text_list
        if gif_path != gif_paths[-1]:
            all_list.append(msg["delay_text"] % delay)
    return all_list


print(msg["head"])

dir_path = Path.cwd() / "Pictures"
dir_path.mkdir(exist_ok=True)
input(msg["dir"])

while True:
    jpg_paths = [path for path in dir_path.glob("*.jpg")]
    png_paths = [path for path in dir_path.glob("*.png")]
    gif_paths = [path for path in dir_path.glob("*.gif")]
    if len(gif_paths):
        gif_mode = 1
    paths = jpg_paths + png_paths + gif_paths
    path_sum = len(paths)
    if path_sum:
        input(msg["path_found"] % path_sum)
        break
    else:
        input(msg["path_not_found"])

mode = input_check(msg["mode"], "in", "12")

if mode == '1':
    for path in paths:
        settings = ask(path)
        name = settings[0]
        if path.suffix == ".gif":
            with open(name + ".yml", 'w') as yaml:
                yaml.write(name + msg["skill_part"] + '\n'.join(
                    gif_build(path, get_pic_info(path), settings, *gif_ask(
                        get_pic_info(path), settings))) + '\n')
        else:
            with open(name + ".yml", 'w') as yaml:
                yaml.write(name + msg["skill_part"] + '\n'.join(
                    build(path, *get_pic_info(path), *settings)) + '\n')
        print(msg["done"])
    input(msg["all_done"])
else:
    pass
