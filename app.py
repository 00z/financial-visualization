import streamlit as st
import baostock as bs
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import altair as alt

# 配置常量
DEFAULT_COLOR = '#5470C6'
CHART_WIDTH = 1200
CHART_HEIGHT = 600
DATE_FORMAT = '%Y-%m-%d'
RESAMPLE_FREQ = 'M'

# 初始化baostock
def init_baostock():
    """初始化baostock连接"""
    login_result = bs.login()
    if login_result.error_code != '0':
        st.error(f"Baostock登录失败: {login_result.error_msg}")
        return False
    return True

# 获取沪深300股息率数据
def get_dividend_data():
    """获取沪深300成分股的股息率数据"""
    end_date = datetime.now().strftime(DATE_FORMAT)
    start_date = (datetime.now() - timedelta(days=365)).strftime(DATE_FORMAT)
    
    try:
        # 获取沪深300成分股
        rs = bs.query_hs300_stocks()
        if rs.error_code != '0':
            st.error(f"获取沪深300成分股失败: {rs.error_msg}")
            return pd.DataFrame(columns=['date', 'value'])
            
        # 使用pandas直接解析数据
        df_stocks = rs.get_data()
        if df_stocks.empty:
            st.warning("未获取到成分股数据")
            return pd.DataFrame(columns=['date', 'value'])
            
        # 提取股票代码
        hs300_stocks = df_stocks['code'].tolist()
        if not hs300_stocks:
            st.warning("未找到有效的成分股代码")
            return pd.DataFrame(columns=['date', 'value'])
    except Exception as e:
        st.error(f"解析成分股数据时发生错误: {str(e)}")
        return pd.DataFrame(columns=['date', 'value'])
        
    try:
        # 获取所有成分股的股息率数据
        all_dividends = []
        
        for code in hs300_stocks:
            try:
                rs = bs.query_dividend_data(
                    code=code,
                    year=start_date[:4],
                    yearType="report"
                )
                if rs.error_code != '0':
                    continue
                    
                # 使用pandas直接解析数据
                df_dividend = rs.get_data()
                if df_dividend.empty:
                    continue
                    
                # 筛选有效股息率数据
                df_dividend = df_dividend[df_dividend['dividend_rate'] > 0]
                if not df_dividend.empty:
                    all_dividends.append(df_dividend[['dividend_date', 'dividend_rate']])
                    
            except Exception as e:
                print(f"获取股票 {code} 数据失败: {str(e)}")
                continue
                
        if not all_dividends:
            st.warning("未找到有效的股息率数据")
            return pd.DataFrame(columns=['date', 'value'])
            
        # 合并所有数据
        df = pd.concat(all_dividends)
        df = df.rename(columns={
            'dividend_date': 'date',
            'dividend_rate': 'value'
        })
    except Exception as e:
        st.error(f"处理股息率数据时发生错误: {str(e)}")
        return pd.DataFrame(columns=['date', 'value'])
                
    except Exception as e:
        st.error(f"数据获取失败: {str(e)}")
        return pd.DataFrame()
    
    # 检查是否有有效数据
    if df.empty:
        st.warning("未获取到有效股息率数据")
        return pd.DataFrame(columns=['date', 'value'])
        
    # 转换日期格式并处理数据
    try:
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date').resample('M').mean().reset_index()
    except Exception as e:
        st.error(f"数据处理失败: {str(e)}")
        return pd.DataFrame(columns=['date', 'value'])
    
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
