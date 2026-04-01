#!/bin/bash
sudo nohup java -jar /home/openailab/Downloads/kiftd-1.2.2-release/kiftd-1.2.2-RELEASE.jar -start & echo $!
echo "正在安装Python应用开机自启动服务..."

# 检查Python脚本是否存在
if [ ! -f "/home/openailab/Documents/app.py" ]; then
    echo "错误: 找不到 /home/openailab/Documents/app.py"
    exit 1
fi

# 检查python3.8是否存在
if ! command -v python3.8 &> /dev/null; then
    echo "错误: 找不到 python3.8"
    exit 1
fi

# 复制服务文件到systemd目录
#sudo cp myapp.service /etc/systemd/system/

# 设置文件权限
sudo chmod 644 /etc/systemd/system/myapp.service

# 重新加载systemd配置
sudo systemctl daemon-reload

# 启用服务开机自启动
sudo systemctl enable myapp.service

# 启动服务
sudo systemctl start myapp.service

# 等待服务启动
sleep 2

echo ""
echo "服务安装完成！"
echo "================================================"
echo "服务状态: sudo systemctl status myapp.service"
echo "查看实时日志: sudo journalctl -u myapp.service -f"
echo "停止服务: sudo systemctl stop myapp.service"
echo "重启服务: sudo systemctl restart myapp.service"
echo "禁用自启动: sudo systemctl disable myapp.service"
echo "================================================"

