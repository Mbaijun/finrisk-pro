# config.py - FinRisk Pro 配置文件

# 数据源配置
DATA_SOURCES = {
    'primary': 'yfinance',  # 主要数据源
    'fallback': 'mock',     # 备用数据源
    'cache_enabled': True,  # 启用缓存
    'cache_ttl': 86400,     # 缓存有效期(秒): 24小时
}

# API 配置
API_CONFIG = {
    'yfinance': {
        'max_retries': 3,
        'retry_delay': 2,
        'timeout': 10,
    },
    'alpha_vantage': {
        'api_key': None,  # 如果需要，可以添加 Alpha Vantage API 密钥
        'enabled': False,
    }
}

# 应用配置
APP_CONFIG = {
    'title': 'FinRisk Pro',
    'version': '1.1.0',
    'default_port': 8502,
    'debug': True,
}

# 模拟数据配置
MOCK_DATA_CONFIG = {
    'enabled': True,
    'default_source': True,  # 默认使用模拟数据
    'realistic_mode': True,  # 生成更真实的数据
}

# 可视化配置
CHART_CONFIG = {
    'theme': 'plotly_white',
    'colors': ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6'],
    'default_height': 500,
}

# 风险分析配置
RISK_CONFIG = {
    'default_confidence': 0.95,
    'default_risk_free': 0.02,
    'default_window': 252,
}

# 路径配置
PATH_CONFIG = {
    'data_dir': './data',
    'cache_dir': './data/cache',
    'reports_dir': './reports',
    'logs_dir': './logs',
}
