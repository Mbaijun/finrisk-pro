@echo off
echo ========================================
echo   FinRisk Pro - 金融风险分析平台
echo ========================================
echo.

cd /d D:\finrisk-pro

REM 激活虚拟环境
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo 错误: 虚拟环境不存在
    pause
    exit /b 1
)

REM 安装必要依赖（如果需要）
echo 检查依赖包...
pip install --quiet streamlit pandas numpy plotly yfinance

REM 运行启动脚本
echo.
echo 正在启动应用...
echo 按 Ctrl+C 停止应用
echo.
python start_finrisk.py

pause
