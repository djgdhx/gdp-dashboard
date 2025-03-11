import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 读取CSV文件
DATA_FILENAME = Path(__file__).parent/'data/supermarket_sales - Sheet1.csv'
df = pd.read_csv(DATA_FILENAME)


# 转换日期列为datetime类型
df['Date'] = pd.to_datetime(df['Date'])

# 创建图表
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Daily Sales Trend - Sales Amount Over Time',
                   'Product Category Distribution - Sales Proportion by Category',
                   'Payment Method Distribution - Customer Payment Preferences',
                   'Customer Type and Gender Distribution - Customer Demographics'),
    specs=[[{'type': 'scatter'}, {'type': 'pie'}],
           [{'type': 'pie'}, {'type': 'bar'}]],
    vertical_spacing=0.2,
    horizontal_spacing=0.15
)

# 1. 每日销售额趋势
daily_sales = df.groupby('Date')['Total'].sum().reset_index()
fig.add_trace(
    go.Scatter(
        x=daily_sales['Date'],
        y=daily_sales['Total'],
        mode='lines+markers',
        name='Daily Sales',
        line=dict(color='#1f77b4', width=2),
        hovertemplate='Date: %{x}<br>Sales: $%{y:.2f}<extra></extra>'
    ),
    row=1, col=1
)

# 2. 产品类别销售分布
product_sales = df.groupby('Product line')['Total'].sum()
fig.add_trace(
    go.Pie(
        labels=product_sales.index,
        values=product_sales.values,
        textinfo='label+percent',
        hovertemplate='Category: %{label}<br>Sales: $%{value:.2f}<br>Proportion: %{percent}<extra></extra>',
        marker=dict(colors=px.colors.qualitative.Set3)
    ),
    row=1, col=2
)

# 3. 支付方式分布
payment_counts = df['Payment'].value_counts()
fig.add_trace(
    go.Pie(
        labels=payment_counts.index,
        values=payment_counts.values,
        textinfo='label+percent',
        hovertemplate='Payment Method: %{label}<br>Count: %{value}<br>Proportion: %{percent}<extra></extra>',
        marker=dict(colors=px.colors.qualitative.Pastel)
    ),
    row=2, col=1
)

# 4. 客户类型与性别分布
customer_gender = df.groupby(['Customer type', 'Gender']).size().reset_index(name='count')
fig.add_trace(
    go.Bar(
        x=customer_gender['Customer type'],
        y=customer_gender['count'],
        text=customer_gender['count'],
        textposition='auto',
        name='Customer Distribution',
        marker=dict(
            color=customer_gender['Gender'].map({'Male': '#1f77b4', 'Female': '#ff7f0e'}),
            pattern=dict(shape=['/', '\\'])
        ),
        hovertemplate='Customer Type: %{x}<br>Count: %{y}<extra></extra>'
    ),
    row=2, col=2
)

# 更新布局
fig.update_layout(
    height=900,
    width=1300,
    title_text='Supermarket Sales Analysis Dashboard',
    title_x=0.5,
    title_font=dict(size=24, family='Microsoft YaHei'),
    font=dict(family='Microsoft YaHei'),
    showlegend=True,
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=1
    ),
    template='plotly_white',
    margin=dict(t=100, b=50, l=50, r=50)
)

# 更新子图布局
fig.update_xaxes(title_text='Date', row=1, col=1)
fig.update_yaxes(title_text='Sales ($)', row=1, col=1)
fig.update_xaxes(title_text='Customer Type', row=2, col=2)
fig.update_yaxes(title_text='Count', row=2, col=2)

# 保存为HTML文件以实现交互
fig.write_html('sales_dashboard.html')
