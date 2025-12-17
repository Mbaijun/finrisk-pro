# deploy.sh - FinRisk Pro 部署脚本
#!/bin/bash

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查命令是否存在
check_command() {
    if ! command -v $1 &> /dev/null; then
        log_error "$1 未安装，请先安装 $1"
        exit 1
    fi
}

# 显示横幅
show_banner() {
    echo "=========================================="
    echo "  FinRisk Pro 部署脚本"
    echo "  版本: 1.0.0"
    echo "=========================================="
    echo ""
}

# 部署选项菜单
show_menu() {
    echo "请选择部署方式："
    echo "1. 本地开发环境"
    echo "2. Docker部署"
    echo "3. Docker Compose部署"
    echo "4. 部署到Streamlit Cloud"
    echo "5. 部署到Heroku"
    echo "6. 退出"
    echo ""
    read -p "请选择 (1-6): " choice
}

# 本地开发环境部署
deploy_local() {
    log_info "开始本地开发环境部署..."
    
    # 检查Python
    check_command python3
    
    # 创建虚拟环境
    if [ ! -d "venv" ]; then
        log_info "创建虚拟环境..."
        python3 -m venv venv
    fi
    
    # 激活虚拟环境
    log_info "激活虚拟环境..."
    source venv/bin/activate
    
    # 安装依赖
    log_info "安装依赖包..."
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # 创建必要目录
    log_info "创建数据目录..."
    mkdir -p data/cache logs reports
    
    # 启动应用
    log_info "启动应用..."
    echo ""
    echo "应用将在 http://localhost:8501 启动"
    echo "按 Ctrl+C 停止应用"
    echo ""
    
    streamlit run app/Home.py --server.port 8501
}

# Docker部署
deploy_docker() {
    log_info "开始Docker部署..."
    check_command docker
    
    # 构建镜像
    log_info "构建Docker镜像..."
    docker build -t finrisk-pro:latest .
    
    # 运行容器
    log_info "启动容器..."
    docker run -d \
        --name finrisk-pro \
        -p 8501:8501 \
        -v $(pwd)/data:/app/data \
        finrisk-pro:latest
    
    log_info "部署完成！"
    echo "应用地址: http://localhost:8501"
    echo ""
    echo "常用命令:"
    echo "  查看日志: docker logs finrisk-pro"
    echo "  停止应用: docker stop finrisk-pro"
    echo "  重启应用: docker restart finrisk-pro"
    echo "  删除容器: docker rm finrisk-pro"
}

# Docker Compose部署
deploy_docker_compose() {
    log_info "开始Docker Compose部署..."
    check_command docker
    check_command docker-compose
    
    # 检查环境变量文件
    if [ ! -f ".env" ]; then
        log_warn ".env 文件不存在，使用 .env.example 模板"
        cp .env.example .env
        log_warn "请编辑 .env 文件设置实际值"
    fi
    
    # 启动服务
    log_info "启动服务..."
    docker-compose -f docker-compose.yml up -d
    
    log_info "部署完成！"
    echo "应用地址: http://localhost:8501"
    echo "数据库: localhost:5432"
    echo "Redis: localhost:6379"
    echo ""
    echo "常用命令:"
    echo "  查看所有服务: docker-compose ps"
    echo "  查看日志: docker-compose logs -f"
    echo "  停止服务: docker-compose down"
    echo "  重启服务: docker-compose restart"
}

# Streamlit Cloud部署
deploy_streamlit_cloud() {
    log_info "准备Streamlit Cloud部署..."
    
    # 检查streamlit配置
    if [ ! -f ".streamlit/config.toml" ]; then
        log_warn "创建Streamlit配置..."
        mkdir -p .streamlit
        cat > .streamlit/config.toml << EOF
[server]
port = 8501
address = "0.0.0.0"
enableCORS = false
enableXsrfProtection = false

[browser]
serverAddress = "0.0.0.0"

[theme]
primaryColor = "#3B82F6"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
EOF
    fi
    
    # 检查requirements.txt
    if [ ! -f "requirements.txt" ]; then
        log_error "requirements.txt 文件不存在"
        exit 1
    fi
    
    log_info "Streamlit Cloud部署准备完成！"
    echo ""
    echo "请按照以下步骤操作："
    echo "1. 推送代码到GitHub仓库"
    echo "2. 访问 https://streamlit.io/cloud"
    echo "3. 点击'New app'按钮"
    echo "4. 选择您的仓库和分支"
    echo "5. 设置文件路径为: app/Home.py"
    echo "6. 点击'Deploy!'按钮"
    echo ""
    echo "注意：确保requirements.txt包含所有依赖"
}

# Heroku部署
deploy_heroku() {
    log_info "准备Heroku部署..."
    check_command heroku
    
    # 检查是否已登录
    if ! heroku whoami &> /dev/null; then
        log_error "请先登录Heroku: heroku login"
        exit 1
    fi
    
    # 创建Procfile
    if [ ! -f "Procfile" ]; then
        log_info "创建Procfile..."
        echo "web: streamlit run app/Home.py --server.port=$PORT --server.address=0.0.0.0" > Procfile
    fi
    
    # 创建runtime.txt
    if [ ! -f "runtime.txt" ]; then
        log_info "创建runtime.txt..."
        echo "python-3.9.16" > runtime.txt
    fi
    
    # 创建setup.sh
    if [ ! -f "setup.sh" ]; then
        log_info "创建setup.sh..."
        cat > setup.sh << 'EOF'
#!/bin/bash
mkdir -p ~/.streamlit/
echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
enableXsrfProtection = false\n\
" > ~/.streamlit/config.toml
EOF
        chmod +x setup.sh
    fi
    
    log_info "Heroku部署准备完成！"
    echo ""
    echo "请按照以下步骤操作："
    echo "1. 创建Heroku应用: heroku create finrisk-pro"
    echo "2. 推送代码: git push heroku main"
    echo "3. 打开应用: heroku open"
    echo ""
    echo "可选步骤："
    echo "  添加数据库: heroku addons:create heroku-postgresql"
    echo "  查看日志: heroku logs --tail"
}

# 主函数
main() {
    show_banner
    
    while true; do
        show_menu
        
        case $choice in
            1)
                deploy_local
                break
                ;;
            2)
                deploy_docker
                break
                ;;
            3)
                deploy_docker_compose
                break
                ;;
            4)
                deploy_streamlit_cloud
                break
                ;;
            5)
                deploy_heroku
                break
                ;;
            6)
                log_info "退出部署脚本"
                exit 0
                ;;
            *)
                log_error "无效选择，请重新输入"
                ;;
        esac
    done
}

# 运行主函数
main "$@"
