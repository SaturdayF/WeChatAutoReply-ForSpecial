# core/watching.py
from datetime import datetime

import os
from PIL import ImageGrab


class WatchingMessageStrategy:
    def __init__(self):
        self.watching_content = []
        self._load_instructions()

    def _load_instructions(self):
        with open('core/instruction/watching.txt', 'r', encoding='utf-8') as f:
            for line in f:
                key, value = line.strip().split(':', 1)
                self.watching_content.append(value)

    def _save_instructions(self):
        """保存当前指令"""
        with open('core/instruction/watching.txt', 'w', encoding='utf-8') as f:
            for content in self.watching_content:
                f.write(f'watch:{content}\n')

    def append(self, message):
        self.watching_content.append(message)
        self._save_instructions()

    def delete(self,message):
        if message in self.watching_content:
            self.watching_content.remove(message)
            self._save_instructions()
            return '删除成功!'
        else:
            return '该指令不存在于指令集中'

    def printlist(self):
        return self.watching_content

    def handle(self,wx,chat):
        # 截取屏幕
        screenshot = ImageGrab.grab()
        # 保存图片
        save_path = os.path.join('screenshot', self.gettime() + '.png')
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        screenshot.save(save_path)
        print(f"截图已保存到: {save_path}")
        # 获取绝对路径
        absolute_path = os.path.abspath(save_path)
        chat.SendMsg('图片已保存，马上送达！！！')  # 回复收到
        wx.SendFiles(filepath=absolute_path, who=chat.who)
        os.remove(absolute_path)
        print(f"文件 {absolute_path} 已删除。")

    def gettime(self):
        ''' 获取当前的时间 '''
        current_datetime = datetime.now()
        formatted_time = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")  # 将冒号替换为下划线
        return formatted_time