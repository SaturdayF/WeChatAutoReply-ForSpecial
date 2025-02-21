# ui/main_window.py
import sys

from PyQt5 import Qt
from PyQt5.QtCore import pyqtSignal, QObject, QMetaObject, Q_ARG
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QTextCursor, QColor


class ConsoleStream(QObject):
    new_log = pyqtSignal(str, QColor)

    def write(self, text):
        self.new_log.emit(text.rstrip(), QColor("#FFFFFF"))

    def flush(self):
        pass


class MainWindow(QMainWindow):
    operation_requested = pyqtSignal(str, dict)  # 操作类型, 参数

    def __init__(self):
        super().__init__()
        self._init_ui()
        self._setup_console()

    def _init_ui(self):
        # 窗口基础设置
        self.setWindowTitle("GoodMorning!")
        self.resize(1000, 800)

        # 主布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # 日志显示区
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                color: #FFFFFF;
                font-family: Consolas;
                font-size: 12pt;
            }
        """)
        layout.addWidget(self.console)

        # 控制面板
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)

        self.btn_start = QPushButton("启动")
        self.btn_stop = QPushButton("停止")
        self.btn_status = QPushButton("获取状态")

        # 正确绑定所有按钮的点击事件
        self.btn_start.clicked.connect(lambda: self.on_button_click("start"))
        self.btn_stop.clicked.connect(lambda: self.on_button_click("stop"))
        self.btn_status.clicked.connect(lambda: self.on_button_click("get_status"))

        control_layout.addWidget(self.btn_start)
        control_layout.addWidget(self.btn_stop)
        control_layout.addWidget(self.btn_status)

        layout.addWidget(control_panel)

    def on_button_click(self, operation):
        self.operation_requested.emit(operation, {"key": "value"})  # 触发信号

    def update_status(self, text, color="#FFFFFF"):
        """线程安全的UI更新"""
        # 使用 QueuedConnection 确保在主线程执行
        QMetaObject.invokeMethod(
            self.console,
            "append",
            Qt.QueuedConnection,
            Q_ARG(str, f"[状态] {text}"),
            Q_ARG("QColor", QColor(color))
        )

    def _setup_console(self):
        # 重定向标准输出
        self.stdout = ConsoleStream()
        self.stdout.new_log.connect(self._append_log)
        sys.stdout = self.stdout

        # 重定向标准错误
        self.stderr = ConsoleStream()
        self.stderr.new_log.connect(lambda t: self._append_log(t, QColor("#FF0000")))
        sys.stderr = self.stderr

    def _append_log(self, text, color):
        cursor = self.console.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(f"{text}\n")
        self.console.setTextCursor(cursor)