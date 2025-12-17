"""
网络监控工具 - exe打包脚本
使用PyInstaller打包
"""
import os
import subprocess
import sys

def main():
    """执行打包"""
    print("="*60)
    print("电脑端网络监控工具 - exe打包")
    print("="*60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print("[OK] PyInstaller 已安装")
    except ImportError:
        print("[!] PyInstaller 未安装")
        print()
        print("正在安装 PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("[OK] PyInstaller 安装完成")
    
    print()
    print("-"*60)
    print("开始打包...")
    print("-"*60)
    print()
    
    # PyInstaller命令
    cmd = [
        "pyinstaller",
        "--onefile",                    # 打包成单个exe
        "--windowed",                   # 无控制台窗口（GUI程序）
        "--name=网络监控工具",          # exe名称
        "--icon=NONE",                  # 图标（可自定义）
        "--add-data=config.json;.",     # 包含配置文件（如果存在）
        "--clean",                      # 清理缓存
        "gui.py"                        # 入口文件
    ]
    
    # Windows下路径分隔符是分号
    if sys.platform == "win32":
        cmd[5] = "--add-data=config.json;."
    else:
        cmd[5] = "--add-data=config.json:."
    
    # 如果config.json不存在，移除该参数
    if not os.path.exists("config.json"):
        cmd.pop(5)
    
    print("执行命令:")
    print(" ".join(cmd))
    print()
    
    try:
        subprocess.check_call(cmd)
        print()
        print("="*60)
        print("[OK] 打包完成！")
        print("="*60)
        print()
        print("exe文件位置: dist/网络监控工具.exe")
        print()
    except Exception as e:
        print()
        print("="*60)
        print("[ERROR] 打包失败")
        print("="*60)
        print(f"错误: {e}")
        print()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

