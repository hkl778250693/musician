# -*- coding: utf-8 -*-
# @Project: amateurPythonProject
# @Author: hkl
# @File name: night_sky_stars
# @Create time: 2021/2/22 15:51

import pygame, sys, random, time
from pygame.locals import *

# 窗口大小以及标题初始化
screen = pygame.display.set_mode((300, 500), 0, 0)
pygame.display.set_caption("夜空中最亮的星")
# 定义用于存放星星的列表
star_x = []
star_y = []
# 随机生成100个星星
for i in range(0, 30):
    star_x.append(random.randint(0, 300))
    star_y.append(random.randint(0, 500))

while True:
    # 遍历事件
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    # 填充黑色
    screen.fill((0, 0, 0))
    # 设置星星的移动轨迹
    for i in range(len(star_x)):
        star_x[i] += 1
        star_y[i] += 1
        # 星星从屏幕中消失
        if star_x[i] > 300:
            star_x[i] = 0
        if star_y[i] > 500:
            star_y[i] = 0
    # 添加背景图片
    background_path = "./1.jpg"
    background = pygame.image.load(background_path).convert()
    screen.blit(background, (0, 0))
    # 初始化显示的字体
    pygame.font.init()
    font = pygame.font.SysFont("wryh.ttf", 30)

    # 生成随机颜色的星星
    for i in range(len(star_x)):
        R = random.randint(0, 255)
        G = random.randint(0, 255)
        B = random.randint(0, 255)
        star = font.render("python", True, (R, G, B))
        screen.blit(star, (star_x[i], star_y[i]))
    pygame.time.delay(200)  # 20秒刷新一次
    pygame.display.update()
