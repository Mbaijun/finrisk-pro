import streamlit as st
import pandas as pd
import base64
from io import BytesIO

st.set_page_config(page_title="下载测试", page_icon="📥", layout="centered")

st.title("📥 下载功能测试")
st.markdown("测试各种文件下载功能")

# 测试 1: 文本文件下载
st.subheader("1. 文本文件下载")

sample_text = """这是一个测试文本文件。
包含多行内容：
- 第一行
- 第二行
- 第三行

测试时间：测试下载功能。
"""

st.download_button(
    label="下载文本文件 (.txt)",
    data=sample_text,
    file_name="测试文件.txt",
    mime="text/plain"
)

# 测试 2: CSV 文件下载
st.subheader("2. CSV 文件下载")

df = pd.DataFrame({
    '姓名': ['张三', '李四', '王五'],
    '年龄': [25, 30, 35],
    '城市': ['北京', '上海', '广州']
})

csv = df.to_csv(index=False)
st.download_button(
    label="下载CSV文件 (.csv)",
    data=csv,
    file_name="测试数据.csv",
    mime="text/csv"
)

# 测试 3: Excel 文件下载
st.subheader("3. Excel 文件下载")

# 需要 openpyxl 库
try:
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
    
    excel_data = output.getvalue()
    
    st.download_button(
        label="下载Excel文件 (.xlsx)",
        data=excel_data,
        file_name="测试数据.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
except Exception as e:
    st.error(f"Excel下载失败: {e}")
    st.info("请安装 openpyxl: pip install openpyxl")

# 测试 4: HTML 文件下载
st.subheader("4. HTML 文件下载")

html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>测试HTML文件</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        h1 { color: blue; }
        .content { background: #f0f0f0; padding: 15px; }
    </style>
</head>
<body>
    <h1>测试HTML文件</h1>
    <div class="content">
        <p>这是一个测试HTML文件。</p>
        <p>可以在浏览器中打开查看。</p>
    </div>
</body>
</html>
"""

st.download_button(
    label="下载HTML文件 (.html)",
    data=html_content,
    file_name="测试页面.html",
    mime="text/html"
)

# 测试 5: 使用 base64 编码的下载链接
st.subheader("5. 使用链接下载")

# 创建 base64 编码的数据
data_to_encode = "这是通过链接下载的测试内容。"
b64 = base64.b64encode(data_to_encode.encode()).decode()

# 创建下载链接
href = f'<a href="data:text/plain;base64,{b64}" download="链接下载.txt">'
href += '<button style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">'
href += '通过链接下载</button></a>'

st.markdown(href, unsafe_allow_html=True)

# 使用说明
st.markdown("---")
st.markdown("""
### 🔧 故障排除

如果下载功能不正常：

1. **检查浏览器设置**
   - 确保浏览器允许下载
   - 检查下载文件夹权限

2. **检查文件大小**
   - 过大的文件可能导致问题
   - 建议文件大小 < 10MB

3. **尝试不同浏览器**
   - Chrome, Firefox, Edge

4. **检查防火墙/安全软件**
   - 临时禁用安全软件测试

### 📱 支持的浏览器

- ✅ Google Chrome
- ✅ Mozilla Firefox
- ✅ Microsoft Edge
- ✅ Safari (macOS)
""")

st.success("✅ 如果上述测试都能正常工作，说明下载功能正常！")
