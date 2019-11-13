$(function () {

    var length = data.length;
    console.log(length);
    for(var i=0;i<length;i++){
        if(data[i].value<1000&&data[i]>500){
            data[i].value = data[i].value*4
        }else if(data[i]<500){
            data[i].value = data[i].value*5
        }
    }

    var myChart = echarts.init(document.getElementById('main'));
    //温馨提示：image 选取有严格要求不可过大；，否则firefox不兼容 iconfont上面的图标可以
    var maskImage = new Image();
    maskImage.src = img;

    maskImage.onload = function(){
        myChart.setOption( {
            backgroundColor:'#fff',
            tooltip: {
                show: false
            },
            series: [{
                type: 'wordCloud',
                gridSize: 1,
                sizeRange: [15, 40],
                rotationRange: [0,90],
                maskImage: maskImage,
                textStyle: {
                    normal: {
                        color: function() {
                            return 'rgb(' +
                                Math.round(Math.random() * 255) +
                                ', ' + Math.round(Math.random() * 255) +
                                ', ' + Math.round(Math.random() * 255) + ')'
                        }
                    }
                },
                left: 'center',
                top: 'center',
                // width: '96%',
                // height: '100%',
                right: null,
                bottom: null,
                // width: 300,
                // height: 200,
                // top: 20,
                data: data
            }]
        })
    }

});