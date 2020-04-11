from os import system


def title():
    system('cls')
    print('\n  NeverMindMythicPicture v2.4\n  Author: Hodo7am, Zyyans.\n  ')


class PictureSettings:

    def __init__(self, gif=False, batch=False):

        self.name = 'Honoka'
        self.particle = 'reddust'
        self.magic = 1
        self.magic_scale = False
        self.type = '1'
        self.face = 'E'
        self.density = 1
        self.clarity = 1
        self.ignore = []

        if gif:
            self.suffix = '.jpg'
            self.delay = '2'
            self.scale = 1

        if batch:
            self.global_delay = '2'

    def ask(self, path=None, gif=False, batch=False):

        title()

        if path:
            print(f'  正在处理图片 {path.name}\n')

        self.name = input('  请输入你想要的技能名称 >> ')
        while not self.name:
            self.name = input('  输入有误, 请重新输入 >> ')

        temp = input('\n  * 请自行确认粒子名称的正确性.'
                     '\n    直接按下回车键以使用默认粒子(reddust).'
                     '\n  请输入你想要使用的粒子 >> ')
        if temp:
            self.particle = temp

        title()

        temp = input('\n  * 像素化: 将原图指定尺寸的像素块中所有像素的颜色全部取为该像素块中出现频率最高的颜色.'
                     '\n            请输入指定尺寸的面积的算术平方根.'
                     '\n            例: 输入 2, 则每 4(2*2) 个像素会被取为同一颜色.'
                     '\n    直接按下回车键以跳过该步骤.'
                     '\n  请输入 >> ')
        while temp and not temp.isdigit():
            temp = input('  输入有误, 请重新输入 >> ')
        if temp and not temp == '1':
            self.magic = int(temp)
            temp = input('\n  * 像素化缩放: 在进行像素化操作后, 将多个同色像素压缩为一个, 以达到缩小图片尺寸而不产生杂色的目的.' 
                         '\n    输入任意内容以开启像素化缩放.'
                         '\n    直接按下回车键以关闭像素化缩放.'
                         '\n  请输入 >> ')
            if temp:
                self.magic_scale = True

        title()

        self.type = input('  1. 水平.\n  2. 竖直.\n  请输入你想要的技能类型的代号 >> ')
        while self.type not in ['1', '2']:
            self.type = input('  输入有误, 请重新输入 >> ')

        temp = '底部' if self.type == '1' else '正面'
        self.face = input(f'\n  * 朝向: 图片的{temp}对应的游戏内方向.'
                           '\n          请输入相应的字母: E(东), W(西), S(南), N(北).'
                           '\n  请输入你想要的图片朝向 >> ')
        while self.face not in ['E', 'W', 'S', 'N']:
            self.face = input('  输入有误, 请重新输入 >> ')

        title()

        temp = input('  * 密度: 相邻粒子之间的距离(默认为 0.1).'
                     '\n          例: 输入 2, 则相邻粒子之间的距离为 0.2.'
                     '\n  请输入粒子的密度 >> ')
        while not temp.isdigit():
            temp = input('  输入有误, 请重新输入 >> ')
        self.density = int(temp)

        temp = input('\n  * 清晰度: 图片像素数与技能像素数的比值的算术平方根.'
                     '\n            例: 输入 2, 则每 4(2*2) 个像素只会转化为 1 个粒子.'
                     '\n                输入 1, 则每个像素都会转化为粒子.'
                     '\n  请输入您想要的清晰度 >> ')
        while not temp.isdigit():
            temp = input('  输入有误, 请重新输入 >> ')
        self.clarity = int(temp)

        temp = input('\n  * 本软件自动忽略 PNG 图片的透明像素.'
                     '\n    如果你需要忽略其他颜色的像素, 请按格式输入指定的 RGB 颜色, 多个颜色之间用半角逗号隔开.'
                     '\n    例: #39C5BB, #FFA500, #FFE211, #FFC0CB, #D80000, #0000FF'
                     '\n    直接按下回车键以跳过.'
                     '\n  请输入你需要忽略的像素的颜色 >> ')
        while temp:
            temp = [color.strip() for color in temp.split(',')]
            legal = True
            for color in temp:
                if len(color) != 7 or not color.startswith('#'):
                    legal = False
                    break
                for char in color[1:]:
                    if ord(char) not in range(48, 58) and ord(char) not in range(65, 91):
                        legal = False
                        break
            if legal:
                self.ignore = temp
                break
            else:
                temp = input('  输入有误, 请重新输入 >> ')

        if not gif:
            return self

        title()

        temp = input('  1. JPG.\n  2. PNG.\n  请输入你想要的 GIF 分解后图片格式的代号 >> ')
        while temp not in ['1', '2']:
            temp = input('  输入有误, 请重新输入 >> ')
        self.suffix = '.jpg' if temp == '1' else '.png'

        if not batch:
            self.delay = input('\n  请输入 GIF 技能中每张图片的间隔时间(单位: tick) >> ')
            while not self.delay.isdigit():
                self.delay = input('  输入有误, 请重新输入 >> ')

        temp = input('\n  * 缩放比例: 图片面积与技能面积的比值的算术平方根, 可以为小数.'
                     '\n              例: 输入 2, 则 1920 * 1080 的图片将会被转化为 960 * 540 的技能.'
                     '\n  请输入你需要的缩放比例 >> ')
        while temp.count('.') > 1 or not temp.replace('.', '').isdigit():
            temp = input('  输入有误, 请重新输入 >> ')
        self.scale = float(temp)

        if not batch:
            return self

        title()

        self.global_delay = input('  请输入每个技能之间的间隔时间(单位: tick) >> ')
        while not self.global_delay.isdigit():
            self.global_delay = input('  输入有误, 请重新输入 >> ')


class TextureSettings:

    def __init__(self):

        self.name = 'Honoka'
        self.particle = 'reddust'
        self.size = 1
        self.scale = 1
        self.density = 1

    def ask(self, path):

        title()
        print(f'  正在处理模型 {path.stem}.')

        self.name = input('\n  请输入你想要的技能名称 >> ')
        while not self.name:
            self.name = input('  输入有误, 请重新输入 >> ')

        temp = input('\n  * 请自行确认粒子名称的正确性.'
                     '\n    直接按下回车键以使用默认粒子(reddust).'
                     '\n  请输入你想要使用的粒子 >> ')
        if temp:
            self.particle = temp

        title()

        temp = input('  请输入单个 voxel 的边长 >> ')
        while temp.count('.') > 1 or not temp.replace('.', '').isdigit():
            temp = input('  输入有误, 请重新输入 >> ')
        self.size = float(temp)

        temp = input('\n  例: uvgrid 为 64x64, PNG 图片尺寸为 32x32, 则输入 2.'
                     '\n  请输入 uvgrid 与 PNG 图片边长的比值 >> ')
        while not temp.isdigit():
            temp = input('  输入有误, 请重新输入 >> ')
        self.scale = int(temp)

        temp = input('\n  * 密度: 相邻粒子之间的距离(默认为 0.1).'
                     '\n          例: 输入 2, 则相邻粒子之间的距离为 0.2.'
                     '\n  请输入粒子的密度 >> ')
        while not temp.isdigit():
            temp = input('  输入有误, 请重新输入 >> ')
        self.density = int(temp)

        return self
