from pathlib import Path

print("\n  NeverMindMythicPicture v2.3\n  Author: Hodo7am, Zyyans")

picture_dir_path = Path.cwd()/"Pictures"
picture_dir_path.mkdir(exist_ok=True)
input("\n  请将需要处理的图片放入Pictures文件夹内.\
    \n  本软件仅支持JPG, PNG, GIF格式的图片.\n  按回车键以继续...")
print('\n', end='  ')

while True:
    picture_path_list = picture_dir_path.glob("*.*['jpg', 'png', 'gif']*")
    picture_sum = 0
    for picture_path in picture_path_list:
        picture_sum += 1
    if picture_sum == 0:
        input("未找到任何图片.\n  按回车键以再次查找...")
        print('\n', end='  ')
    else:
        print("\n  已找到%d张图片.\n  按回车键以开始处理..." % picture_sum)
        break

mode = input("\n  1.普通模式: 以不同参数分别处理每张图片.\
    \n  2.批量模式: 以相同的参数处理所有图片, 并整合在同一技能组中.\
    \n  请选择您想要的处理模式 >> ")
