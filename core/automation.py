# core/automation.py
import time
from wxauto import WeChat
from core.MessageStrategyFactory import MessageStrategyFactory


from PyQt5.QtCore import QThread, pyqtSignal, QMutex, QMutexLocker


class WorkerThread(QThread):
    # 定义信号用于与主线程通信
    status_updated = pyqtSignal(str)  # 发送状态更新
    error_occurred = pyqtSignal(str)  # 发送错误信息
    finished = pyqtSignal()          # 任务完成信号

    def __init__(self, automation):
        super().__init__()
        self.automation = automation
        self._is_running = False  # 使用线程安全的标志
        self._mutex = QMutex()

    def run(self):
        """线程核心执行逻辑"""
        with QMutexLocker(self._mutex):
            self._is_running = True
        try:
            while self.is_running:
                result = self.automation.perform_task()
                self.status_updated.emit(result)
        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            self.finished.emit()

    def stop(self):
        with QMutexLocker(self._mutex):
            self._is_running = False
        self.wait(1000)  # 等待线程退出

    @property
    def is_running(self):
        with QMutexLocker(self._mutex):
            return self._is_running


class WeChatAutomation:
    def __init__(self):
        self.thread = None
        self.my_wx = Mywxauto()  # 核心逻辑实例

    @property
    def is_running(self):
        return self.thread and self.thread.isRunning()

    def start(self):
        """启动线程"""
        if not self.is_running:
            self.thread = WorkerThread(self)
            self.thread.start()  # 启动线程

    def stop(self):
        if self.is_running:
            self.thread.stop()

    def perform_task(self):
        return self.my_wx.run()  # 执行实际任务


class Mywxauto:
    def __init__(self):
        self.wx = None
        self.chat = None
        self._mutex = QMutex()
        self._is_running = False  # 私有变量
        # self.is_running = False
        self.strategy = MessageStrategyFactory()

    @property
    def is_running(self):
        with QMutexLocker(self._mutex):
            return self._is_running

    @is_running.setter
    def is_running(self, value):
        with QMutexLocker(self._mutex):
            self._is_running = value

    def get_list(self,value):
        return self.strategy.get_strategy(value).printlist()

    def get_status(self):
        """获取当前状态"""
        return {
            'listen_list': self.get_list('listening'),
            'calling': self.get_list('calling'),
            'watching': self.get_list('watching')
        }

    def handle_message(self, msgtype, content, sender):
        """处理消息核心逻辑"""
        wx = self.wx
        chat = self.chat

        print(f'【{sender}】：{content}')
        # 处理消息逻辑
        if msgtype == 'friend':
            if content == '@help':
                chat.SendMsg(
                    '1.@添加呼叫指令：\n2.@添加截屏指令：\n3.@查看指令集\n4.@删除呼叫指令：\n5.@删除截屏指令：')
            elif content[:6] == '@查看指令集':
                str1 = '————呼叫指令————\n'
                for c in self.get_list('calling'):
                    str1 = str1 + c + '\n'
                str1 = str1 + '\n' + '————截屏指令————\n'
                for c in self.get_list('watching'):
                    str1 = str1 + c + '\n'
                chat.SendMsg(str1)

            elif content[:8] == '@添加呼叫指令：':
                self.strategy.get_strategy('calling').append(content[8:])
                chat.SendMsg('添加成功！')
            elif content[:8] == '@添加截屏指令：':
                self.strategy.get_strategy('watching').append(content[8:])
                chat.SendMsg('添加成功！')
            elif content[:8] == '@删除呼叫指令：':
                return_msg = self.strategy.get_strategy('calling').delete(content[8:])
                chat.SendMsg(return_msg)
            elif content[:8] == '@删除截屏指令：':
                return_msg = self.strategy.get_strategy('watching').delete(content[8:])
                chat.SendMsg(return_msg)
            elif content in self.get_list('calling'):
                self.strategy.get_strategy('calling').handle(chat)
            elif content in self.get_list('watching'):
                self.strategy.get_strategy('watching').handle(wx,chat)

        # 此处应返回处理结果
        return f"已处理来自{sender}的消息：{content}"

    def run(self):
        # 初始化
        self.is_running = True
        self.wx = WeChat()

        # 开始加载监听窗口
        print('监听窗口加载中……')
        for i in self.get_list('listening'):
            self.wx.AddListenChat(who=i, savepic=False)
            self.chat = self.wx.get_chat(i)
            self.chat.SendMsg("程序已开始运行！")
        print('监听窗口加载完毕！')

        # 此处应改为可控制的中断式循环
        while self.is_running:
            # 消息处理逻辑
            try:
                msgs = self.wx.GetListenMessage()
                # ...处理消息...
                for self.chat in msgs:
                    who = self.chat.who  # 获取聊天窗口名（人或群名）
                    one_msgs = msgs.get(self.chat)  # 获取消息内容
                    for msg in one_msgs:
                        msgtype = msg.type  # 获取消息类型
                        content = msg.content  # 获取消息内容，字符串类型的消息内容
                        self.handle_message(msgtype, content, who)
            except Exception as e:
                print(f"Error: {str(e)}")
            time.sleep(1)

    def stop(self):
        self.is_running = False
        if self.wx:
            # 假设 wxauto 有释放资源的方法
            self.wx.close()  # 或 self.wx.cleanup()
            self.wx = None

# if __name__ == "__main__":
#     wxx = WeChatAutomation()
#     wxx.run()
