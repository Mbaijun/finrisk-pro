@echo off
echo ==========================================
echo    FinRisk Pro 部署脚本 (Windows)
echo ==========================================
echo.

:menu
echo 请选择部署方式：
echo 1. 本地开发环境
echo 2. Docker部署
echo 3. 部署到Streamlit Cloud
echo 4. 退出
echo.
set /p choice="请选择 (1-4): "

if "%choice%"=="1" goto local
if "%choice%"=="2" goto docker
if "%choice%"=="3" goto streamlit
if "%choice%"=="4" goto exit
echo 无效选择，请重新输入
goto menu

:local
echo.
echo 开始本地开发环境部署...
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: Python未安装
    pause
    exit /b 1
)

REM 创建虚拟环境
if not exist venv (
    echo 创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate.bat

REM 安装依赖
echo 安装依赖包...
pip install --upgrade pip
pip install -r requirements.txt

REM 创建必要目录
echo 创建数据目录...
mkdir data\cache 2>nul
mkdir logs 2>nul
mkdir reports 2>nul

REM 启动应用
echo.
echo 应用将在 http://localhost:8501 启动
echo 按 Ctrl+C 停止应用
echo.
streamlit run app\Home.py --server.port 8501
goto end

:docker
echo.
echo 开始Docker部署...
echo.

REM 检查Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo 错误: Docker未安装
    pause
    exit /b 1
)

echo 构建Docker镜像...
docker build -t finrisk-pro:latest .

echo.
echo 启动容器...
docker run -d ^
    --name finrisk-pro ^
    -p 8501:8501 ^
    -v %CD%\data:/app/data ^
    finrisk-pro:latest

echo.
echo 部署完成！
echo 应用地址: http://localhost:8501
echo.
echo 常用命令:
echo   查看日志: docker logs finrisk-pro
echo   停止应用: docker stop finrisk-pro
echo   重启应用: docker restart finrisk-pro
echo   删除容器: docker rm finrisk-pro
goto end

:streamlit
echo.
echo 准备Streamlit Cloud部署...
echo.

REM 检查streamlit配置
if not exist .streamlit\config.toml (
    echo 创建Streamlit配置...
    mkdir .streamlit 2>nul
    echo [server] > .streamlit\config.toml
    echo port = 8501 >> .streamlit\config.toml
    echo address = "0.0.0.0" >> .streamlit\config.toml
    echo enableCORS = false >> .streamlit\config.toml
    echo enableXsrfProtection = false >> .streamlit\config.toml
    echo. >> .streamlit\config.toml
    echo [browser] >> .streamlit\config.toml
    echo serverAddress = "0.0.0.0" >> .streamlit\config.toml
    echo. >> .streamlit\config.toml
    echo [theme] >> .streamlit\config.toml
    echo primaryColor = "#3B82F6" >> .streamlit\config.toml
    echo backgroundColor = "#FFFFFF" >> .streamlit\config.toml
    echo secondaryBackgroundColor = "#F0F2F6" >> .streamlit\config.toml
    echo textColor = "#262730" >> .streamlit\config.toml
    echo font = "sans serif" >> .streamlit\config.toml
)

echo.
echo Streamlit Cloud部署准备完成！
echo.
echo 请按照以下步骤操作：
echo 1. 推送代码到GitHub仓库
echo 2. 访问 https://streamlit.io/cloud
echo 3. 点击'New app'按钮
echo 4. 选择您的仓库和分支
echo 5. 设置文件路径为: app/Home.py
echo 6. 点击'Deploy!'按钮
echo.
echo 注意：确保requirements.txt包含所有依赖
goto end

:exit
echo 退出部署脚本
exit /b 0

:end
echo.
pause
