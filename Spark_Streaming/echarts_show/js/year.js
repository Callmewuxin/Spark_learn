$(function () {
    var yearChart = echarts.init(document.getElementById('year'));
    yearOption = {
        backgroundColor: '#fff',

        title : {
            // text: '粉丝年龄比例',
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
            data: ['1994','1995','1996','1997','1998','1999','2000','2001']
        },

        // visualMap: {
        //     show: false,
        //     min: 80,
        //     max: 600,
        //     inRange: {
        //         colorLightness: [0, 1]
        //     }
        // },
        series : [
            {
                type:'pie',
                radius : '55%',
                center: ['50%', '60%'],
                data:[
                    {value:316, name:'1994'},
                    {value:535, name:'1995'},
                    {value:753, name:'1996'},
                    {value:988, name:'1997'},
                    {value:1240, name:'1998'},
                    {value:1301, name:'1999'},
                    {value:1184, name:'2000'},
                    {value:534, name:'2001'}
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
    yearChart.setOption(yearOption)
})