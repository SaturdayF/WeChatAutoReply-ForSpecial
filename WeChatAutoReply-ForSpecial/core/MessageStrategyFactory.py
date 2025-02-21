from core.listening import ListeningMessageStrategy
from core.calling import CallingMessageStrategy
from core.watching import WatchingMessageStrategy

class MessageStrategyFactory:
    def __init__(self):
        self.listening = ListeningMessageStrategy()
        self.calling = CallingMessageStrategy()
        self.watching = WatchingMessageStrategy()

    def get_strategy(self,strategy_type):
        if strategy_type == "calling":
            return self.calling
        elif strategy_type == "watching":
            return self.watching
        elif strategy_type == "listening":
            return self.listening
        else:
            raise ValueError("未知的策略类型")


