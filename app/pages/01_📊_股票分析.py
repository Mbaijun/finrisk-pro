import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="股票分析", page_icon="📊", layout="wide")

st.title("📊 股票分析")
st.markdown("### 个股技术分析与基本面分析")

# 简单的数据生成函数（内联定义，避免导入问题）
def generate_stock_data(ticker, period="1y"):
    """生成模拟股票数据"""
    
    # 根据周期确定天数
    period_days = {
        "1mo": 30, "3mo": 90, "6mo": 180,
        "1y": 252, "2y": 504, "5y": 1260
    }
    days = period_days.get(period, 252)
    
    # 根据股票代码设置不同的参数
    if ticker in ["AAPL", "MSFT", "GOOGL", "AMZN"]:
        base_price = np.random.uniform(100, 500)
        daily_return = 0.0005
        volatility = 0.015
    elif ticker in ["TSLA", "NVDA"]:
        base_price = np.random.uniform(50, 300)
        daily_return = 0.0008
        volatility = 0.025
    elif ticker in ["SPY", "VTI", "QQQ"]:
        base_price = np.random.uniform(200, 500)
        daily_return = 0.0003
        volatility = 0.012
    else:
        base_price = np.random.uniform(50, 200)
        daily_return = 0.0004
        volatility = 0.018
    
    # 生成日期序列
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    dates = pd.date_range(start=start_date, end=end_date, freq='B')[:days]
    
    # 生成价格序列
    n = len(dates)
    returns = np.random.normal(daily_return, volatility, n)
    prices = base_price * np.exp(np.cumsum(returns))
    
    # 创建DataFrame
    data = pd.DataFrame(index=dates[:len(prices)])
    data['Close'] = prices
    data['Open'] = data['Close'].shift(1) * (1 + np.random.normal(0, 0.001, len(data)))
    data['High'] = data[['Open', 'Close']].max(axis=1) * (1 + np.random.uniform(0, 0.02, len(data)))
    data['Low'] = data[['Open', 'Close']].min(axis=1) * (1 - np.random.uniform(0, 0.02, len(data)))
    data['Volume'] = np.random.randint(1000000, 10000000, len(data))
    
    # 填充NaN值
    data = data.ffill().bfill()
    
    return data

# 侧边栏
st.sidebar.header("分析设置")

# 股票选择
ticker = st.sidebar.text_input("股票代码", "AAPL").upper()

# 热门股票快捷按钮
st.sidebar.markdown("### 📈 热门股票")
hot_stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "JPM", "JNJ", "SPY", "QQQ"]
cols = st.sidebar.columns(5)
for idx, stock in enumerate(hot_stocks):
    with cols[idx % 5]:
        if st.button(stock, key=f"hot_{stock}", use_container_width=True):
            st.session_state['ticker'] = stock
            st.experimental_rerun()

# 时间周期
period = st.sidebar.selectbox("时间周期", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)

# 显示数据源说明
st.sidebar.markdown("---")
st.sidebar.info("""
**数据源说明**
- 🟡 使用模拟数据
- 避免API限制问题
- 数据仅用于演示
""")

if st.sidebar.button("开始分析", type="primary", use_container_width=True):
    with st.spinner(f"正在分析 {ticker}..."):
        try:
            # 生成数据
            data = generate_stock_data(ticker, period)
            
            # 显示数据来源标签
            st.markdown(f"""
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <h4 style="margin: 0;">{ticker} - 股票分析</h4>
                <span style="background-color: #F59E0B; color: white; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.8rem; font-weight: bold; margin-left: 0.5rem;">
                    模拟数据
                </span>
            </div>
            """, unsafe_allow_html=True)
            
            # 标签页
            tab1, tab2 = st.tabs(["📈 价格走势", "📊 技术指标"])
            
            with tab1:
                # 价格走势图
                fig1 = go.Figure()
                
                # K线图
                fig1.add_trace(go.Candlestick(
                    x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'],
                    name="OHLC",
                    increasing_line_color='#10B981',
                    decreasing_line_color='#EF4444'
                ))
                
                fig1.update_layout(
                    title=f"{ticker} 价格走势 ({period})",
                    yaxis_title="价格",
                    xaxis_title="日期",
                    height=500,
                    showlegend=True,
                    xaxis_rangeslider_visible=False
                )
                
                st.plotly_chart(fig1, use_container_width=True)
                
                # 价格统计
                st.subheader("价格统计")
                
                col1, col2, col3, col4 = st.columns(4)
                
                price_change = ((data['Close'].iloc[-1] - data['Close'].iloc[0]) / data['Close'].iloc[0] * 100)
                
                with col1:
                    st.metric("当前价格", f"${data['Close'].iloc[-1]:.2f}")
                with col2:
                    st.metric("期间涨跌", f"{price_change:.2f}%")
                with col3:
                    st.metric("最高价", f"${data['High'].max():.2f}")
                with col4:
                    st.metric("最低价", f"${data['Low'].min():.2f}")
            
            with tab2:
                # 技术指标
                st.subheader("技术分析")
                
                # 计算收益率
                returns = data['Close'].pct_change().dropna()
                
                if len(returns) > 0:
                    # 收益率分布
                    fig2 = px.histogram(
                        x=returns * 100,
                        nbins=50,
                        title="日收益率分布",
                        labels={'x': '日收益率 (%)'},
                        color_discrete_sequence=['#3B82F6']
                    )
                    
                    st.plotly_chart(fig2, use_container_width=True)
                    
                    # 技术指标表格
                    st.subheader("技术指标汇总")
                    
                    annual_return = returns.mean() * 252
                    annual_volatility = returns.std() * np.sqrt(252)
                    sharpe_ratio = annual_return / annual_volatility if annual_volatility > 0 else 0
                    
                    tech_metrics = {
                        "平均日收益率": f"{returns.mean()*100:.4f}%",
                        "日收益率标准差": f"{returns.std()*100:.4f}%",
                        "年化收益率": f"{annual_return*100:.2f}%",
                        "年化波动率": f"{annual_volatility*100:.2f}%",
                        "夏普比率": f"{sharpe_ratio:.2f}",
                        "最大单日涨幅": f"{returns.max()*100:.2f}%",
                        "最大单日跌幅": f"{returns.min()*100:.2f}%"
                    }
                    
                    tech_df = pd.DataFrame(list(tech_metrics.items()), columns=['指标', '数值'])
                    st.dataframe(tech_df, use_container_width=True, hide_index=True)
                
        except Exception as e:
            st.error(f"分析失败: {str(e)}")

# 如果未开始分析，显示说明
if not st.sidebar.button:
    st.info("👈 在左侧输入股票代码并点击'开始分析'")
    
    # 功能介绍
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📈 功能特点
        
        - **价格走势分析**: K线图展示
        - **技术指标计算**: 收益率、波动率等
        - **模拟数据**: 避免API限制
        - **快速分析**: 热门股票一键分析
        
        ### 🎯 使用说明
        
        1. 输入股票代码或使用热门股票按钮
        2. 选择时间周期
        3. 点击"开始分析"按钮
        4. 查看分析结果
        """)
    
    with col2:
        st.markdown("""
        ### 📊 支持的股票
        
        **美股大盘股**
        - AAPL (苹果)
        - MSFT (微软)
        - GOOGL (谷歌)
        - AMZN (亚马逊)
        
        **高成长股**
        - TSLA (特斯拉)
        - NVDA (英伟达)
        
        **ETF基金**
        - SPY (标普500)
        - QQQ (纳斯达克100)
        """)
    
    # 数据源说明
    st.markdown("---")
    st.markdown("""
    ### 🔧 关于数据源
    
    为了避免 Yahoo Finance API 的频率限制，本应用使用：
    
    **模拟数据模式**:
    - 为不同类别股票生成合理的价格序列
    - 包含基本的OHLC和成交量数据
    - 可用于演示、测试和学习
    
    **优势**:
    - 无API限制问题
    - 分析速度快
    - 数据稳定可靠
    """)
