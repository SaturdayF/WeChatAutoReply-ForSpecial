# core/calling.py
import pygame
import time

from playsound import playsound
from datetime import datetime

class CallingMessageStrategy:
    def __init__(self):
        self.calling_content = []
        self._load_instructions()

    def _load_instructions(self):
        with open('core/instruction/calling.txt', 'r', encoding='utf-8') as f:
            for line in f:
                key, value = line.strip().split(':', 1)
                self.calling_content.append(value)

    def _save_instructions(self):
        """保存当前指令"""
        with open('core/instruction/calling.txt', 'w', encoding='utf-8') as f:
            for content in self.calling_content:
                f.write(f'calling:{content}\n')

    def append(self, message):
        self.calling_content.append(message)
        self._save_instructions()

    def delete(self,message):
        if message in self.calling_content:
            self.calling_content.remove(message)
            self._save_instructions()
            return '删除成功!'
        else:
            return '该指令不存在于指令集中'

    def printlist(self):
        return self.calling_content

    def handle(self,chat):
        chat.SendMsg('正在加急呼叫中！！！')  # 回复收到
        self.play_alert()

    def play_alert(self):
        """播放提示音"""
        pygame.mixer.init()
        pygame.mixer.music.load("music.mp3")
        pygame.mixer.music.play()
        time.sleep(10)
        pygame.mixer.music.stop()





