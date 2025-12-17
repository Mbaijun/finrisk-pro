# FinRisk Pro 📊

[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-FF4B4B?logo=streamlit)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**全自动金融风险分析与投资组合管理平台**

## ✨ 功能特性

- 📈 **股票分析**: 个股技术分析与基本面分析
- ⚖️ **投资组合**: 多资产组合构建与优化
- ⚠️ **风险指标**: 全面的金融风险度量（VaR、CVaR、波动率等）
- 📋 **报告生成**: 专业级分析报告导出
- 🤖 **智能数据**: 模拟数据与缓存机制，避免API限制
- 🎨 **美观界面**: Streamlit构建的现代化Web界面

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Windows/Mac/Linux

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/yourusername/finrisk-pro.git
cd finrisk-pro
创建虚拟环境

bash

复制

下载
python -m venv venv
# Windows
venv\Scripts\activate.bat
# Linux/Mac
source venv/bin/activate
安装依赖

bash

复制

下载
pip install -r requirements.txt
运行应用

bash

复制

下载
streamlit run app/Home.py
访问应用
打开浏览器访问: http://localhost:8501

📁 项目结构
text

复制

下载
finrisk-pro/
├── app/                    # Streamlit应用
│   ├── Home.py            # 主页面
│   └── pages/             # 子页面
│       ├── 01_📊_股票分析.py
│       ├── 02_⚖️_投资组合.py
│       ├── 03_📈_风险指标.py
│       └── 04_📋_报告生成.py
├── src/                   # 源代码
│   └── data_manager.py    # 数据管理模块
├── data/                  # 数据目录
│   └── cache/             # 数据缓存
├── docs/                  # 文档
├── config.py              # 配置文件
├── requirements.txt       # 依赖包
└── README.md              # 项目说明
🔧 配置说明
数据源配置
默认使用模拟数据，避免API限制。如需使用真实数据：

在页面中取消勾选"使用模拟数据"

注意：yFinance有API频率限制

缓存设置
数据默认缓存24小时

缓存目录: ./data/cache/

可手动清理缓存文件

📊 功能详解
1. 股票分析
价格走势图（K线图）

技术指标计算

收益率分析

基本面数据（模拟）

2. 投资组合
多资产组合构建

等权重/自定义权重

组合表现分析

风险收益指标

3. 风险指标
Value at Risk (VaR)

Conditional VaR (CVaR)

波动率计算

夏普比率

最大回撤

4. 报告生成
HTML报告导出

Excel数据下载

文本报告

打印功能

🤝 贡献指南
欢迎贡献代码！请按以下步骤：

Fork项目

创建功能分支 (git checkout -b feature/AmazingFeature)

提交更改 (git commit -m 'Add some AmazingFeature')

推送到分支 (git push origin feature/AmazingFeature)

提交Pull Request

📄 许可证
本项目采用 MIT 许可证 - 查看 LICENSE 文件了解详情。

🙏 致谢
Streamlit - 应用框架

yFinance - 金融数据

Plotly - 可视化图表

Pandas - 数据处理

📞 联系
如有问题或建议，请通过以下方式联系：

GitHub Issues: 项目Issues页面

Email: your.email@example.com

⚠️ 免责声明: 本工具仅用于学习和研究目的，不构成投资建议。金融投资有风险，请谨慎决策。