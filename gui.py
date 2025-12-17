"""
网络监控工具 - GUI版本入口
"""
import tkinter as tk
from src.gui.main_window import NetworkMonitorGUI


def main():
    """主函数"""
    root = tk.Tk()
    app = NetworkMonitorGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == '__main__':
    main()

