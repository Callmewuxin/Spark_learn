$(function () {
    emojiOption = {
        title : {
            text: '评论表情',
            x:'center'
        },
        xAxis: {
            type: 'category',
            data:
                ['🐴', '👴', '🐶', '🐎', '🍺', '👍', '🌶', '🐛', '🔨', '🐔', '👶', '🔥', '🐮', '🍔', '🐲', '🐢', '💊', '💧']
        },
        yAxis: {
            type: 'value'
        },
        lenged:{
            data:['🐴', '👴', '🐶', '🐎', '🍺', '👍', '🌶', '🐛', '🔨', '🐔', '👶', '🔥', '🐮', '🍔', '🐲', '🐢', '💊', '💧']
        },
        series: [{
            data: [15352 ,8393, 7784, 5639, 5359, 2484, 1777,1578,1563,1387,1316,1226,1099,949,934,679,514,540],
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
    var emojiChart = echarts.init(document.getElementById('emoji'));
    emojiChart.setOption(emojiOption)
})