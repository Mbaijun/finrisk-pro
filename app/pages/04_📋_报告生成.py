import streamlit as st
import pandas as pd
import numpy as np
import base64
from datetime import datetime
from io import BytesIO, StringIO

st.set_page_config(page_title="报告生成", page_icon="📋", layout="wide")

st.title("📋 报告生成")
st.markdown("### 生成专业的金融分析报告")

# 侧边栏
st.sidebar.header("报告设置")

# 报告类型
report_type = st.sidebar.selectbox(
    "报告类型",
    ["股票分析报告", "投资组合报告", "风险评估报告", "综合分析报告"]
)

# 公司信息
st.sidebar.subheader("公司信息")
company_name = st.sidebar.text_input("公司名称", "FinRisk Pro Analytics")
analyst_name = st.sidebar.text_input("分析师", "AI Assistant")
report_date = st.sidebar.date_input("报告日期", datetime.now())

# 客户信息（可选）
st.sidebar.subheader("客户信息（可选）")
client_name = st.sidebar.text_input("客户姓名", "")
client_email = st.sidebar.text_input("客户邮箱", "")

# 报告格式选项
st.sidebar.subheader("导出选项")
export_html = st.sidebar.checkbox("HTML格式", True)
export_pdf = st.sidebar.checkbox("PDF格式", False)
export_excel = st.sidebar.checkbox("Excel格式", True)

# 生成模拟数据用于报告
def generate_report_data():
    """生成模拟报告数据"""
    return {
        "portfolio_value": np.random.uniform(100000, 500000),
        "annual_return": np.random.uniform(0.05, 0.25),
        "annual_volatility": np.random.uniform(0.15, 0.35),
        "sharpe_ratio": np.random.uniform(0.5, 1.5),
        "max_drawdown": np.random.uniform(-0.2, -0.05),
        "var_95": np.random.uniform(-0.03, -0.01),
        "top_performers": ["AAPL", "MSFT", "NVDA", "TSLA", "GOOGL"],
        "worst_performers": ["INTC", "PYPL", "META", "NFLX", "AMZN"],
        "recommendations": [
            ("增持", "科技板块", "行业复苏，增长潜力大"),
            ("持有", "消费板块", "防御性强，稳定收益"),
            ("减持", "能源板块", "周期性高点，风险增加")
        ]
    }

if st.sidebar.button("生成报告", type="primary"):
    with st.spinner("正在生成报告..."):
        try:
            # 获取报告数据
            report_data = generate_report_data()
            date_str = report_date.strftime("%Y年%m月%d日")
            
            # 生成报告内容
            html_content = f'''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{report_type} - {company_name}</title>
    <style>
        body {{
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
        }}
        .header {{
            text-align: center;
            border-bottom: 3px solid #1E3A8A;
            padding-bottom: 20px;
            margin-bottom: 30px;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .section {{
            background: white;
            padding: 25px;
            margin: 20px 0;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            border-left: 4px solid #3B82F6;
        }}
        .metric-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin: 10px;
            text-align: center;
        }}
        .table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        .table th, .table td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        .table th {{
            background-color: #1E3A8A;
            color: white;
        }}
        .recommendation-buy {{ color: #10B981; font-weight: bold; }}
        .recommendation-hold {{ color: #F59E0B; font-weight: bold; }}
        .recommendation-sell {{ color: #EF4444; font-weight: bold; }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #666;
            font-size: 0.9em;
        }}
        @media print {{
            body {{ padding: 0; }}
            .no-print {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1 style="color: #1E3A8A; margin-bottom: 10px;">{report_type}</h1>
        <h3 style="color: #4B5563; margin-top: 5px;">{company_name}</h3>
        <p style="color: #6B7280;">
            报告日期: {date_str} | 分析师: {analyst_name} | 
            客户: {client_name if client_name else "不适用"}
        </p>
    </div>

    <div class="section">
        <h2 style="color: #1E3A8A;">📋 执行摘要</h2>
        <p>本报告基于FinRisk Pro平台的风险模型和市场数据分析，提供全面的投资评估和风险洞察。分析覆盖了投资组合表现、风险指标和市场趋势。</p>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0;">
            <div class="metric-card">
                <h3 style="margin: 0;">组合价值</h3>
                <h2 style="margin: 10px 0;">{report_data["portfolio_value"]:,.0f}</h2>
            </div>
            <div class="metric-card">
                <h3 style="margin: 0;">年化收益</h3>
                <h2 style="margin: 10px 0;">{report_data["annual_return"]*100:.1f}%</h2>
            </div>
            <div class="metric-card">
                <h3 style="margin: 0;">夏普比率</h3>
                <h2 style="margin: 10px 0;">{report_data["sharpe_ratio"]:.2f}</h2>
            </div>
            <div class="metric-card">
                <h3 style="margin: 0;">最大回撤</h3>
                <h2 style="margin: 10px 0;">{report_data["max_drawdown"]*100:.1f}%</h2>
            </div>
        </div>
    </div>

    <div class="section">
        <h2 style="color: #1E3A8A;">📊 投资组合表现</h2>
        
        <h3>绩效指标</h3>
        <table class="table">
            <thead>
                <tr>
                    <th>指标</th>
                    <th>数值</th>
                    <th>评级</th>
                    <th>市场分位</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>年化收益率</td>
                    <td>{report_data["annual_return"]*100:.2f}%</td>
                    <td></td>
                    <td>前 25%</td>
                </tr>
                <tr>
                    <td>年化波动率</td>
                    <td>{report_data["annual_volatility"]*100:.2f}%</td>
                    <td></td>
                    <td>前 40%</td>
                </tr>
                <tr>
                    <td>夏普比率</td>
                    <td>{report_data["sharpe_ratio"]:.2f}</td>
                    <td></td>
                    <td>前 20%</td>
                </tr>
                <tr>
                    <td>VaR (95%)</td>
                    <td>{report_data["var_95"]*100:.2f}%</td>
                    <td></td>
                    <td>前 35%</td>
                </tr>
                <tr>
                    <td>最大回撤</td>
                    <td>{report_data["max_drawdown"]*100:.2f}%</td>
                    <td></td>
                    <td>前 15%</td>
                </tr>
            </tbody>
        </table>
    </div>

    <div class="section">
        <h2 style="color: #1E3A8A;">📈 个股表现</h2>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px;">
            <div>
                <h3>👍 最佳表现股票</h3>
                <ul>
                    {''.join(f'<li><strong>{stock}</strong>: +{np.random.uniform(10, 50):.1f}%</li>' for stock in report_data["top_performers"][:3])}
                </ul>
            </div>
            <div>
                <h3>👎 最差表现股票</h3>
                <ul>
                    {''.join(f'<li><strong>{stock}</strong>: -{np.random.uniform(5, 25):.1f}%</li>' for stock in report_data["worst_performers"][:3])}
                </ul>
            </div>
        </div>
    </div>

    <div class="section">
        <h2 style="color: #1E3A8A;">🎯 投资建议</h2>
        
        <table class="table">
            <thead>
                <tr>
                    <th>建议</th>
                    <th>板块/资产</th>
                    <th>理由</th>
                </tr>
            </thead>
            <tbody>
                {''.join(f'''
                <tr>
                    <td><span class="recommendation-{action}">{action}</span></td>
                    <td>{sector}</td>
                    <td>{reason}</td>
                </tr>
                ''' for action, sector, reason in report_data["recommendations"])}
            </tbody>
        </table>
        
        <h3>风险提示</h3>
        <ul>
            <li>市场波动可能加大，建议控制仓位</li>
            <li>关注美联储货币政策变化对市场的影响</li>
            <li>地缘政治风险可能对全球市场产生冲击</li>
            <li>建议定期评估投资组合风险暴露</li>
        </ul>
    </div>

    <div class="section">
        <h2 style="color: #1E3A8A;">📋 后续行动计划</h2>
        <ol>
            <li><strong>立即行动</strong>: 调整投资组合，增加防御性资产配置</li>
            <li><strong>一周内</strong>: 审查持仓，止损设定在-8%</li>
            <li><strong>一月内</strong>: 重新评估市场环境，调整投资策略</li>
            <li><strong>一季度</strong>: 全面回顾投资组合表现，优化资产配置</li>
        </ol>
    </div>

    <div class="footer">
        <p><strong>免责声明</strong>: 本报告仅供参考，不构成投资建议。投资有风险，决策需谨慎。过往表现不代表未来收益。</p>
        <p>{company_name} | {date_str} | 报告编号: FR-{datetime.now().strftime("%Y%m%d%H%M%S")}</p>
        <p class="no-print">如需进一步咨询，请联系: {analyst_name} | 报告生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    </div>

    <script>
        // 打印功能
        function printReport() {{
            window.print();
        }}
        
        // 页面加载完成后添加打印按钮
        window.onload = function() {{
            var printBtn = document.createElement('button');
            printBtn.innerHTML = '🖨️ 打印报告';
            printBtn.style.cssText = 'position: fixed; bottom: 20px; right: 20px; padding: 10px 20px; background: #3B82F6; color: white; border: none; border-radius: 5px; cursor: pointer; z-index: 1000;';
            printBtn.onclick = printReport;
            document.body.appendChild(printBtn);
        }};
    </script>
</body>
</html>
            '''
            
            # 成功消息
            st.success("✅ 报告生成完成！")
            
            # 显示报告预览
            st.markdown("---")
            st.subheader("📄 报告预览")
            
            # 在Streamlit中显示HTML内容（只显示部分）
            st.markdown("""
            <div style="border: 1px solid #ddd; padding: 20px; border-radius: 10px; background: white; max-height: 400px; overflow-y: auto;">
                <h3 style="color: #1E3A8A;">报告预览</h3>
                <p><strong>报告类型:</strong> {}</p>
                <p><strong>公司名称:</strong> {}</p>
                <p><strong>分析师:</strong> {}</p>
                <p><strong>报告日期:</strong> {}</p>
                <p><strong>客户姓名:</strong> {}</p>
                <hr>
                <p>本报告包含完整的投资分析、风险指标和投资建议。</p>
                <p>点击下方按钮下载完整报告。</p>
            </div>
            """.format(report_type, company_name, analyst_name, date_str, client_name if client_name else "未指定"), 
            unsafe_allow_html=True)
            
            # 导出选项
            st.markdown("---")
            st.subheader("📤 导出选项")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # HTML下载
                if export_html:
                    # 将HTML内容转换为字节
                    html_bytes = html_content.encode('utf-8')
                    b64 = base64.b64encode(html_bytes).decode()
                    
                    # 创建下载链接
                    href = f'<a href="data:text/html;base64,{b64}" download="{report_type}_{date_str}.html" style="text-decoration: none;">'
                    href += '<button style="background-color: #3B82F6; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; width: 100%;">'
                    href += '📥 下载HTML报告</button></a>'
                    
                    st.markdown(href, unsafe_allow_html=True)
                    
                    # 额外的HTML下载按钮（使用st.download_button）
                    st.download_button(
                        label="📥 下载HTML (备用)",
                        data=html_bytes,
                        file_name=f"{report_type}_{date_str}.html",
                        mime="text/html",
                        help="下载完整的HTML报告"
                    )
            
            with col2:
                # Excel数据下载（模拟数据）
                if export_excel:
                    # 创建Excel数据
                    excel_data = pd.DataFrame({
                        '指标': ['组合价值', '年化收益', '年化波动', '夏普比率', '最大回撤', 'VaR(95%)'],
                        '数值': [
                            f'{report_data["portfolio_value"]:,.0f}',
                            f'{report_data["annual_return"]*100:.2f}%',
                            f'{report_data["annual_volatility"]*100:.2f}%',
                            f'{report_data["sharpe_ratio"]:.2f}',
                            f'{report_data["max_drawdown"]*100:.2f}%',
                            f'{report_data["var_95"]*100:.2f}%'
                        ],
                        '评级': ['', '', '', '', '', '']
                    })
                    
                    # 转换为Excel
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        excel_data.to_excel(writer, sheet_name='投资组合指标', index=False)
                        
                        # 添加第二个工作表 - 投资建议
                        recommendations_df = pd.DataFrame(report_data["recommendations"], 
                                                         columns=['建议', '板块', '理由'])
                        recommendations_df.to_excel(writer, sheet_name='投资建议', index=False)
                        
                        # 添加第三个工作表 - 股票表现
                        stocks_df = pd.DataFrame({
                            '股票': report_data["top_performers"] + report_data["worst_performers"],
                            '表现': [f'+{np.random.uniform(10, 50):.1f}%' for _ in range(5)] + 
                                   [f'-{np.random.uniform(5, 25):.1f}%' for _ in range(5)],
                            '评级': ['买入', '买入', '增持', '持有', '持有', '减持', '减持', '观望', '卖出', '卖出']
                        })
                        stocks_df.to_excel(writer, sheet_name='股票表现', index=False)
                    
                    excel_bytes = output.getvalue()
                    
                    st.download_button(
                        label="📊 下载Excel数据",
                        data=excel_bytes,
                        file_name=f"{report_type}_数据_{date_str}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        help="下载Excel格式的数据报告"
                    )
            
            with col3:
                # 打印功能说明
                st.markdown("""
                <div style="text-align: center; padding: 15px; background: #F0F9FF; border-radius: 10px;">
                    <h4 style="color: #1E3A8A;">🖨️ 打印指南</h4>
                    <p style="color: #4B5563; font-size: 0.9em;">
                    1. 先下载HTML报告<br>
                    2. 用浏览器打开<br>
                    3. 按 <kbd>Ctrl</kbd>+<kbd>P</kbd> 打印<br>
                    4. 或使用浏览器打印功能
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # 简单的文本报告下载
                text_report = f"""{report_type}
生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
公司: {company_name}
分析师: {analyst_name}
客户: {client_name if client_name else "未指定"}

执行摘要:
- 组合价值: {report_data["portfolio_value"]:,.0f}
- 年化收益: {report_data["annual_return"]*100:.2f}%
- 夏普比率: {report_data["sharpe_ratio"]:.2f}
- 最大回撤: {report_data["max_drawdown"]*100:.2f}%

投资建议:
"""
                for action, sector, reason in report_data["recommendations"]:
                    text_report += f"- {action}: {sector} - {reason}\n"
                
                text_report += "\n风险提示: 市场有风险，投资需谨慎。"
                
                st.download_button(
                    label="📝 下载文本报告",
                    data=text_report,
                    file_name=f"{report_type}_摘要_{date_str}.txt",
                    mime="text/plain",
                    help="下载文本格式的报告摘要"
                )
            
            # 报告模板保存选项
            st.markdown("---")
            st.subheader("💾 保存报告模板")
            
            if st.button("保存当前模板", key="save_template"):
                # 这里可以添加模板保存逻辑（实际应用中可能需要数据库）
                st.success("模板已保存！可以在下次生成报告时使用。")
            
            # 报告历史
            with st.expander("📚 报告历史记录"):
                # 模拟历史报告
                history_data = pd.DataFrame({
                    '日期': ['2024-01-15', '2024-02-01', '2024-03-10'],
                    '报告类型': ['股票分析报告', '投资组合报告', '风险评估报告'],
                    '客户': ['张三', '李四', '王五'],
                    '状态': ['已完成', '已完成', '进行中']
                })
                
                st.dataframe(history_data, use_container_width=True)
                
                if st.button("查看完整历史", key="view_history"):
                    st.info("完整报告历史功能需要数据库支持，后续版本将添加。")
        
        except Exception as e:
            st.error(f"报告生成失败: {str(e)}")
            st.info("如果遇到问题，请尝试简化报告内容或联系技术支持。")

# 如果未开始生成，显示说明
if not st.sidebar.button:
    st.info("👈 在左侧配置报告参数，然后点击'生成报告'")
    
    # 功能介绍
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📋 报告内容
        
        **包含以下部分:**
        
        1. **执行摘要**
           - 关键指标概览
           - 投资组合表现
           - 主要发现
        
        2. **详细分析**
           - 投资组合指标
           - 个股表现
           - 风险分析
        
        3. **投资建议**
           - 具体操作建议
           - 风险提示
           - 后续计划
        """)
    
    with col2:
        st.markdown("""
        ### 🚀 导出功能
        
        **支持多种格式:**
        
        - **HTML报告**: 完整的网页格式报告
        - **Excel数据**: 结构化数据表格
        - **文本摘要**: 简洁的文本格式
        
        **打印功能:**
        
        1. 下载HTML报告
        2. 用浏览器打开
        3. 使用浏览器打印功能
        4. 或按 Ctrl+P 打印
        """)
    
    # 报告模板示例
    st.markdown("---")
    st.subheader("📝 报告模板示例")
    
    templates = [
        {"name": "简易报告", "desc": "适合快速分析，包含核心指标和简要建议", "features": ["核心指标", "简要建议", "一页总结"]},
        {"name": "详细报告", "desc": "包含全面分析、图表、数据表格和详细建议", "features": ["全面分析", "数据表格", "详细建议"]},
        {"name": "专业报告", "desc": "符合行业标准，包含压力测试、情景分析", "features": ["压力测试", "情景分析", "专业格式"]},
        {"name": "客户报告", "desc": "面向客户的易懂格式，包含可视化图表", "features": ["客户友好", "可视化", "易懂语言"]}
    ]
    
    for template in templates:
        with st.expander(f"✨ {template['name']} - {template['desc']}"):
            cols = st.columns([2, 1])
            with cols[0]:
                st.write("**包含功能:**")
                for feature in template['features']:
                    st.write(f"- {feature}")
            with cols[1]:
                if st.button(f"使用{template['name']}", key=f"use_{template['name']}"):
                    st.success(f"已选择{template['name']}模板，请在左侧配置其他参数。")
    
    # 页脚
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9em;">
        <p>FinRisk Pro 报告生成系统 | 版本 1.1.0</p>
        <p>💡 提示: 所有报告均为模拟数据，仅用于演示目的</p>
    </div>
    """, unsafe_allow_html=True)
