import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from scipy import stats

st.set_page_config(page_title="风险指标", page_icon="⚠️", layout="wide")

st.title("⚠️ 风险指标计算")
st.markdown("### 全面的金融风险度量和分析")

# 模拟收益率生成函数
def generate_returns_data(ticker, days=252):
    """生成模拟收益率数据"""
    np.random.seed(hash(ticker) % 10000)
    
    # 不同资产的参数
    if "SPY" in ticker or "VTI" in ticker:
        mu, sigma = 0.0003, 0.01
    elif "AAPL" in ticker or "MSFT" in ticker:
        mu, sigma = 0.0005, 0.015
    elif "TSLA" in ticker or "NVDA" in ticker:
        mu, sigma = 0.0008, 0.025
    else:
        mu, sigma = 0.0004, 0.018
    
    # 生成收益率序列
    returns = np.zeros(days)
    for i in range(days):
        if i == 0:
            returns[i] = np.random.normal(mu, sigma)
        else:
            returns[i] = 0.1 * returns[i-1] + np.random.normal(mu, sigma * (1 + 0.5 * abs(returns[i-1])))
    
    # 添加一些极端事件
    extreme_days = np.random.choice(days, size=max(1, days//50), replace=False)
    returns[extreme_days] *= np.random.choice([-2, 2], size=len(extreme_days))
    
    return pd.Series(returns, index=pd.date_range(end=datetime.now(), periods=days, freq='B'))

# 风险计算函数
def calculate_risk_metrics(returns, confidence_level=0.95):
    """计算风险指标"""
    metrics = {}
    
    if len(returns) == 0:
        return metrics
    
    # 基础统计
    metrics['mean_return'] = returns.mean()
    metrics['std_return'] = returns.std()
    
    # 年化指标
    metrics['annual_return'] = metrics['mean_return'] * 252
    metrics['annual_volatility'] = metrics['std_return'] * np.sqrt(252)
    
    # VaR (历史模拟法)
    metrics['var'] = np.percentile(returns, (1 - confidence_level) * 100)
    
    # CVaR
    var_threshold = metrics['var']
    tail_returns = returns[returns <= var_threshold]
    metrics['cvar'] = tail_returns.mean() if len(tail_returns) > 0 else metrics['var']
    
    # 夏普比率（假设无风险利率2%）
    risk_free_rate = 0.02
    if metrics['annual_volatility'] > 0:
        metrics['sharpe_ratio'] = (metrics['annual_return'] - risk_free_rate) / metrics['annual_volatility']
    else:
        metrics['sharpe_ratio'] = 0
    
    # 偏度和峰度
    metrics['skewness'] = stats.skew(returns)
    metrics['kurtosis'] = stats.kurtosis(returns)
    
    return metrics

# 侧边栏
st.sidebar.header("风险分析设置")

# 资产选择
risk_ticker = st.sidebar.text_input("股票/资产代码", "SPY").upper()

# 热门资产快捷按钮
st.sidebar.markdown("### 📈 热门资产")
hot_assets = ["SPY", "AAPL", "TSLA", "BTC-USD", "GC=F"]
for asset in hot_assets:
    if st.sidebar.button(asset, key=f"risk_{asset}", use_container_width=True):
        st.session_state['risk_ticker'] = asset
        st.experimental_rerun()

# 风险参数
st.sidebar.subheader("风险参数")
confidence_level = st.sidebar.slider("置信水平", 0.90, 0.99, 0.95, 0.01)
lookback_days = st.sidebar.slider("回看天数", 30, 1000, 252, 10)

if st.sidebar.button("计算风险指标", type="primary"):
    with st.spinner("正在计算风险指标..."):
        try:
            # 生成数据
            returns = generate_returns_data(risk_ticker, lookback_days)
            
            if len(returns) < 30:
                st.error("数据不足，无法进行有效的风险分析")
            else:
                # 计算风险指标
                metrics = calculate_risk_metrics(returns, confidence_level)
                
                # 显示核心指标卡片
                st.subheader("主要风险指标")
                
                cols = st.columns(4)
                
                core_metrics = [
                    ("年化波动率", f"{metrics.get('annual_volatility', 0)*100:.2f}%", "波动风险", "#EF4444"),
                    (f"VaR ({confidence_level*100:.0f}%)", f"{metrics.get('var', 0)*100:.2f}%", "在险价值", "#DC2626"),
                    ("夏普比率", f"{metrics.get('sharpe_ratio', 0):.2f}", "风险调整收益", "#10B981"),
                    ("最大损失", f"{returns.min()*100:.2f}%", "历史最差", "#8B5CF6")
                ]
                
                for col, (label, value, desc, color) in zip(cols, core_metrics):
                    with col:
                        st.markdown(f'''
                        <div style="
                            background: white;
                            padding: 1rem;
                            border-radius: 10px;
                            border-left: 5px solid {color};
                            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                            text-align: center;
                        ">
                            <h4 style="margin: 0; color: #666;">{label}</h4>
                            <h2 style="margin: 0.5rem 0; color: {color};">{value}</h2>
                            <p style="margin: 0; color: #9CA3AF; font-size: 0.9em;">{desc}</p>
                        </div>
                        ''', unsafe_allow_html=True)
                
                # 收益率分布图
                st.subheader("收益率分布分析")
                
                fig1 = go.Figure()
                fig1.add_trace(go.Histogram(
                    x=returns * 100,
                    nbinsx=50,
                    name="收益率分布",
                    opacity=0.7,
                    marker_color='#3B82F6'
                ))
                
                # 添加VaR线
                var_line = metrics.get('var', 0) * 100
                fig1.add_vline(x=var_line, line_dash="dash", line_color="orange", 
                              annotation_text=f"VaR ({confidence_level*100:.0f}%)")
                
                fig1.update_layout(
                    title="收益率分布",
                    xaxis_title="日收益率 (%)",
                    yaxis_title="频率",
                    height=400
                )
                
                st.plotly_chart(fig1, use_container_width=True)
                
                # 详细指标
                st.subheader("详细风险指标")
                
                detail_cols = st.columns(3)
                
                detail_metrics = [
                    ("CVaR", f"{metrics.get('cvar', 0)*100:.2f}%", "条件在险价值"),
                    ("年化收益", f"{metrics.get('annual_return', 0)*100:.2f}%", "预期收益"),
                    ("偏度", f"{metrics.get('skewness', 0):.3f}", "分布不对称性"),
                    ("峰度", f"{metrics.get('kurtosis', 0):.3f}", "尾部厚度"),
                    ("平均日收益", f"{metrics.get('mean_return', 0)*100:.4f}%", "日收益率均值"),
                    ("日收益标准差", f"{metrics.get('std_return', 0)*100:.4f}%", "日收益率波动")
                ]
                
                for i in range(0, 6, 3):
                    cols = st.columns(3)
                    for j in range(3):
                        if i+j < len(detail_metrics):
                            label, value, desc = detail_metrics[i+j]
                            with cols[j]:
                                st.metric(label, value, desc)
                
        except Exception as e:
            st.error(f"计算失败: {str(e)}")

# 初始说明
if not st.sidebar.button:
    st.info("👈 在左侧配置风险分析参数")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 风险指标详解
        
        #### 在险价值 (VaR)
        
        **定义**: 在给定置信水平下的最大可能损失。
        
        **计算方法**:
        1. **历史模拟法**: 基于历史收益率分布
        2. **参数法**: 假设正态分布
        3. **蒙特卡洛法**: 模拟大量随机路径
        """)
    
    with col2:
        st.markdown("""
        #### 条件在险价值 (CVaR)
        
        **定义**: 当损失超过VaR时的平均损失。
        
        **优点**:
        - 考虑尾部风险
        - 更全面的风险度量
        
        #### 其他重要指标
        
        **波动率**: 价格变动的标准差
        **夏普比率**: 风险调整后收益
        **偏度**: 分布不对称性
        **峰度**: 尾部厚度
        """)
