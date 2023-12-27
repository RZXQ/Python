import pygame

pygame.init()
import sys
import random

# 图片加载
screen = pygame.display.set_mode((1000, 700))
car = pygame.image.load("car.png")
car1 = pygame.image.load("car1.png")
car2 = pygame.image.load("car2.png")
cars = [car, car1, car2]
bg = pygame.image.load("bg.png")
block = pygame.image.load('block.png')
coin = pygame.image.load('coin.png')
l = pygame.image.load("lose.png")
w = pygame.image.load("win.png")
s = pygame.image.load("start.png")
hp0 = pygame.image.load('hp0.png')
hp1 = pygame.image.load('hp1.png')
hp2 = pygame.image.load('hp2.png')
hp3 = pygame.image.load('hp3.png')
hps = [hp0, hp1, hp2, hp3]
c0 = pygame.image.load('s0.png')
c1 = pygame.image.load('s1.png')
c2 = pygame.image.load('s2.png')
c3 = pygame.image.load('s3.png')
c4 = pygame.image.load('s4.png')
c5 = pygame.image.load('s5.png')
coins = [c0, c1, c2, c3, c4, c5]
x = 40
y = 300
bx = 0
x1 = 1250
y1 = 300
index = 0
x2 = 1550
y2 = 300
hp = 3
score = 0
state = 'start'
while True:
    # 开始界面
    if state == 'start':
        screen.blit(s, (0, 0))
    # 游戏运行
    if state == 'running':
        screen.blit(bg, (bx, 0))
        screen.blit(bg, (bx + 1000, 0))
        screen.blit(cars[index], (x, y))
        screen.blit(block, (x1, y1))
        screen.blit(coin, (x2, y2))
        screen.blit(coins[score], (670, 0))
        screen.blit(hps[hp], (0, 0))
        pygame.time.delay(30)
        index += 1
        if index == 3:
            index = 0
        bx = bx - 40
        if bx + 1000 == 0:
            bx = 0
        x1 = x1 - 40
        if x1 < -150:
            x1 = 1250
            y1 = random.choice([150, 300, 450])
        x2 = x2 - 40
        if x2 < -150:
            x2 = 1550
            y2 = random.choice([150, 300, 450])
        ############碰撞检测#############
        if y == y1 and -50 < x1 < 375:
            print('撞到障碍物了！')
            x1 = 1250
            y1 = random.choice([150, 300, 450])
            hp -= 1
            if hp == 0:
                print('lose')
                state = 'lose'
        if y == y2 and -50 < x2 < 375:
            print('撞到金币了！')
            x2 = 1550
            y2 = random.choice([150, 300, 450])
            score += 1
            if score == 5:
                print('win')
                state = 'win'
    # 游戏结束
    if state == 'win':
        screen.blit(w, (0, 0))
    if state == 'lose':
        screen.blit(l, (0, 0))
    pygame.display.update()
    # 事件获取
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
        # 键盘事件
        if e.type == pygame.KEYDOWN:
            if state == 'start':
                state = 'running'
            if e.key == pygame.K_UP:
                y = y - 150
                if y == 0:
                    y = 150
            if e.key == pygame.K_DOWN:
                y = y + 150
                if y == 600:
                    y = 450
