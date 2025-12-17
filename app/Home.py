# -*- coding: utf-8 -*-
import streamlit as st

st.set_page_config(
    page_title="FinRisk Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 3rem;
        color: #1E3A8A;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #4B5563;
        margin-bottom: 2rem;
    }
    .feature-card {
        background-color: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 4px solid #3B82F6;
    }
    .quick-start {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 标题
st.markdown('<h1 class="main-title">📊 FinRisk Pro</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">全自动金融风险分析与投资组合管理平台</p>', unsafe_allow_html=True)

# 平台简介
st.markdown("""
### 🎯 平台简介

**FinRisk Pro** 是一个专业的金融风险分析平台，集成了实时市场数据分析、全面风险指标计算、
智能投资组合优化和可视化报表生成等功能。

无论您是个人投资者、金融分析师还是风险管理专业人士，FinRisk Pro 都能为您提供强大的分析工具。
""")

# 功能卡片
st.markdown("## 🚀 核心功能")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>📊 股票分析</h3>
        <p>实时获取股票数据，进行技术分析和基本面分析</p>
        <ul>
            <li>价格走势图表</li>
            <li>技术指标计算</li>
            <li>基本面数据查看</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h3>📈 风险指标</h3>
        <p>计算各类金融风险指标</p>
        <ul>
            <li>VaR / CVaR 计算</li>
            <li>波动率分析</li>
            <li>夏普比率计算</li>
            <li>压力测试</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>⚖️ 投资组合</h3>
        <p>构建和优化投资组合</p>
        <ul>
            <li>多资产组合管理</li>
            <li>风险收益优化</li>
            <li>相关性分析</li>
            <li>回测分析</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h3>📋 报告生成</h3>
        <p>生成专业分析报告</p>
        <ul>
            <li>自定义报告模板</li>
            <li>多种导出格式</li>
            <li>历史报告管理</li>
            <li>自动化报告</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# 快速开始指南
st.markdown("""
<div class="quick-start">
    <h2 style="color: white;">🚀 快速开始</h2>
    <ol style="color: white; font-size: 1.1rem;">
        <li><strong>左侧导航栏</strong>选择您需要的功能模块</li>
        <li><strong>输入股票代码</strong>（如：AAPL, MSFT, TSLA）</li>
        <li><strong>设置分析参数</strong>（时间范围、风险偏好等）</li>
        <li><strong>点击"开始分析"</strong>获取详细报告</li>
        <li><strong>导出结果</strong>或保存分析配置</li>
    </ol>
</div>
""", unsafe_allow_html=True)

# 技术栈
st.markdown("## 🛠️ 技术栈")

tech_cols = st.columns(4)
technologies = [
    ("Python", "编程语言"),
    ("Streamlit", "Web应用框架"),
    ("yFinance", "金融数据"),
    ("Plotly", "可视化图表"),
    ("Pandas", "数据处理"),
    ("NumPy", "数值计算"),
    ("Scikit-learn", "机器学习"),
    ("TA-Lib", "技术指标")
]

for i in range(0, 8, 4):
    cols = st.columns(4)
    for j in range(4):
        if i+j < len(technologies):
            name, desc = technologies[i+j]
            with cols[j]:
                st.markdown(f"**{name}**")
                st.caption(desc)

# 成功消息
st.success("""
✅ **FinRisk Pro 已成功启动！**
请使用左侧导航栏访问各个功能模块，开始您的金融分析之旅。
""")

# 页脚
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem 0;">
    <p>© 2024 FinRisk Pro | 版本 1.0.0</p>
    <p>数据来源：Yahoo Finance | 仅供学习和研究使用</p>
    <p style="font-size: 0.9em;">⚠️ 免责声明：本平台提供的数据和分析结果仅供参考，不构成投资建议</p>
</div>
""", unsafe_allow_html=True)
