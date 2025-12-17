# 电脑端网络监控工具

网络监控工具，用于测试时记录电脑的网络状况。

## 快速使用

### 运行程序

```bash
python gui.py
```

或者直接运行打包好的 `网络监控工具.exe`

### 使用步骤

1. 输入目标服务器地址（与手机APP填写相同）
2. 设置采样间隔（默认1秒）
3. 点击「开始监控」
4. 进行测试（录制视频等）
5. 点击「停止监控」
6. 点击「保存日志」导出CSV文件

---

## 打包exe

```bash
pip install pyinstaller
pyinstaller --onefile --windowed gui.py
```

生成的exe在 `dist` 文件夹中。

---

## 输出格式

CSV文件格式：

```csv
timestamp,datetime,target,ping_ms,packet_loss,status
1702652400.123,2023-12-15 16:00:00.123,api.link.aliyun.com,45.20,0.00,ok
```

**字段说明：**
- `timestamp`: Unix时间戳
- `datetime`: 可读时间
- `target`: 目标服务器
- `ping_ms`: 延迟（毫秒）
- `packet_loss`: 丢包率（0-1）
- `status`: 状态（ok/timeout/error）

---

## 注意事项

1. 电脑和手机必须ping同一个服务器地址
2. 确保电脑和手机时间准确
3. 监控要和视频录制同时进行
4. 确保防火墙允许ping（ICMP协议）

---

## 系统要求

- Windows 7+
- Python 3.6+（exe版本无需Python）
