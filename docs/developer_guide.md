
FinRisk Pro 开发指南
开发环境设置
1. 环境准备
bash

复制

下载
# 克隆项目
git clone https://github.com/yourusername/finrisk-pro.git
cd finrisk-pro

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate.bat
# Linux/Mac
source venv/bin/activate

# 安装开发依赖
pip install -r requirements-dev.txt
2. 项目结构说明
text

复制

下载
finrisk-pro/
 app/                    # Streamlit应用
    Home.py            # 主页面
    pages/             # 子页面（自动加载）
 src/                   # Python模块
    data_acquisition/  # 数据获取
    risk_metrics/      # 风险计算
    portfolio/         # 投资组合
    utils/             # 工具函数
 tests/                 # 测试代码
 docs/                  # 文档
 config/               # 配置文件
开发规范
1. 代码规范
使用PEP 8编码规范

函数和类使用英文命名

添加必要的文档字符串

保持代码简洁可读

2. 页面开发
python

复制

下载
# 页面文件模板
import streamlit as st

st.set_page_config(
    page_title="页面标题",
    page_icon="🎯",
    layout="wide"
)

def main():
    st.title("页面标题")
    
    # 侧边栏配置
    with st.sidebar:
        st.header("配置")
        # 配置选项...
    
    # 主内容区
    col1, col2 = st.columns(2)
    
    with col1:
        # 内容...
        pass
    
    with col2:
        # 内容...
        pass

if __name__ == "__main__":
    main()
3. 数据管理
使用 src/data_manager.py 统一管理数据

实现缓存机制减少API调用

优雅降级到模拟数据

4. 错误处理
python

复制

下载
try:
    # 可能失败的操作
    data = fetch_data(ticker)
except APIError as e:
    st.error(f"API错误: {e}")
    # 降级到模拟数据
    data = generate_mock_data(ticker)
except Exception as e:
    st.error(f"未知错误: {e}")
    st.info("请稍后重试或联系支持")
添加新功能
1. 添加新页面
在 app/pages/ 目录创建新文件

文件名格式: 数字_图标_页面名.py

实现页面逻辑

重启应用测试

2. 添加新数据源
在 src/data_acquisition/ 添加模块

实现数据获取接口

在 data_manager.py 中集成

更新配置选项

3. 添加新分析指标
在 src/risk_metrics/ 或 src/portfolio/ 添加函数

实现指标计算逻辑

在相关页面中调用

添加可视化展示

测试
1. 单元测试
bash

复制

下载
# 运行所有测试
pytest tests/

# 运行特定测试
pytest tests/test_data_manager.py

# 带覆盖率报告
pytest --cov=src tests/
2. 集成测试
手动测试页面功能

测试数据流完整性

测试错误处理机制

3. 性能测试
测试页面加载速度

测试大数据量处理

测试并发访问

部署
1. 本地部署
bash

复制

下载
# 开发模式
streamlit run app/Home.py --server.port 8501

# 生产模式（建议）
streamlit run app/Home.py \
  --server.port 8501 \
  --server.headless true \
  --server.enableCORS false \
  --server.enableXsrfProtection false
2. Docker部署
dockerfile

复制

下载
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app/Home.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0"]
3. 云平台部署
Streamlit Cloud: 免费，简单

Heroku: 支持自定义配置

AWS/GCP/Azure: 企业级部署

版本控制
1. Git工作流
bash

复制

下载
# 创建功能分支
git checkout -b feature/new-feature

# 提交更改
git add .
git commit -m "Add: 新功能描述"

# 推送到远程
git push origin feature/new-feature

# 创建Pull Request
2. 版本号规范
主版本号.次版本号.修订号 (MAJOR.MINOR.PATCH)

遵循语义化版本控制

更新 CHANGELOG.md

性能优化
1. 前端优化
减少页面重绘

使用Streamlit缓存

优化图表渲染

2. 后端优化
数据缓存策略

异步数据加载

数据库优化

3. 数据库优化
索引优化

查询优化

连接池管理

安全考虑
1. 数据安全
API密钥安全管理

用户数据加密

访问控制

2. 应用安全
输入验证和清理

SQL注入防护

XSS防护

3. 部署安全
HTTPS强制

防火墙配置

定期安全更新

监控和日志
1. 应用监控
性能监控

错误监控

用户行为分析

2. 日志记录
python

复制

下载
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
贡献指南
1. 代码贡献
Fork项目

创建功能分支

编写代码和测试

提交Pull Request

2. 文档贡献
更新README

编写使用指南

添加API文档

3. 问题反馈
查看现有Issues

创建新Issue

提供详细描述和复现步骤

保持更新: 定期从主分支拉取更新
交流渠道: GitHub Discussions / Discord
代码审查: 所有更改需要至少一个review
