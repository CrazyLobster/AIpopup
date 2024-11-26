import tkinter as tk
from tkinter import messagebox 
import os
import json
import importlib


class DesktopWidget:
    def __init__(self):
        # 初始化目录
        self.config_dir = "config"
        os.makedirs(self.config_dir, exist_ok=True)

        # 当前配置
        self.current_config = {
            "name": "默认模型",
            "link": "http://default.model.api",
            "apikey": "default_key"
        }

        # 最近访问的配置
        self.recent_configs = []

        # 加载最近访问的配置
        self.recent_configs = self.load_recent_configs()

        # 创建主窗口
        self.root = tk.Tk()
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

        # 绑定事件
        self.icon_label.bind("<Button-1>", self.start_drag_or_show_plugin)
        self.icon_label.bind("<B1-Motion>", self.do_drag)
        self.icon_label.bind("<ButtonRelease-1>", self.stop_drag)
        self.icon_label.bind("<Button-3>", self.show_menu)

        # 初始化状态
        self.is_dragging = False
        self.start_x = 0
        self.start_y = 0

        # 动态加载插件
        self.plugin = self.load_plugin()

        # 创建右键菜单
        self.create_context_menu()

        # 运行主窗口
        self.root.mainloop()

    def load_recent_configs(self):
        """加载最近访问的配置列表"""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)

        config_files = sorted(
            os.listdir(self.config_dir),
            key=lambda x: os.path.getmtime(os.path.join(self.config_dir, x)),
            reverse=True
        )
        return config_files[:10]

    def save_config_to_file(self, config):
        """保存配置到文件"""
        config_path = os.path.join(self.config_dir, f"{config['name']}.json")
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=4)

        # 更新最近配置
        self.recent_configs = self.load_recent_configs()

    def load_config_from_file(self, config_name):
        """从文件加载配置"""
        config_path = os.path.join(self.config_dir, f"{config_name}.json")
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                self.current_config = json.load(f)
            self.recent_configs = self.load_recent_configs()
        else:
            tk.messagebox.showerror("错误", f"配置文件 {config_name} 不存在！")

    def create_context_menu(self):
        """右键菜单"""
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="配置", command=self.open_config_window)

        # 动态添加最近访问的配置
        if self.recent_configs:
            recent_menu = tk.Menu(self.menu, tearoff=0)
            for config_file in self.recent_configs:
                config_name = os.path.splitext(config_file)[0]
                recent_menu.add_command(
                    label=config_name,
                    command=lambda name=config_name: self.load_config_from_file(name)
                )
            self.menu.add_cascade(label="最近访问", menu=recent_menu)

        self.menu.add_separator()
        self.menu.add_command(label="退出", command=self.exit_application)

    def show_menu(self, event):
        """显示右键菜单"""
        self.menu.post(event.x_root, event.y_root)

    def start_drag_or_show_plugin(self, event):
        """记录初始位置或显示插件"""
        self.is_dragging = False
        self.start_x = event.x
        self.start_y = event.y

    def do_drag(self, event):
        """拖动挂件"""
        dx = abs(event.x - self.start_x)
        dy = abs(event.y - self.start_y)
        if dx > 5 or dy > 5:
            self.is_dragging = True
            x = self.root.winfo_x() + event.x - self.start_x
            y = self.root.winfo_y() + event.y - self.start_y
            self.root.geometry(f"+{x}+{y}")

    def stop_drag(self, event):
        """判断是否为单击，显示插件"""
        if not self.is_dragging and self.plugin:
            self.plugin.show_text_window()

    def load_plugin(self):
        """加载插件"""
        plugin_dir = "plugins"
        plugin_name = "text_popup"
        plugin_path = os.path.join(plugin_dir, f"{plugin_name}.py")

        if not os.path.exists(plugin_path):
            print(f"插件文件 {plugin_path} 不存在！")
            return None

        module = importlib.import_module(f"{plugin_dir}.{plugin_name}")
        return module.TextPopup(self.root)

    def open_config_window(self):
        """配置窗口"""
        config_window = tk.Toplevel(self.root)
        config_window.title("配置大模型")
        config_window.geometry("400x300+150+150")
        config_window.attributes('-topmost', True)

        # 输入框
        tk.Label(config_window, text="名称：", font=("Arial", 12)).pack(pady=5, anchor="w", padx=20)
        name_entry = tk.Entry(config_window, font=("Arial", 12), width=40)
        name_entry.insert(0, self.current_config["name"])
        name_entry.pack(pady=5, padx=20)

        tk.Label(config_window, text="链接：", font=("Arial", 12)).pack(pady=5, anchor="w", padx=20)
        link_entry = tk.Entry(config_window, font=("Arial", 12), width=40)
        link_entry.insert(0, self.current_config["link"])
        link_entry.pack(pady=5, padx=20)

        tk.Label(config_window, text="API Key：", font=("Arial", 12)).pack(pady=5, anchor="w", padx=20)
        apikey_entry = tk.Entry(config_window, font=("Arial", 12), width=40, show="*")
        apikey_entry.insert(0, self.current_config["apikey"])
        apikey_entry.pack(pady=5, padx=20)

        def save_config():
            # 更新配置
            self.current_config["name"] = name_entry.get()
            self.current_config["link"] = link_entry.get()
            self.current_config["apikey"] = apikey_entry.get()
            self.save_config_to_file(self.current_config)
            
            # 更新右键菜单
            self.create_context_menu()

            # 提示成功并关闭窗口
            # tk.messagebox.showinfo("成功", "配置已保存！")
            config_window.destroy()

        save_button = tk.Button(
            config_window, text="保存", command=save_config, bg="green", fg="white", font=("Arial", 12)
        )
        save_button.pack(pady=20)

    def exit_application(self):
        """退出程序"""
        self.root.destroy()


if __name__ == "__main__":
    DesktopWidget()
