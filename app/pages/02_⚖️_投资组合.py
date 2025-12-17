import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="投资组合", page_icon="⚖️", layout="wide")

st.title("⚖️ 投资组合分析")
st.markdown("### 构建和优化您的投资组合")

# 模拟数据生成函数
def generate_portfolio_data(tickers, days=252):
    """生成模拟投资组合数据"""
    dates = pd.date_range(end=datetime.now(), periods=days, freq='B')
    portfolio_data = pd.DataFrame(index=dates)
    
    for ticker in tickers:
        # 根据股票代码生成不同的参数
        if ticker in ["AAPL", "MSFT", "GOOGL"]:
            base_price = np.random.uniform(100, 300)
            daily_return = 0.0005
            volatility = 0.015
        elif ticker in ["TSLA", "NVDA"]:
            base_price = np.random.uniform(50, 200)
            daily_return = 0.0008
            volatility = 0.025
        else:
            base_price = np.random.uniform(50, 150)
            daily_return = 0.0004
            volatility = 0.018
        
        # 生成价格序列
        returns = np.random.normal(daily_return, volatility, days)
        prices = base_price * np.exp(np.cumsum(returns))
        
        portfolio_data[ticker] = prices
    
    return portfolio_data

# 侧边栏配置
st.sidebar.header("投资组合设置")

# 股票选择
portfolio_stocks = st.sidebar.text_area(
    "输入股票代码（每行一个）",
    "AAPL\nMSFT\nGOOGL",
    height=150
)

# 权重设置
st.sidebar.subheader("权重设置")
equal_weights = st.sidebar.checkbox("使用等权重", True)

# 示例组合
st.sidebar.markdown("### 📋 示例组合")
if st.sidebar.button("科技组合", key="tech_port"):
    portfolio_stocks = "AAPL\nMSFT\nGOOGL\nNVDA\nTSLA"

if st.sidebar.button("稳健组合", key="stable_port"):
    portfolio_stocks = "JPM\nJNJ\nWMT\nPG\nSPY"

if st.sidebar.button("开始分析", type="primary"):
    with st.spinner("正在分析投资组合..."):
        try:
            # 解析股票列表
            tickers = [t.strip().upper() for t in portfolio_stocks.split("\n") if t.strip()]
            
            if len(tickers) < 1:
                st.error("请至少输入1个股票代码")
            else:
                # 生成数据
                data = generate_portfolio_data(tickers)
                
                # 等权重组合
                weights = np.ones(len(tickers)) / len(tickers)
                weight_dict = dict(zip(tickers, weights))
                
                # 标签页
                tab1, tab2 = st.tabs(["📊 组合表现", "📈 资产配置"])
                
                with tab1:
                    st.subheader("投资组合表现")
                    
                    # 计算组合收益率
                    returns = data.pct_change().dropna()
                    portfolio_returns = (returns * list(weight_dict.values())).sum(axis=1)
                    
                    # 累计收益
                    cumulative_returns = (1 + portfolio_returns).cumprod() - 1
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=cumulative_returns.index,
                        y=cumulative_returns * 100,
                        mode='lines',
                        name='投资组合',
                        line=dict(color='blue', width=3)
                    ))
                    
                    fig.update_layout(
                        title="投资组合累计收益率",
                        yaxis_title="累计收益率 (%)",
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # 性能指标
                    st.subheader("性能指标")
                    
                    annual_return = portfolio_returns.mean() * 252
                    annual_volatility = portfolio_returns.std() * np.sqrt(252)
                    sharpe_ratio = annual_return / annual_volatility if annual_volatility > 0 else 0
                    
                    # 最大回撤
                    cumulative = (1 + portfolio_returns).cumprod()
                    max_dd = (cumulative / cumulative.cummax() - 1).min()
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("年化收益", f"{annual_return*100:.2f}%")
                    with col2:
                        st.metric("年化波动", f"{annual_volatility*100:.2f}%")
                    with col3:
                        st.metric("夏普比率", f"{sharpe_ratio:.2f}")
                    with col4:
                        st.metric("最大回撤", f"{max_dd*100:.2f}%")
                
                with tab2:
                    st.subheader("资产配置")
                    
                    # 饼图显示权重
                    fig2 = px.pie(
                        values=list(weight_dict.values()),
                        names=list(weight_dict.keys()),
                        title="投资组合权重分配",
                        hole=0.4
                    )
                    
                    st.plotly_chart(fig2, use_container_width=True)
                    
                    # 权重表格
                    weights_df = pd.DataFrame({
                        '股票': list(weight_dict.keys()),
                        '权重': [f"{w*100:.1f}%" for w in weight_dict.values()],
                        '当前价格': [data[t].iloc[-1] if t in data.columns else 0 for t in weight_dict.keys()]
                    })
                    
                    st.dataframe(weights_df, use_container_width=True)
                    
        except Exception as e:
            st.error(f"分析失败: {str(e)}")

# 初始说明
if not st.sidebar.button:
    st.info("👈 在左侧配置您的投资组合")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 投资组合理论
        
        **现代投资组合理论 (MPT)**
        
        - **核心思想**: 通过分散投资降低风险
        - **有效前沿**: 最优风险收益组合的集合
        - **关键指标**: 夏普比率、波动率、相关性
        
        **常用优化策略**
        
        1. **最大化夏普比率**
           - 寻找最优风险收益比
        2. **最小化波动率**
           - 适合风险厌恶投资者
        3. **等权重分配**
           - 简单有效的策略
        """)
    
    with col2:
        st.markdown("""
        ### 构建步骤
        
        1. **选择资产**
           - 股票、ETF等
        2. **设置权重**
           - 等权重或自定义
        3. **分析评估**
           - 计算风险收益指标
        4. **优化调整**
           - 根据目标调整配置
        
        ### 注意事项
        
        - 模拟数据用于演示
        - 实际投资需谨慎
        - 建议多元化投资
        """)
