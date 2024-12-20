import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
import importlib
import os


class DesktopWidget:
    def __init__(self):
        # 使用 TkinterDnD 创建主窗口
        self.root = TkinterDnD.Tk()
        self.root.title("桌面挂件")
        self.root.geometry("100x100+100+100")
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.9)
        self.root.config(bg="gray")

        # 挂件图标
        self.icon_label = tk.Label(
            self.root, text="📌", font=("Arial", 32), bg="gray", fg="white"
        )
        self.icon_label.pack(expand=True, fill="both")

        # 绑定拖放事件
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.handle_drop_event)

        # 动态加载插件
        self.plugin = self.load_plugin()

        # 运行主窗口
        self.root.mainloop()

    def handle_drop_event(self, event):
        """处理拖放事件"""
        if self.plugin:
            self.plugin.handle_drop(event.data)

    def load_plugin(self):
        """加载插件"""
        plugin_dir = "plugins"
        plugin_name = "image_popup"
        plugin_path = os.path.join(plugin_dir, f"{plugin_name}.py")

        if not os.path.exists(plugin_path):
            print(f"插件文件 {plugin_path} 不存在！")
            return None

        module = importlib.import_module(f"{plugin_dir}.{plugin_name}")
        return module.ImageHandlerPlugin(self.root)


if __name__ == "__main__":
    DesktopWidget()
