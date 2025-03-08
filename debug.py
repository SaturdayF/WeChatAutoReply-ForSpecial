import time
import pygame

pygame.mixer.init()
# 加载音乐文件
pygame.mixer.music.load('music.mp3')
# 播放音乐
pygame.mixer.music.play()
# 等待播放完成（避免程序提前退出）
while pygame.mixer.music.get_busy():
    time.sleep(0.1)