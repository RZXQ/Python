# 第九课
# bossDamage
# 显示结果页面
# 梳理数据类型都有啥
# 来几个数据类型的 控制台练习

import os
import random
import sys

import pygame

# 初始化及背景显示
pygame.init()
screen = pygame.display.set_mode((1000, 700))
# 字体设置
font = pygame.font.SysFont('simhei', 20)
#######单人角色属性字典，
playerData = {
    'def': 50,
    'atk': 100,
    'addHP': 200,
    'addAtk': 200,
    'addDef': 100,
    'magic': 1000,
    'HP': 1000,
    'maxHP': 1000,

}
# boss属性字典
bossData = {
    # 'atk': 300,
    'def': 50,
    'ice': 100,  # 魔法攻击1 ice
    'earth': 200,  # 魔法攻击2 earth
    'fire': 300,  # 魔法攻击3 fire
    'wind': 400,  # 魔法攻击4 wind
    'HP': 10000,

}


# 插入排序
def insertSort(mylist):
    for i in range(1, len(mylist)):
        for j in range(i, 0, -1):
            if mylist[j] < mylist[j - 1]:
                mylist[j - 1], mylist[j] = mylist[j], mylist[j - 1]
            else:
                break


# 构建动画字典，返回值是动画字典
def createDict(path):
    # 获取文件夹名字
    keys = os.listdir(path)  # print()列表
    # 以文件夹名字列表构建字典
    # 小练习，给一个带重复元素的列表让孩子建字典，加深key唯一性记忆，引出集合（列表变集合set方法）总结数据类型。
    gameDict = dict.fromkeys(keys)  # print()空字典
    # 字典赋值
    for key in keys:
        pictures = []  # 临时列表，每次执行for时，会清空
        # 获取图片的名字（全名包括扩展名）
        names = os.listdir(path + key + '/')
        # 把图片变量存在picture列表中
        for i in range(len(names)):
            names[i] = int(names[i].replace('.png', ''))
        print(names)
        insertSort(names)
        print(names)
        for name in names:
            # 把.png拼上
            img = pygame.image.load(path + key + '/' + str(name) + '.png')  # convert可以去掉
            pictures.append(img)
        # 把动画序列帧列表存在字典相应的KEY值中
        gameDict[key] = pictures
    return gameDict


# 绘制单独角色UI函数，角色字典名，坐标x，y
def showHP(x, y, hp, name):  # x,y固定值
    # 绘制生命条 ratio百分比，血条宽100xp， 高13px rect（）查
    if name == 'player':
        ratio = int(0.1 * hp)  # 0.1 = 100/1000，ratio不能为小数，否则缩放函数报错
    elif name == 'boss':
        ratio = int(0.01 * hp)
    # 保证血条，不能为负值。
    if ratio < 0:
        ratio = 0
    # 缩放图片，参数：图片变量；缩放的像素大小
    bar = pygame.transform.scale(uiDict['HPbar'][0], (ratio, 13))
    screen.blit(bar, (x, y))


# 绘制角色，字典名，文件夹名，状态帧，frame全局变量在递增
def showActor(dict, file, pos=(0, 0)):
    global player, boss
    list = dict[file]
    # 获取文件夹下有多少张图片
    num = len(list)

    if dict == playerDict:  # print 验证相当
        if player >= num:
            player = 0
        screen.blit(list[player], pos)
        player += 1
    else:
        if boss >= num:
            boss = 0
        screen.blit(list[boss], pos)
        boss += 1


# 显示人物属性
def showData(dict):
    global offset
    if dict == playerData:
        x = 260
        gap = 21  # n.缺口;差距;间隙;间隔;开口;豁口;裂口;间断;分歧;隔阂
    else:
        x = 700
        gap = 25
    for k, v in dict.items():
        if k != 'maxHP':
            words = k + ':' + str(v)
            text = font.render(words, True, 'black')
            screen.blit(text, (x, 516 + offset * gap))
            offset += 1
    offset = 0


# 玩家计算
def playerDamage(playerState):
    global bossData, playerData
    if playerState == 'attack':
        # 剩余生命计算
        damage = (playerData['atk'] - bossData['def'])
        bossData['HP'] -= damage
    elif playerState == 'magic':
        damage = (playerData['magic'] - bossData['def'])
        bossData['HP'] -= damage
    # 生命恢复
    elif playerState == 'addHP':
        # 保证血条、生命值不超过上限
        if playerData['HP'] < playerData['maxHP']:  # 满血不加
            playerData['HP'] = playerData['HP'] + playerData['addHP']
            if playerData['HP'] > playerData['maxHP']:  # 不满血，加完了超上限，限制
                playerData['HP'] = playerData['maxHP']
    elif playerState == 'addDef':
        playerData['def'] += playerData['addDef']
    elif playerState == 'addAtk':
        playerData['atk'] += playerData['addAtk']
    print(bossData['HP'])


# boss伤害
def bossDamage():
    global bossData, playerData, randomSkill
    damage = (bossData[randomSkill] - playerData['def'])
    if damage > 0:
        playerData['HP'] -= damage
    print(playerData['HP'])


state = 'loading'
turn = 'player'
choose = 'doing'
# 技能选择列表
panel = 0

# 动画状态帧
player = 0
boss = 0

playerState = 'idle'
randomSkill = 'ice'
offset = 0
while True:
    if state == 'loading':
        # 资源加载（更换图片）
        uiDict = createDict('UI/')
        screen.blit(uiDict['start'][0], (0, 0))
        pygame.display.update()

        playerDict = createDict('animation/player/')
        screen.blit(uiDict['start'][1], (0, 0))
        pygame.display.update()

        bossDict = createDict('animation/boss/')
        screen.blit(uiDict['start'][3], (0, 0))
        pygame.display.update()

        pygame.time.delay(500)
        state = 'start'
    if state == 'start':
        # 显示开始界面,按enter或者小键盘enter按键进入游戏
        screen.blit(uiDict['start'][4], (0, 0))

    if state == 'running':
        # 绘制背景
        screen.blit(uiDict['map'][panel], (0, 0))
        # 显示面板UI
        showHP(86, 642, playerData['HP'], 'player')
        showHP(818, 642, bossData['HP'], 'boss')
        # 显示属性
        showData(playerData)
        showData(bossData)
        # 回合判断，也就播放相应的动画，玩家orBOSS
        if turn == 'player':  # 玩家回合
            # 玩家选择完成开始

            if choose == 'doing':
                showActor(playerDict, 'idle')
                showActor(bossDict, 'idle')
            else:

                # BOSS为闲置动画
                showActor(bossDict, 'idle')
                # 玩家技能播放
                showActor(playerDict, playerState)

                num = len(playerDict[playerState])
                if player >= num:
                    # 动画帧清零，也可清零1,2动画帧，1动画帧保证idle动画从0开始，2动画帧保证gun的攻击动画从零开始
                    playerDamage(playerState)
                    randomSkill = random.choice(['ice', 'earth', 'fire', 'wind'])
                    turn = 'boss'

        # boss回合
        elif turn == 'boss':

            # player为闲置动画
            showActor(playerDict, 'idle')

            showActor(bossDict, randomSkill)
            num = len(bossDict[randomSkill])
            if boss >= num:
                # boss伤害
                bossDamage()
                choose = 'doing'
                turn = 'player'

        if playerData['HP'] <= 0 or bossData['HP'] <= 0:
            # 双方任意一方没血，结束游戏
            state = 'end'

    # 结束状态，显示胜利或者失败
    if state == 'end':
        if playerData['HP'] <= 0:
            screen.blit(uiDict['end'][0], (0, 0))
        elif bossData['HP'] <= 0:
            screen.blit(uiDict['end'][1], (0, 0))
    # 全局更新
    pygame.display.update()
    pygame.time.delay(100)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
        if e.type == pygame.KEYDOWN:
            # 回车键进入游戏
            if e.key == pygame.K_KP_ENTER or e.key == pygame.K_RETURN:
                state = 'running'
                # 空格键选择完毕
            if e.key == pygame.K_SPACE:
                choose = 'done'

        if e.type == pygame.MOUSEBUTTONDOWN:
            if choose == 'doing':
                x = e.pos[0]
                y = e.pos[1]
                # 点击区域判断
                print(x, y)
                if 450 < y < 490:  # 根据UI改
                    # y坐标判断
                    if 270 < x < 340:
                        playerState = 'attack'  # 5个
                        panel = 1  # 12345 六张图
                    elif 370 < x < 440:
                        playerState = 'magic'  # 5个
                        panel = 2
                    elif 470 < x < 540:
                        playerState = 'addHP'  # 5个
                        panel = 3
                    elif 570 < x < 640:
                        playerState = 'addAtk'  # 5个
                        panel = 4
                    elif 670 < x < 740:
                        playerState = 'addDef'  # 5个
                        panel = 5
