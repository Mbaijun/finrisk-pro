# start_finrisk.py - 启动脚本
import os
import sys
import subprocess
import argparse

def setup_environment():
    """设置运行环境"""
    print("🚀 设置 FinRisk Pro 环境...")
    
    # 创建必要的目录
    directories = [
        './data',
        './data/cache',
        './reports',
        './logs',
        './src'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  创建目录: {directory}")
    
    # 检查依赖
    print("\n📦 检查依赖包...")
    try:
        import streamlit
        import pandas
        import numpy
        import plotly
        print("  核心依赖: ✓")
    except ImportError as e:
        print(f"  缺少依赖: {e}")
        print("  运行: pip install -r requirements.txt")
        return False
    
    return True

def find_available_port(start_port=8502, max_attempts=10):
    """查找可用端口"""
    import socket
    
    for port in range(start_port, start_port + max_attempts):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            
            if result != 0:
                return port
        except:
            continue
    
    return start_port + max_attempts

def clear_cache(days_old=7):
    """清除旧的缓存文件"""
    import time
    from pathlib import Path
    
    cache_dir = Path('./data/cache')
    if not cache_dir.exists():
        return
    
    current_time = time.time()
    cutoff = current_time - (days_old * 24 * 60 * 60)
    
    deleted = 0
    for file in cache_dir.glob('*.pkl'):
        if file.stat().st_mtime < cutoff:
            try:
                file.unlink()
                deleted += 1
            except:
                pass
    
    if deleted > 0:
        print(f"🗑️  已清除 {deleted} 个旧缓存文件")

def main():
    parser = argparse.ArgumentParser(description='启动 FinRisk Pro')
    parser.add_argument('--port', type=int, help='指定端口号')
    parser.add_argument('--clear-cache', action='store_true', help='清除缓存')
    parser.add_argument('--no-browser', action='store_true', help='不自动打开浏览器')
    args = parser.parse_args()
    
    print("=" * 50)
    print("📊 FinRisk Pro - 金融风险分析平台")
    print("=" * 50)
    
    # 清除缓存（如果需要）
    if args.clear_cache:
        clear_cache()
    
    # 设置环境
    if not setup_environment():
        print("❌ 环境设置失败")
        return
    
    # 查找可用端口
    port = args.port if args.port else find_available_port()
    
    print(f"\n🌐 使用端口: {port}")
    print(f"📁 数据目录: ./data/cache")
    
    # 构建启动命令
    cmd = [
        sys.executable, '-m', 'streamlit', 'run',
        'app/Home.py',
        '--server.port', str(port),
        '--server.address', 'localhost',
        '--theme.base', 'light',
    ]
    
    if args.no_browser:
        cmd.extend(['--server.headless', 'true'])
    
    print(f"\n🚀 启动应用...")
    print(f"🔗 访问: http://localhost:{port}")
    print("\n按 Ctrl+C 停止应用")
    print("-" * 50)
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

if __name__ == '__main__':
    main()
