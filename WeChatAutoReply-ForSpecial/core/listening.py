# core/listening.py
# from Strategy import Strategy


class ListeningMessageStrategy:
    def __init__(self):
        self.listen_list = []
        self._load_instructions()

    def _load_instructions(self):
        with open('core/instruction/listen.txt', 'r', encoding='utf-8') as f:
            for line in f:
                key, value = line.strip().split(':', 1)
                self.listen_list.append(value)

    def _save_instructions(self):
        """保存当前指令"""
        with open('core/instruction/listen.txt', 'w', encoding='utf-8') as f:
            for content in self.listen_list:
                f.write(f'listen:{content}\n')

    def append(self, message):
        self.listen_list.append(message)
        self._save_instructions()

    def delete(self,message):
        if message in self.listen_list:
            self.listen_list.remove(message)
            return '删除成功!'
        else:
            return '该指令不存在于指令集中'

    def printlist(self):
        return self.listen_list


