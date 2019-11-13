$(function () {
    var data = [
        [44,34,29,13,15,16,15,12,12,6,10,8],
        [183,96,70,46,49,29,43,32,34,26,23,30],
        [225,162, 102, 71, 72, 53, 65, 51, 51, 38, 46,22],
        [300, 163, 102, 71, 73, 54, 72, 75, 64, 55, 56,35],
        [594, 254, 139, 109, 100, 207, 101, 104, 108, 82, 78,56],
        [891, 366, 226, 177, 352, 418, 135, 186, 107, 135, 107,92],
        [905, 389, 246, 220, 387, 448, 171, 220, 240, 155, 148,166],
        [450, 400, 279, 256, 424, 486, 210, 264, 225, 212, 195,120],
        [949, 404, 330, 225, 462, 505, 224, 265, 256, 227, 202,123],
        [949, 404, 330, 225, 462, 505, 224, 265, 256, 227, 202,123]

    ];
    timeOption = {
        title : {
            text: '评论时间段增长数量',
            x:'center'
        },
        xAxis: {
            type: 'category',
            data:
                ['0-10', '10-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90', '90-100', '100-110', '110-120']
        },
        yAxis: {
            type: 'value'
        },
        lenged:{
            data:['0-10', '10-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90', '90-100', '100-110', '110-120']
        },
        series: [{
            data: data[0],
            type: 'bar',
            itemStyle:{
                normal:{
                    color: function(params){
                        var colorList = [
                            "#c23531",
                            "#2f4554",
                            "#61a0a8",
                            "#d48265",
                            "#91c7ae",
                            "#749f83",
                            "#ca8622",
                            "#bda29a",
                            "#6e7074",
                            "#546570",
                            "#c4ccd3",
                            "#4BABDE",
                            "#FFDE76",
                            "#E43C59",
                            "#37A2DA",
                            "#E432DA",
                            "#bda074",
                            "#91cf83",
                        ];
                        return colorList[params.dataIndex];
                    }
                }
            }
        }]
    };
    var timeChart = echarts.init(document.getElementById('time'));
    timeChart.setOption(timeOption);
    var i = 1;
    var s = setInterval(function () {
        if (i === data.length) {
            clearInterval(s);
        }else{
            // console.log(data1);
            timeOption.series[0].data = data[i];
            timeChart.setOption(timeOption);
            i++
        }
    },5000)
});