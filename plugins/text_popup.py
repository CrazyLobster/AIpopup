# plugins/text_popup.py

import tkinter as tk


class TextPopup:
    def __init__(self, root):
        self.root = root
        self.text_window = None

    def show_text_window(self):
        """弹出文本框窗口"""
        if self.text_window:
            # 如果文本框已存在，则不重复弹出
            return

        # 创建半透明文本框窗口
        self.text_window = tk.Toplevel(self.root)
        self.text_window.title("文本框")
        self.text_window.geometry("400x200+150+150")  # 文本框大小和位置
        self.text_window.overrideredirect(True)  # 去掉标题栏
        self.text_window.attributes('-topmost', True)  # 置顶
        self.text_window.attributes('-alpha', 0.6)  # 设置透明度 (0.0 - 1.0)
        self.text_window.config(bg="#F0F0F0")  # 灰白色背景颜色

        # 文本框内容
        text_label = tk.Label(
            self.text_window, text="点击图标显示的文本框", bg="#F0F0F0", fg="black",
            font=("Arial", 14), wraplength=380, justify="center"
        )
        text_label.pack(expand=True, fill="both", padx=10, pady=10)

        # 添加关闭按钮
        close_button = tk.Button(
            self.text_window, text="关闭", command=self.close_text_window,
            bg="red", fg="white", font=("Arial", 12)
        )
        close_button.pack(pady=20)

        # 为文本框绑定拖动事件
        self.text_window.bind("<Button-1>", self.start_text_drag)
        self.text_window.bind("<B1-Motion>", self.do_text_drag)

    def start_text_drag(self, event):
        """记录文本框鼠标按下时的初始位置"""
        self.text_window.start_x = event.x
        self.text_window.start_y = event.y

    def do_text_drag(self, event):
        """根据鼠标移动更新文本框位置"""
        x = self.text_window.winfo_x() + event.x - self.text_window.start_x
        y = self.text_window.winfo_y() + event.y - self.text_window.start_y
        self.text_window.geometry(f"+{x}+{y}")

    def close_text_window(self):
        """关闭文本框窗口"""
        if self.text_window:
            self.text_window.destroy()
            self.text_window = None
