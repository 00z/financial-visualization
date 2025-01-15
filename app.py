import streamlit as st
import baostock as bs
import pandas as pd
from datetime import datetime, timedelta
import altair as alt

# 初始化baostock
def init_baostock():
    bs.login()

# 获取沪深300股息率数据
def get_dividend_data():
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    
    try:
        # 获取沪深300成分股
        rs = bs.query_hs300_stocks()
        if rs.error_code != '0':
            st.error(f"获取沪深300成分股失败: {rs.error_msg}")
            return pd.DataFrame()
        
        # 手动解析数据
        raw_data = rs.get_data()
        if not raw_data:
            return pd.DataFrame()
            
        # 解析成分股数据
        hs300_stocks = []
        for line in raw_data.split('\n'):
            if not line:
                continue
            try:
                stock_data = line.split(',')
                if len(stock_data) > 1:
                    hs300_stocks.append(stock_data)
            except Exception as e:
                print(f"跳过无效成分股数据: {line}, 错误: {e}")
                continue
        
        dividend_data = []
        for stock in hs300_stocks:
            code = stock[1]
            try:
                # 获取个股股息率数据
                rs = bs.query_dividend_data(
                    code=code,
                    year=start_date[:4],
                    yearType="report"
                )
                if rs.error_code != '0':
                    continue
                    
                # 手动解析股息率数据
                raw_dividend = rs.get_data()
                if not raw_dividend:
                    continue
                    
                for line in raw_dividend.split('\n'):
                    if not line:
                        continue
                    try:
                        data = line.split(',')
                        if len(data) < 4:
                            continue
                            
                        # 解析股息率
                        dividend_rate = float(data[3])
                        dividend_data.append({
                            'date': data[1],
                            'value': dividend_rate
                        })
                    except (ValueError, TypeError) as e:
                        print(f"跳过无效股息率数据: {data[3] if len(data) > 3 else '无数据'}, 错误: {e}")
                        continue
                        
            except Exception as e:
                print(f"获取股票 {code} 数据失败: {str(e)}")
                continue
                
    except Exception as e:
        st.error(f"数据获取失败: {str(e)}")
        return pd.DataFrame()
    
    # 检查是否有有效数据
    if not dividend_data:
        st.warning("未获取到有效股息率数据")
        return pd.DataFrame(columns=['date', 'value'])
        
    # 按日期排序并计算平均值
    df = pd.DataFrame(dividend_data)
    if df.empty:
        st.warning("数据转换失败")
        return pd.DataFrame(columns=['date', 'value'])
        
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date').resample('M').mean().reset_index()
    
    # 检查最终数据是否为空
    if df.empty:
        st.warning("处理后的数据为空")
        return pd.DataFrame(columns=['date', 'value'])
        
    return df

# 页面配置
st.set_page_config(
    page_title="沪深300股息率可视化",
    layout="wide"
)

# 初始化数据获取
init_baostock()
df = get_dividend_data()

# 页面标题
st.title("沪深300指数股息率")

# 使用Altair创建交互式图表
chart = alt.Chart(df).mark_line(
    point=True,
    color='#5470C6'
).encode(
    x=alt.X('date:T', title='日期', axis=alt.Axis(format='%Y-%m')),
    y=alt.Y('value:Q', title='股息率 (%)'),
    tooltip=['date:T', 'value:Q']
).properties(
    width=1200,
    height=600
)

# 显示图表
st.altair_chart(chart, use_container_width=True)

# 显示原始数据
if st.checkbox('显示原始数据'):
    st.write(df)
