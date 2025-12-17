"""
网络监控GUI主窗口
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
from datetime import datetime
from pathlib import Path

from src.core.monitor import NetworkMonitor
from src.utils.config import ConfigManager


class NetworkMonitorGUI:
    """网络监控GUI主窗口"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("网络监控工具")
        self.root.geometry("450x380")
        self.root.resizable(False, False)
        
        self.monitor = None
        self.monitoring = False
        self.update_thread = None
        
        # 配置管理器
        self.config = ConfigManager()
        
        # 加载服务器列表
        self.server_list = self.config.get_server_history(
            default_servers=[
                "www.baidu.com",
                "api.link.aliyun.com",
                "mlvbdc.live.tlivesource.com"
            ]
        )
        
        self.create_widgets()
    
    def create_widgets(self):
        """创建界面组件"""
        # 主容器
        main = tk.Frame(self.root, padx=20, pady=20)
        main.pack(fill=tk.BOTH, expand=True)
        
        # 目标服务器（可输入的下拉框）
        tk.Label(main, text="目标服务器:").grid(row=0, column=0, sticky=tk.W, pady=(0, 8))
        self.server_combo = ttk.Combobox(main, values=self.server_list, width=30)
        self.server_combo.current(0)
        self.server_combo.grid(row=0, column=1, sticky=tk.W, pady=(0, 8))
        
        # 采样间隔
        tk.Label(main, text="采样间隔:").grid(row=1, column=0, sticky=tk.W, pady=(0, 20))
        interval_frame = tk.Frame(main)
        interval_frame.grid(row=1, column=1, sticky=tk.W, pady=(0, 20))
        self.interval_var = tk.DoubleVar(value=1.0)
        tk.Spinbox(interval_frame, from_=0.5, to=5.0, increment=0.5, 
                   textvariable=self.interval_var, width=8).pack(side=tk.LEFT)
        tk.Label(interval_frame, text="秒").pack(side=tk.LEFT, padx=(5, 0))
        
        # 按钮
        btn_frame = tk.Frame(main)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=(0, 20))
        
        self.start_btn = tk.Button(btn_frame, text="开始监控", width=15, command=self.start_monitoring)
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = tk.Button(btn_frame, text="停止监控", width=15, state=tk.DISABLED, command=self.stop_monitoring)
        self.stop_btn.pack(side=tk.LEFT)
        
        # 状态
        status_frame = tk.LabelFrame(main, text="状态", padx=10, pady=10)
        status_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        info_frame = tk.Frame(status_frame)
        info_frame.pack(fill=tk.X)
        self.status_label = tk.Label(info_frame, text="未开始")
        self.status_label.pack(side=tk.LEFT)
        self.time_label = tk.Label(info_frame, text="0秒")
        self.time_label.pack(side=tk.RIGHT)
        
        # 统计
        stats_frame = tk.LabelFrame(main, text="统计", padx=10, pady=10)
        stats_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        
        # 第一行
        row1 = tk.Frame(stats_frame)
        row1.pack(fill=tk.X, pady=(0, 5))
        tk.Label(row1, text="请求:").pack(side=tk.LEFT)
        self.total_label = tk.Label(row1, text="0")
        self.total_label.pack(side=tk.LEFT, padx=(5, 15))
        tk.Label(row1, text="成功:").pack(side=tk.LEFT)
        self.success_label = tk.Label(row1, text="0")
        self.success_label.pack(side=tk.LEFT, padx=(5, 15))
        tk.Label(row1, text="超时:").pack(side=tk.LEFT)
        self.timeout_label = tk.Label(row1, text="0")
        self.timeout_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # 第二行
        row2 = tk.Frame(stats_frame)
        row2.pack(fill=tk.X)
        tk.Label(row2, text="平均:").pack(side=tk.LEFT)
        self.avg_label = tk.Label(row2, text="0ms")
        self.avg_label.pack(side=tk.LEFT, padx=(5, 15))
        tk.Label(row2, text="最小:").pack(side=tk.LEFT)
        self.min_label = tk.Label(row2, text="0ms")
        self.min_label.pack(side=tk.LEFT, padx=(5, 15))
        tk.Label(row2, text="最大:").pack(side=tk.LEFT)
        self.max_label = tk.Label(row2, text="0ms")
        self.max_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # 保存按钮
        self.save_btn = tk.Button(main, text="保存日志", state=tk.DISABLED, command=self.save_log)
        self.save_btn.grid(row=5, column=0, columnspan=2, sticky="ew")
        
    def start_monitoring(self):
        """开始监控"""
        # 获取服务器地址
        server = self.server_combo.get().strip()
        if not server:
            messagebox.showerror("错误", "请输入服务器地址")
            return
        
        # 保存到历史
        self.server_list = self.config.add_server_history(server)
        self.server_combo['values'] = self.server_list
        
        # 创建监控器
        self.monitor = NetworkMonitor(
            name="电脑端",
            targets=[server],
            interval=self.interval_var.get(),
            timeout=2.0,
            high_latency_threshold=100,
            verbose=False
        )
        
        self.monitor.start()
        self.monitoring = True
        self.start_time = time.time()
        
        # 更新UI
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.server_combo.config(state=tk.DISABLED)
        self.status_label.config(text="监控中")
        
        # 启动更新线程
        self.update_thread = threading.Thread(target=self.update_loop, daemon=True)
        self.update_thread.start()
        
    def stop_monitoring(self):
        """停止监控"""
        if self.monitor:
            self.monitor.stop()
            self.monitoring = False
            
            # 更新UI
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.server_combo.config(state=tk.NORMAL)
            self.save_btn.config(state=tk.NORMAL)
            self.status_label.config(text="已停止")
            
            self.update_statistics()
            messagebox.showinfo("完成", "监控已停止")
    
    def update_loop(self):
        """更新循环"""
        while self.monitoring:
            self.root.after(0, self.update_time)
            self.root.after(0, self.update_statistics)
            time.sleep(1)
    
    def update_time(self):
        """更新时间"""
        if self.monitoring:
            elapsed = int(time.time() - self.start_time)
            m, s = divmod(elapsed, 60)
            self.time_label.config(text=f"{m}分{s}秒" if m > 0 else f"{s}秒")
    
    def update_statistics(self):
        """更新统计"""
        if self.monitor:
            stats = self.monitor.get_statistics()
            self.total_label.config(text=str(stats['total_count']))
            self.success_label.config(text=str(stats['success_count']))
            self.timeout_label.config(text=str(stats['timeout_count']))
            self.avg_label.config(text=f"{stats['avg_ping_ms']:.0f}ms")
            self.min_label.config(text=f"{stats['min_ping_ms']:.0f}ms")
            self.max_label.config(text=f"{stats['max_ping_ms']:.0f}ms")
    
    def save_log(self):
        """保存日志"""
        if not self.monitor or not self.monitor.data:
            messagebox.showwarning("提示", "没有数据")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = filedialog.asksaveasfilename(
            initialfile=f"network_log_pc_{timestamp}.csv",
            defaultextension=".csv",
            filetypes=[("CSV文件", "*.csv")]
        )
        
        if filepath:
            self.monitor.save_log(filepath)
            messagebox.showinfo("成功", "日志已保存")
    
    def on_closing(self):
        """窗口关闭事件"""
        if self.monitoring:
            if messagebox.askokcancel("确认", "监控正在运行，确定退出？"):
                if self.monitor:
                    self.monitor.stop()
                self.root.destroy()
        else:
            self.root.destroy()

