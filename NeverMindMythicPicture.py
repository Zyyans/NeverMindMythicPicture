from pathlib import Path
from os import walk as os_walk

from PIL.Image import Image
from PIL.Image import open as image_open
from PIL.JpegImagePlugin import JpegImageFile

# NeverMindMythicPicture v2.1
# Author: Hodo7am, Zyyans

def get_pixel(picture_path):
    # 图片信息获取
    temp = image_open(picture_path).convert('RGB')
    pixel = temp.load()
    temp.close()
    return pixel

def get_pixel_color(pixel, pixel_x, pixel_y):
    # 像素获取颜色
    temp = pixel[pixel_x, pixel_y]
    pixel_color = '#'
    for iterator in temp:
        pixel_color += str(hex(int(iterator)))[-2:].replace('x', '0').upper()
    return pixel_color

def get_picture_list():
    # 获取路径下所有图片, 增强图片兼容性
    temp = []
    for root, dirs, files in os_walk("./Pictures/"):
        temp = [file for file in files]
        print("  已找到的图片如下\n ", temp)
    return temp

def skill_make(skill_face, skill_clarity, pixel, pixel_size_x, pixel_size_y):
    skill_list = []
    skill = "    - Effect:Particles{a=1;c=%s;forwardOffset=%s;sideOffset=%s}"

    for pixel_x in range(pixel_size_x):
        if not pixel_x % skill_clarity:
            for pixel_y in range(pixel_size_y):
                if not pixel_y % skill_clarity:

                    pixel_color = get_pixel_color(pixel, pixel_x, pixel_y)
                    if picture_path[-3:] == "png" and pixel_color == "#FFFFFF":
                        continue

                    skill_fo = skill_so = 0
                    if skill_face == 'E':
                        skill_fo = round((pixel_size_x / 2 - pixel_x) / 10, 1)
                        skill_so = round((pixel_size_y / 2 - pixel_y) / 10, 1)
                    elif skill_face == 'W':
                        skill_fo = round((pixel_x - pixel_size_x / 2) / 10, 1)
                        skill_so = round((pixel_y - pixel_size_y / 2) / 10, 1)
                    elif skill_face == 'S':
                        skill_fo = round((pixel_y - pixel_size_y / 2) / 10, 1)
                        skill_so = round((pixel_size_y / 2 - pixel_x) / 10, 1)
                    else:
                        skill_fo = round((pixel_size_x / 2 - pixel_y) / 10, 1)
                        skill_so = round((pixel_x - pixel_size_x / 2) / 10, 1)

                    skill_list.append(skill %
                        (pixel_color, str(skill_fo), str(skill_so)))

    return skill_list

def skill_write(skill_name, skill_list):
    skill_string = "\n".join(skill_list)
    with open(skill_name + ".yml", 'w') as skill_text:
        skill_text.write("\n%s:\n    Skills:\n" % skill_name)
        skill_text.write(skill_string)
    input("\n  技能%s文本输出完成" % skill_name + "\n  按回车键以继续")



if __name__ == '__main__':

    print("\n  NeverMindMythicPicture v2.1\n  Author: Hodo7am, Zyyans")

    path = Path.cwd()
    input("\n  请将图片放入与本软件同目录的Pictures文件夹\
        \n  按回车键开始处理图片")
    picture_list = get_picture_list()

    if picture_list == []:
        print("\n  未找到任何图片, 程序结束")

    for picture in picture_list:

        skill_name = input("\n  正在处理图片" + picture + "\n  技能的名称是?\
            \n  > ")

        print("\n  说明:\n  图片朝向指图片底部对应的游戏内的方向(东西南北)\
            \n  请输入相应的字母 E(东) W(西) S(南) N(北)\n\n  图片的朝向是?")
        while True:
            skill_face = input("  > ")
            if skill_face in ['E', 'W', 'S', 'N']:
                break
            else:
                print("  ! 格式有误, 请重新输入")

        print("\n 正在处理本张图片")
        global picture_path
        picture_path = './Pictures/%s' % picture
        temp = image_open(picture_path)
        pixel = get_pixel(picture_path)
        pixel_size_x = temp.size[0]
        pixel_size_y = temp.size[1]
        temp.close()
        print("  尺寸 宽: %d 像素, 高: %d 像素" % (pixel_size_x, pixel_size_y))
        
        print("\n  说明\n  技能清晰度指图片像素数与技能像素数的比值\
            \n  1指技能清晰度为原图片的100%, 2指50%, 3指33%\
            \n  png图片的纯白色像素会被自动忽略  \n\n  技能的清晰度是(1-3)?")
        while True:
            skill_clarity = input("  > ")
            if skill_clarity in ['1', '2', '3']:
                break
            else:
                print("  ! 格式有误, 请重新输入")

        skill_write(skill_name, skill_make(skill_face, int(skill_clarity),
            pixel, pixel_size_x , pixel_size_y))
