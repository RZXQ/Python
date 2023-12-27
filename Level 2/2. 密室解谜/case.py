import random
import sys

import pygame

pygame.init()
screen = pygame.display.set_mode((1000, 700))

# 鼠标指针显示设置
pygame.mouse.set_visible(0)

# 图片名称列表
names = ['bg', 'for', 'list', 'random', 'function', 'box', 'lose', 'win', 'm0', 'm1']
# 图片存储列表
plist = []

# 文本
# 建立变量存字符串
t1 = '我找到了一张粉色纸条：'  # 预留
t2 = '这有一张蓝色卡片：'  # 预留
t3 = '绿色卡片给你：'  # 预留
t4 = '和我衣服样颜色的卡片：'  # 预留
talks = [t1, t2, t3, t4]  # 预留

# 字体设置
# windows字体    fangsong        simhei       kaiti
# macOS字体      arialunicode    pingfang     songti

# 字体设置
font = pygame.font.SysFont('simhei', 40)
# 箱子字体设置
font1 = pygame.font.SysFont('simhei', size=120)

# 图片加载
for name in names:
    pic = pygame.image.load('images/%s.png' % (name))
    plist.append(pic)

# 游戏资源加载
screen.blit(plist[0], (0, 0))
pygame.display.update()

offset = 0


# 文字显示
def showTalk(words):
    global offset
    for i in words:
        text = font.render(i, True, 'black')
        screen.blit(text, (330 + offset * 40, 570))
        pygame.display.update()
        pygame.time.delay(100)
        offset += 1
    offset = 0


# 动态密钥生成
key = ''


def createkey():
    global key
    binStr = ''
    for i in range(4):
        for j in range(4):
            binStr += random.choice(['0', '1'])
        talks[i] = talks[i] + binStr
        binStr = hex(int(binStr, 2))
        key += str(binStr)[-1]
        binStr = ''
    print(key)


actor = None
pwd = ''
# 生成随机密码
createkey()

while True:
    # 事件获取
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
        # 鼠标移动
        if e.type == pygame.MOUSEMOTION:
            # 界面刷新，每次移动鼠标都会绘制背景
            screen.blit(plist[0], (0, 0))
            x = e.pos[0]
            y = e.pos[1]
            print('点击鼠标时的x坐标是: % d, y坐标是 % s' % (x, y))
            # 鼠标位置区域判断
            if 130 < x < 200 and 300 < y < 400:
                actor = 'for'
            elif 220 < x < 320 and 80 < y < 180:
                actor = 'list'
            elif 650 < x < 750 and 150 < y < 210:
                actor = 'random'
            elif 720 < x < 820 and 320 < y < 420:
                actor = 'function'
            elif 400 < x < 620 and 300 < y < 450:
                actor = 'box'
            else:
                actor = None
            # 鼠标指针样式更改
            if actor == None:
                screen.blit(plist[-2], (x, y))
            else:
                screen.blit(plist[-1], (x, y))

            # pygame.display.update()
            # 输入密码重置
            pwd = ''
        # 鼠标点击事件
        if e.type == pygame.MOUSEBUTTONDOWN:
            # 人物线索显示
            if actor in names:
                screen.blit(plist[0], (0, 0))
                aIndex = names.index(actor)
                screen.blit(plist[aIndex], (0, 0))
                if actor != 'box':
                    showTalk(talks[aIndex - 1])
                pygame.display.update()
        # 键盘事件处理
        if e.type == pygame.KEYDOWN:
            if actor == 'box':
                # 非回车键，输入字母或者字符
                if e.key != 13:
                    pwd += chr(e.key)
                    text = font1.render(pwd, True, 'white')
                    screen.blit(plist[5], (0, 0))
                    screen.blit(text, (250, 280))
                # 回车键 判断密码
                else:
                    if pwd == key:
                        screen.blit(plist[-3], (0, 0))
                    else:
                        screen.blit(plist[-4], (0, 0))
                    pwd = ''
        pygame.display.update()
