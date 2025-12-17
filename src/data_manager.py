# data_manager.py - 简化的数据管理器
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

class DataManager:
    """简化的数据管理器，避免API限制"""
    
    def __init__(self):
        self.sample_stocks = {
            "AAPL": "Apple Inc.",
            "MSFT": "Microsoft Corporation", 
            "GOOGL": "Alphabet Inc.",
            "AMZN": "Amazon.com Inc.",
            "TSLA": "Tesla Inc.",
            "NVDA": "NVIDIA Corporation",
            "JPM": "JPMorgan Chase & Co.",
            "JNJ": "Johnson & Johnson",
            "WMT": "Walmart Inc.",
            "PG": "Procter & Gamble Co.",
            "SPY": "SPDR S&P 500 ETF",
            "QQQ": "Invesco QQQ Trust",
            "VTI": "Vanguard Total Stock Market ETF"
        }
    
    def generate_mock_data(self, ticker, period="1y"):
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
    
    def get_stock_data(self, ticker, period="1y"):
        """获取股票数据（总是返回模拟数据）"""
        return self.generate_mock_data(ticker, period), "mock"

# 创建全局实例
data_manager = DataManager()
