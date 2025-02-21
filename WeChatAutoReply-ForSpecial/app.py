# app.py
import sys
from PyQt5.QtWidgets import QApplication
from core.automation import WeChatAutomation
from ui.main_window import MainWindow


class Application:
    def __init__(self):
        self.automation = WeChatAutomation()
        self.ui = MainWindow()
        self.ui.operation_requested.connect(self.handle_operation)

    def show_error(self, message):
        """显示错误信息"""
        self.ui.update_status(f"错误: {message}", color="#FF0000")

    def on_automation_finished(self):
        """任务结束处理"""
        self.ui.update_status("自动化任务已停止")

    def handle_operation(self, operation, params=None):
        """处理UI操作请求"""
        if operation  == "start":
            self.start_automation()
        elif operation == "stop":
            self.stop_automation()
        elif operation == "get_status":
            self.send_status()

    def start_automation(self):
        """启动自动化任务"""
        if not self.automation.is_running:
            self.automation.start()  # 启动线程
            # 创建线程后连接信号
            self.automation.thread.status_updated.connect(self.ui.update_status)
            self.automation.thread.error_occurred.connect(self.show_error)
            self.automation.thread.finished.connect(self.on_automation_finished)

    def stop_automation(self):
        """停止自动化任务"""
        if self.automation.is_running:
            self.automation.stop()
            print("自动化任务已停止")

    def send_status(self):
        """发送当前状态到UI"""
        status = self.automation.get_status()
        self.ui.update_status(status)

    def run(self):
        """运行应用"""
        self.ui.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    application = Application()
    application.run()
    sys.exit(app.exec_())