// 初始化ECharts实例
const chartDom = document.getElementById('chart');
const myChart = echarts.init(chartDom);

// 模拟数据（后续可替换为真实API数据）
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
