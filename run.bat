@echo off
echo 正在启动 FinRisk Pro...
echo.

cd /d D:\finrisk-pro

REM 检查虚拟环境
if not exist venv (
    echo 错误: 虚拟环境不存在
    pause
    exit /b 1
)

REM 激活虚拟环境
call venv\Scripts\activate.bat

REM 查找可用端口
set port=8502
:check_port
netstat -ano | findstr ":%port%" >nul
if %errorlevel% equ 0 (
    echo 端口 %port% 被占用，尝试端口 8503...
    set port=8503
    goto check_port
)

echo 使用端口: %port%
echo 启动应用...
echo 访问: http://localhost:%port%
echo.
streamlit run app\Home.py --server.port %port%

pause
