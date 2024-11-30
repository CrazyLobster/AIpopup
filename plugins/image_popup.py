import tkinter as tk
from tkinterdnd2 import TkinterDnD
from PIL import Image, ImageTk
import os
import tkinter.messagebox

class ImageHandlerPlugin:
    def __init__(self, root):
        self.root = root
        self.image_window = None
        self.current_image = None

    def handle_drop(self, dropped_file):
        """处理拖放的图片文件"""
        file_path = dropped_file.strip('{}')  # 去除路径两端的 {}
        if os.path.isfile(file_path) and file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            self.open_image_window(file_path)
        else:
            tk.messagebox.showerror("错误", "仅支持图片文件！")

    def open_image_window(self, file_path):
        """打开窗口显示图片和输入框"""
        if self.image_window:
            self.image_window.destroy()

        # 创建图片窗口
        self.image_window = tk.Toplevel(self.root)
        self.image_window.title("图片处理")
        self.image_window.geometry("500x600")
        self.image_window.attributes('-topmost', True)

        # 加载图片
        try:
            img = Image.open(file_path)
            img.thumbnail((500, 400))
            self.current_image = ImageTk.PhotoImage(img)

            # 显示图片
            img_label = tk.Label(self.image_window, image=self.current_image)
            img_label.pack(pady=10)

        except Exception as e:
            tk.messagebox.showerror("错误", f"无法加载图片：{e}")
            return

        # 添加输入框和提交按钮
        tk.Label(self.image_window, text="请输入您的问题：", font=("Arial", 12)).pack(pady=5)
        input_entry = tk.Entry(self.image_window, font=("Arial", 12), width=40)
        input_entry.pack(pady=10)

        def submit_question():
            question = input_entry.get().strip()
            if not question:
                tk.messagebox.showerror("错误", "问题不能为空！")
                return

            # 模拟发送图片和问题
            response = f"发送成功：图片({file_path})，问题({question})"
            tk.messagebox.showinfo("结果", response)

        submit_button = tk.Button(
            self.image_window, text="提交", command=submit_question, bg="green", fg="white", font=("Arial", 12)
        )
        submit_button.pack(pady=20)
