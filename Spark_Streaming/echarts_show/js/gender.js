$(function () {
    var genderChart = echarts.init(document.getElementById('gender'));
    genderOption = {
        title : {
            text: '粉丝性别比例',
            top: 40,
            x:'center'
        },
        tooltip : {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
            orient: 'vertical',
            left: 'right',
            top: 40,
            data: ['男','女']
        },
        series : [
            {
                name: '性别比例',
                type: 'pie',
                radius : '55%',
                center: ['50%', '60%'],
                data:[
                    {value:15737, name:'男'},
                    {value:2946, name:'女'},
                ],
                itemStyle: {
                    emphasis: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    };
    genderChart.setOption(genderOption)
})