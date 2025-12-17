"""
网络监控工具 - 命令行版本入口
"""
import time
from datetime import datetime
from src.core.monitor import NetworkMonitor


def main():
    """主函数"""
    print("="*60)
    print("电脑端网络监控工具")
    print("="*60)
    print()
    
    # 配置
    print("请输入监控配置：")
    print()
    
    # 云平台选择
    print("云平台选择：")
    print("  1. 百度（测试）  - www.baidu.com")
    print("  2. 阿里云       - api.link.aliyun.com")
    print("  3. 腾讯云       - mlvbdc.live.tlivesource.com")
    print("  4. 自定义地址")
    print()
    
    platform_choice = input("选择平台 (1-4，默认: 1): ").strip()
    
    if platform_choice == "2":
        target = "api.link.aliyun.com"
    elif platform_choice == "3":
        target = "mlvbdc.live.tlivesource.com"
    elif platform_choice == "4":
        target = input("请输入服务器地址: ").strip()
        if not target:
            target = "www.baidu.com"
    else:
        target = "www.baidu.com"
    
    print()
    
    # 监控时长
    default_duration = 60
    duration_input = input(f"监控时长/秒 (默认: {default_duration}): ").strip()
    try:
        duration = int(duration_input) if duration_input else default_duration
    except:
        duration = default_duration
    
    # 采样间隔
    default_interval = 1.0
    interval_input = input(f"采样间隔/秒 (默认: {default_interval}): ").strip()
    try:
        interval = float(interval_input) if interval_input else default_interval
    except:
        interval = default_interval
    
    print()
    print("-"*60)
    print(f"配置确认：")
    print(f"  目标: {target}")
    print(f"  时长: {duration}秒")
    print(f"  间隔: {interval}秒")
    print("-"*60)
    print()
    
    input("按回车开始监控...")
    print()
    
    # 创建监控器
    monitor = NetworkMonitor(
        name="电脑端",
        targets=[target],
        interval=interval,
        timeout=2.0,
        high_latency_threshold=100,
        verbose=True
    )
    
    # 启动监控
    monitor.start()
    
    print()
    print(f"⏱️  监控进行中... (共{duration}秒)")
    print(f"💡 现在可以开始录制视频并进行测试")
    print(f"💡 按 Ctrl+C 可提前停止")
    print()
    
    # 倒计时
    try:
        for i in range(duration):
            remaining = duration - i
            print(f"  ⏳ 剩余 {remaining} 秒...", end='\r')
            time.sleep(1)
        print()
    except KeyboardInterrupt:
        print("\n\n用户中断")
    
    # 停止监控
    print()
    monitor.stop()
    
    # 统计
    stats = monitor.get_statistics()
    print()
    print("="*60)
    print("监控统计")
    print("="*60)
    print(f"总请求数:   {stats['total_count']}")
    print(f"成功数:     {stats['success_count']}")
    print(f"超时数:     {stats['timeout_count']}")
    print(f"丢包率:     {stats['packet_loss_rate']:.1%}")
    print(f"平均延迟:   {stats['avg_ping_ms']:.1f}ms")
    print(f"最小延迟:   {stats['min_ping_ms']:.1f}ms")
    print(f"最大延迟:   {stats['max_ping_ms']:.1f}ms")
    print(f"高延迟次数: {stats['high_latency_count']}")
    print("="*60)
    print()
    
    # 保存日志
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"network_log_pc_{timestamp}.csv"
    monitor.save_log(log_file)
    
    print()
    print(f"✓ 完成！日志文件: {log_file}")
    print()
    input("按回车退出...")


if __name__ == '__main__':
    main()

