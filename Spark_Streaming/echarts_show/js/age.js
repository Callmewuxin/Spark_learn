$(function () {
    var ageChart = echarts.init(document.getElementById('age'));
    ageOption = {
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
            data: ['80后','85后','90后','95后','00后']
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
                    {value:40, name:'80后'},
                    {value:123, name:'85后'},
                    {value:794, name:'90后'},
                    {value:4817, name:'95后'},
                    {value:2279, name:'00后'}
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
    ageChart.setOption(ageOption)
})