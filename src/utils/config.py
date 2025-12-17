"""
配置管理工具
"""
import json
from pathlib import Path
from typing import List


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file: str = "config.json"):
        """
        初始化配置管理器
        
        Args:
            config_file: 配置文件路径
        """
        self.config_file = Path(config_file)
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """加载配置文件"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载配置文件失败: {e}")
                return {}
        return {}
    
    def _save_config(self):
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存配置文件失败: {e}")
    
    def get_server_history(self, default_servers: List[str] = None) -> List[str]:
        """
        获取服务器历史记录
        
        Args:
            default_servers: 默认服务器列表
            
        Returns:
            服务器列表（包含历史和默认）
        """
        default_servers = default_servers or ["www.baidu.com"]
        history = self.config.get('server_history', [])
        
        # 合并默认和历史，去重
        all_servers = default_servers + [s for s in history if s not in default_servers]
        return all_servers[:10]  # 最多保留10个
    
    def add_server_history(self, server: str) -> List[str]:
        """
        添加服务器到历史记录
        
        Args:
            server: 服务器地址
            
        Returns:
            更新后的服务器列表
        """
        history = self.config.get('server_history', [])
        
        # 添加到列表顶部
        if server in history:
            history.remove(server)
        history.insert(0, server)
        
        # 只保留前10个
        history = history[:10]
        
        # 保存
        self.config['server_history'] = history
        self._save_config()
        
        return history
    
    def get(self, key: str, default=None):
        """获取配置项"""
        return self.config.get(key, default)
    
    def set(self, key: str, value):
        """设置配置项"""
        self.config[key] = value
        self._save_config()

