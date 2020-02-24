import message
from pathlib import Path

from PIL import Image

message = {
    "head": "\n  NeverMindMythicPicture v2.3\n  Author: Hodo7am, Zyyans.",
    "dirStr": "\n  请将需要处理的图片放入Pictures文件夹内.\n  本软件仅支持JPG, PNG和GIF格式的图片.\n  按回车键以继续...",
    "pathFoundStr": "\n  已找到%d张图片.\n  按回车键以开始处理...",
    "pathNotFoundStr": "\n  未找到任何图片.\n  按回车键以再次查找...",
    "modeStr": "\n  1.普通模式: 以不同参数分别处理每张图片.\n  2.批量模式: 以相同的参数处理所有图片, 并按字典序整合在同一技能组中.\n  请选择您想要的处理模式 >> ",
    "illegalStr": "  输入不合法, 请重新输入 >> ",
    "doneStr": "  技能生成完毕.",
    "allDoneStr": "\n  所有图片处理完毕.\n  按回车键以退出...",
    "nameStr": "\n  正在处理图片%s.\n  技能的名称 >> ",
    "subModeStr": "\n  1.水平.\n  2.垂直.\n  技能的类型 >> ",
    "faceStr": "\n  图片朝向指图片%s对应的游戏内的方向.\n  请输入相应的字母: E, W, S, N.\n  请选择您想要的图片朝向 >> ",
    "faceDict": {'1': "底部", '2': "正面"},
    "clarityStr": "\n  本张图片尺寸为: 宽%d像素, 高%d像素.\n  清晰度指图片像素数与技能像素数的比值的算术平方根(1-3).\n  请选择您想要的清晰度 >> ",
    "askDoneStr": "\n  参数设置已完成."
}


def ask(path):

    name = input(message["nameStr"] % path.name)

    mode = input(message["subModeStr"])
    while mode not in ['1', '2']:
        mode = input(message["illegalStr"])

    face = input(message["faceStr"] % message["faceDict"][mode])
    while face not in ['E', 'W', 'S', 'N']:
        face = input(message["illegalStr"])

    temp = Image.open(path).convert('RGB')
    pixel, sizeX, sizeY = temp.load(), temp.size[0], temp.size[1]
    temp.close()
    clarity = int(input(message["clarityStr"] % (sizeX, sizeY)))
    while clarity not in [1, 2, 3]:
        clarity = int(input(message["illegalStr"]))

    print(message["askDoneStr"])
    return name, face, pixel, sizeX, sizeY, clarity


def get_color(raw_color):
    color = '#'
    for value in raw_color:
        color += str(hex(int(value)))[-2:].replace('x', '0')
    return color.upper()


def build(path, name, face, pixel, sizeX, sizeY, clarity):
    text = "    - effect:particles{a=1;c=%s;forwardOffset=%s;sideOffset=%s}"
    textList = []
    for x in range(0, sizeX, clarity):
        for y in range(0, sizeY, clarity):
            color = get_color(pixel[x, y])
            if path.suffix == ".png" and color == "#FFFFFF":
                continue
            xo = yo = 0
            if face == 'E':
                xo = round((sizeX / 2 - x) / 10, 1)
                yo = round((sizeY / 2 - y) / 10, 1)
            elif face == 'W':
                xo = round((x - sizeX / 2) / 10, 1)
                yo = round((y - sizeY / 2) / 10, 1)
            elif face == 'S':
                xo = round((y - sizeY / 2) / 10, 1)
                yo = round((sizeY / 2 - x) / 10, 1)
            else:
                xo = round((sizeX / 2 - y) / 10, 1)
                yo = round((x - sizeX / 2) / 10, 1)
            textList.append(text % (color, str(xo), str(yo)))
    with open(name + ".yml", 'w') as yaml:
        yaml.write(name + ":\n    Skills:\n" + "\n".join(textList))


print(message["head"])

dirPath = Path.cwd() / "Pictures"
dirPath.mkdir(exist_ok=True)
input(message["dirStr"])

pathList = []
while True:
    pathList = [path for path in dirPath.glob("*.*['jpg', 'png', 'gif']*")]
    pathSum = len(pathList)
    if pathSum:
        input(message["pathFoundStr"] % pathSum)
        break
    else:
        input(message["pathNotFoundStr"])

mode = input(message["modeStr"])
while mode not in ['1', '2']:
    mode = input(message["illegalStr"])

if mode == '1':
    for path in pathList:
        build(path, *ask(path))
        print(message["doneStr"])
    input(message["allDoneStr"])
