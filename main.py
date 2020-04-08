from os import system
from pathlib import Path


def title():
    system('cls')
    print('\n  NeverMindMythicPicture v2.4'
          '\n  Author: Hodo7am, Zyyans.'
          '\n  ')


title()
dir_path = Path.cwd() / 'Pictures'
dir_path.mkdir(exist_ok=True)
input('  初始化完成.'
      '\n  请在 Pictures 文件夹中放入你需要处理的图片.'
      '\n  仅支持 JPG, PNG 和 GIF 格式的图片.'
      '\n  按回车键以继续.'
      '\n  ')

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
             '\n     * 顺序 - 第一关键字: 后缀名(JPG, PNG, GIF), 第二优先级: 字典序.'
             '\n  请输入你需要的处理模式 >> ')
while True:
    if mode in ['1', '2']:
        break
    else:
        mode = input('  输入有误, 请重新输入 >> ')
