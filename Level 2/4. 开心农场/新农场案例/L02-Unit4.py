import os
import pickle
import platform
import random
import sys
import time

import pygame

# 生成随机价格，别忘了导如random库

# pygame初始化及设置
pygame.init()
screen = pygame.display.set_mode((1000, 700))
pygame.mouse.set_visible(False)

# 字体设置
# windows字体    fangsong        simhei       kaiti
# macOS字体      arialunicode    pingfang     songti
# 根据系统选择字体
osName = platform.system()
print(osName)
if osName == 'Windows':
    font = pygame.font.SysFont('simhei', 28)
elif osName == 'macOS':
    font = pygame.font.SysFont('songti', 28)


# 插入排序函数
def insertSort(mylist):
    for i in range(1, len(mylist)):
        for j in range(i, 0, -1):
            if mylist[j] < mylist[j - 1]:
                mylist[j], mylist[j - 1] = mylist[j - 1], mylist[j]
            else:
                break


# 构建动画字典，返回值是动画字典
def createDict(path):
    keys = os.listdir(path)
    gameDict = dict.fromkeys(keys)
    for key in keys:
        gameDict[key] = []
        names = os.listdir(path + key + '/')
        for i in range(len(names)):
            names[i] = int(names[i].replace('.png', ''))
        insertSort(names)
        for name in names:
            img = pygame.image.load(path + key + '/' + str(name) + '.png')
            gameDict[key].append(img)
    return gameDict


# 资源加载
UIDict = createDict('images/UI/')
candyDict = createDict('images/candy/')
iconDict = createDict('images/icon/')

# 土地字典
soilDict = {'soil1': {'name': 'blank', 'pos': (190, 330), 'time': 0},
            'soil2': {'name': 'blank', 'pos': (545, 330), 'time': 0},
            'soil3': {'name': 'blank', 'pos': (360, 240), 'time': 0},
            'soil4': {'name': 'blank', 'pos': (370, 425), 'time': 0}
            }

# 仓库字典
plygoods = {'c0': 5, 'c1': 5, 'c2': 5, 'c3': 5, 'c4': 5, 'c5': 5, 'c6': 5}

# 糖果信息字典
candyUI = {
    'c0': {'name': '棉花糖', 'pic': iconDict['big'][0], 'pic1': iconDict['small'][0],
           'text': '甜美柔软的棉花状糖果,入口即化。', 'price': 10},
    'c1': {'name': '棒棒糖', 'pic': iconDict['big'][1], 'pic1': iconDict['small'][1],
           'text': '五颜六色的糖果，口味丰富。', 'price': 9},
    'c2': {'name': '彩虹糖', 'pic': iconDict['big'][2], 'pic1': iconDict['small'][2],
           'text': '五彩缤纷的小糖果，味道鲜美。', 'price': 8},
    'c3': {'name': '流心面包', 'pic': iconDict['big'][3], 'pic1': iconDict['small'][3],
           'text': '鲜奶油和巧克力混合的面包，外酥里软。', 'price': 7},
    'c4': {'name': '生巧泡芙', 'pic': iconDict['big'][4], 'pic1': iconDict['small'][4],
           'text': '口感轻盈的泡芙，内陷丝滑的巧克力酱。', 'price': 6},
    'c5': {'name': '樱桃蛋糕', 'pic': iconDict['big'][5], 'pic1': iconDict['small'][5],
           'text': '口感细腻的蛋糕，上面点缀着美味的樱桃。', 'price': 5},
    'c6': {'name': '焦糖布丁', 'pic': iconDict['big'][6], 'pic1': iconDict['small'][6],
           'text': '香气四溢的甜点，带有焦糖的独特风味。', 'price': 4}
}


# 绘制糖果树
def drawCandy():
    for crop in soilDict.values():
        k = crop['name']
        p = crop['pos']
        # 作物生长
        level = (time.time() - crop['time']) // 2
        if level > 3:
            level = 3
        screen.blit(candyDict[k][int(level)], p)


# 道具功能
candyName = 'c0'
pointer = UIDict['pointer'][0]
tool = ''


def prop(n):
    global pointer, tool
    if soilDict[n]['name'] == 'blank':
        if tool == '糖果':
            soilDict[n]['name'] = candyName
            soilDict[n]['time'] = time.time()
            plygoods[candyName] -= 1
            pointer = UIDict['pointer'][0]
            tool = ''
    else:
        if tool == '铲子':
            soilDict[n]['name'] = 'blank'
        elif tool == '手':
            level = (time.time() - soilDict[n]['time']) // 2
            if level >= 3:
                plygoods[soilDict[n]['name']] += 4
                soilDict[n]['name'] = 'blank'
    print(plygoods)


# 绘制主界面界面UI
gold = 1000


def showUI():
    # 种植的种子图标
    if plygoods[candyName] > 0:
        screen.blit(candyUI[candyName]['pic1'], (860, 595))
    datetime = time.strftime("%H:%M:%S", time.localtime())
    fs = font.render(datetime, True, 'white')
    screen.blit(fs, (60, 14))
    fs = font.render(str(gold), True, 'white')
    screen.blit(fs, (290, 14))


menu = 0
goods = list(plygoods.keys())
tab = 0
ck = 'c0'


# 随机生成糖果价格
def randomPrice():
    p = [random.randint(1, 10) for i in range(7)]
    print(p)
    p.sort(reverse=True)
    print(p)
    k = [i['name'] for i in candyUI.values()]
    random.shuffle(k)
    print(k)
    return list(zip(k, p))


prices = randomPrice()
print(prices)
click = None
buy = 20

soldText = {}

g = 0


# 售卖策略
def greedy():
    global buy, gold, g
    dict1 = {candyUI[key]['name']: key for key, value in candyUI.items()}
    # print(dict1)
    b = buy
    g = 0
    for name, price in prices:
        key = dict1[name]
        if b >= plygoods[key]:
            b = b - plygoods[key]
            g = g + price * plygoods[key]
            # print(f"卖出了{name}{plygoods[key]}个")
            soldText[name] = plygoods[key]
            plygoods[key] = 0
        else:
            g = g + price * b
            # print(f"卖出了{name}{b}个")
            soldText[name] = b
            plygoods[key] = plygoods[key] - b
            break
    gold += g
    print(soldText)


# 绘制菜单页
def drawMenu():
    global click, prices, g
    screen.blit(UIDict['scene'][tab], (0, 0))
    # 买入
    if tab == 0:
        # 糖果图片
        screen.blit(candyUI[ck]['pic'], (445, 350))
        # 糖果名称
        fs = font.render(candyUI[ck]['name'], True, 'white')
        screen.blit(fs, (450, 250))
        # 糖果价格
        t = '售价: ' + str(candyUI[ck]['price']) + '个金币'
        fs = font.render(t, True, 'brown')
        screen.blit(fs, (530, 495))
        # 糖果介绍
        t = candyUI[ck]['text']
        # 描述文本自适应行数
        n = 0
        for i in range(0, len(t), 8):
            fs = font.render(t[i:i + 8], True, 'brown')
            screen.blit(fs, (600, 320 + (i / 8) * 30))
            n += 1

    # 卖出
    elif tab == 1:
        if click == None:
            # 绘制按键图标
            screen.blit(UIDict['button'][0], (0, 0))
            # 绘制收购标题
            t1 = f'预计采购{str(buy)}个水果'
            fs = font.render(t1, True, 'brown')
            screen.blit(fs, (400, 315))
            # 绘制收购价格清单
            x, i = 400, 0
            for name, price in prices:
                fs = font.render(f'{name}{price}元/个', True, 'brown')
                screen.blit(fs, (x, 360 + i * 32))
                i += 1
                if i == 4:
                    x = 650
                    i = 0
        elif click == 'accept':
            t1 = '收购水果清单'
            fs = font.render(t1, True, 'brown')
            screen.blit(fs, (400, 315))
            # 绘制收购价格清单
            x, i = 400, 0
            for name, price in soldText.items():
                if price > 0:
                    fs = font.render(f'{name}{price}个', True, 'brown')
                    screen.blit(fs, (x, 360 + i * 32))
                    i += 1
                    if i == 4:
                        x = 650
                        i = 0
            t1 = f'共计收入{g}元'
            fs = font.render(t1, True, 'brown')
            screen.blit(fs, (400, 500))
        elif click == 'cancel':
            now = time.time()
            timeLeft = 5 - (now - start)
            if timeLeft <= 0:
                click = None
                prices = randomPrice()
            else:
                fs = font.render(f'下次收购时间倒计时：{int(timeLeft)}秒', True, 'white')
                screen.blit(fs, (500, 450))
    # 仓库
    elif tab == 2:
        i = 0
        for k in goods[0:4]:
            screen.blit(candyUI[k]['pic'], (95 + i * 235, 365))
            fs = font.render(candyUI[k]['name'], True, 'white')
            screen.blit(fs, (90 + i * 235, 260))
            fs = font.render(str(plygoods[k]) + ' 个', True, 'brown')
            screen.blit(fs, (120 + i * 235, 510))
            i += 1


# 保存
def save():
    with open('game.pkl', 'wb') as f:
        game = [plygoods, soilDict, gold]
        pickle.dump(game, f)


# 读取
def load():
    global gold
    with open('game.pkl', 'rb') as f:
        game = pickle.load(f)
        plygoods.update(game[0])
        soilDict.update(game[1])
        gold = game[2]


# 异常处理
try:
    load()
    print('存档读取成功')
except:
    save()
    print('存档读取失败，以重新创建')

load()

x, y = 0, 0
candyIndex = 0
candyKeys = list(candyUI.keys())
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            save()
            sys.exit()
        elif e.type == pygame.MOUSEMOTION:
            x = e.pos[0]
            y = e.pos[1]
        elif e.type == pygame.MOUSEBUTTONDOWN:
            if menu == 1:
                # 菜单关闭功能
                if 900 < x < 935 and 70 < y < 105:
                    menu = 0
                    # 选项卡功能
                elif 140 < y < 225:
                    if 40 < x < 130:
                        tab = 0
                    elif 150 < x < 230:
                        tab = 1
                    elif 250 < x < 340:
                        tab = 2
                if tab == 0:
                    if 550 < x < 735 and 565 < y < 610:
                        if gold - candyUI[ck]['price'] >= 0:
                            gold -= candyUI[ck]['price']
                            plygoods[ck] += 1
                    elif 400 < y < 470:
                        if 280 < x < 345:
                            candyIndex -= 1
                            if candyIndex < 0:
                                candyIndex = 6
                        elif 890 < x < 960:
                            candyIndex += 1
                            if candyIndex > 6:
                                candyIndex = 0
                        ck = candyKeys[candyIndex]

                elif tab == 1 and click == None:
                    if 565 < y < 615:
                        if 710 < x < 770:
                            click = 'cancel'
                            start = time.time()
                        elif 830 < x < 890:
                            greedy()
                            click = 'accept'


                # 滚轮翻页
                elif tab == 2:
                    if e.button == 5:
                        first = goods[0]
                        rest = goods[1:]
                        goods = rest + [first]
                    elif e.button == 4:
                        last = goods[-1]
                        rest = goods[:-1]
                        goods = [last] + rest
                        # 物品选择功能
                    elif e.button == 1:
                        if 325 < y < 500:
                            for i in range(4):
                                if 55 + i * (58 + 175) < x < 55 + 175 + i * (58 + 175):
                                    candyName = goods[i]
            elif menu == 0:
                if e.button == 1:
                    # 种植区域点击判断
                    if 390 < y < 490:
                        if 270 < x < 370:
                            prop('soil1')
                        elif 615 < x < 715:
                            prop('soil2')
                    elif 400 < x < 500:
                        if 290 < y < 390:
                            prop('soil3')
                        elif 480 < y < 580:
                            prop('soil4')
                    # 工具区域判断
                    elif 610 < y < 670:
                        if 660 < x < 720:
                            pointer = UIDict['pointer'][1]
                            tool = '铲子'
                        elif 765 < x < 825:
                            pointer = UIDict['pointer'][2]
                            tool = '手'
                        elif 870 < x < 930:
                            if plygoods[candyName] > 0:
                                pointer = candyUI[candyName]['pic1']
                                tool = '糖果'
                        elif 75 < x < 135:
                            menu = 1
                            pointer = UIDict['pointer'][0]
                            tool = '手指'
                elif e.button == 3:
                    pointer = UIDict['pointer'][0]
                    tool = '手指'
    # 绘制背景
    screen.blit(UIDict['map'][0], (0, 0))
    # 绘制糖果树
    drawCandy()
    # 绘制主界面UI
    showUI()
    # 绘制菜单页面
    if menu == 1:
        drawMenu()
    # 绘制鼠标样式
    screen.blit(pointer, (x - 30, y - 30))
    pygame.display.update()
