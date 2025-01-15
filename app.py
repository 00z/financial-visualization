import streamlit as st
from streamlit.components.v1 import html

# 页面配置
st.set_page_config(
    page_title="沪深300股息率可视化",
    layout="wide"
)

# 嵌入HTML内容
html_code = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.2/dist/echarts.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
            color: #333;
        }
        .container {
            max-width: 1200px;
            margin: 40px auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            text-align: center;
            color: #2c3e50;
            margin-bottom: 40px;
            font-size: 2.2rem;
        }
        @media (max-width: 768px) {
            .container {
                margin: 20px;
                padding: 15px;
            }
            h1 {
                font-size: 1.8rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>沪深300指数股息率</h1>
        <div id="chart" style="width: 100%;height:600px;"></div>
    </div>
    <script>
        // 初始化ECharts实例
        const chartDom = document.getElementById('chart');
        const myChart = echarts.init(chartDom);

        // 模拟数据
        const dividendData = [
            { date: '2023-01', value: 2.85 },
            { date: '2023-02', value: 2.78 },
            { date: '2023-03', value: 2.92 },
            { date: '2023-04', value: 2.88 },
            { date: '2023-05', value: 2.95 },
            { date: '2023-06', value: 3.02 },
            { date: '2023-07', value: 3.10 },
            { date: '2023-08', value: 3.05 },
            { date: '2023-09', value: 3.12 },
            { date: '2023-10', value: 3.08 }
        ];

        // 配置图表选项
        const option = {
            title: {
                text: '近一年沪深300股息率走势',
                left: 'center',
                textStyle: {
                    fontSize: 18,
                    fontWeight: 'bold'
                }
            },
            tooltip: {
                trigger: 'axis',
                formatter: function(params) {
                    return `日期：${params[0].name}<br>股息率：${params[0].value}%`;
                }
            },
            xAxis: {
                type: 'category',
                data: dividendData.map(item => item.date),
                axisLabel: {
                    rotate: 45
                }
            },
            yAxis: {
                type: 'value',
                axisLabel: {
                    formatter: '{value} %'
                }
            },
            series: [{
                name: '股息率',
                type: 'line',
                data: dividendData.map(item => item.value),
                smooth: true,
                lineStyle: {
                    width: 3
                },
                itemStyle: {
                    color: '#5470C6'
                },
                areaStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        {
                            offset: 0,
                            color: 'rgba(84, 112, 198, 0.7)'
                        },
                        {
                            offset: 1,
                            color: 'rgba(84, 112, 198, 0.1)'
                        }
                    ])
                }
            }]
        };

        // 应用配置
        myChart.setOption(option);

        // 窗口大小改变时自适应
        window.addEventListener('resize', function() {
            myChart.resize();
        });
    </script>
</body>
</html>
"""

# 显示HTML内容
html(html_code, height=700)
