import streamlit as st
import pandas as pd
import numpy as np


# 设置页面标题
st.title('我的 Streamlit 看板')

# 侧边栏
with st.sidebar:
    st.header('控制面板')
    selected_option = st.selectbox(
        '选择展示内容',
        ['数据概览', '图表分析', '交互控件']
    )

# 主要内容区域
if selected_option == '数据概览':
    st.header('数据概览')
    
    # 创建示例数据
    data = pd.DataFrame({
        '姓名': ['张三', '李四', '王五', '赵六'],
        '年龄': [25, 30, 35, 40],
        '收入': [8000, 12000, 15000, 20000]
    })
    
    st.dataframe(data)

elif selected_option == '图表分析':
    st.header('图表分析')
    
    # 生成随机数据
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['A', 'B', 'C']
    )
    
    st.line_chart(chart_data)
    st.bar_chart(chart_data)

else:
    st.header('交互控件示例')
    
    # 各种交互控件
    name = st.text_input('输入你的名字')
    age = st.slider('选择你的年龄', 0, 100, 25)
    is_happy = st.checkbox('我很开心')
    
    if name:
        st.write(f'你好, {name}!')
    if is_happy:
        st.write('太好了，继续保持！')
    st.write(f'你选择的年龄是: {age}')
