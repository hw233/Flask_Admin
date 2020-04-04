function eCharts_init(url, id) {
    var myChart = echarts.init(document.getElementById(id));
    var resizeWorldMapContainer = function () {
        document.getElementById(id).style.width = $('.panel-body').attr('width');
        document.getElementById(id).style.height = $('.panel-body').attr('height');

    };
    resizeWorldMapContainer();
    $.getJSON(url, function (data) {
        myChart.setOption({
            tooltip: {
                trigger: 'axis',
            },
            legend: {
                data: data.data.legen
            },
            calculable: true,
            toolbox: {
                show: true,
                feature: {
                    mark: {show: true},
                    dataView: {show: true, readOnly: false},
                    magicType: {show: true, type: ['line', 'bar', 'tiled']},
                    restore: {show: true},
                    saveAsImage: {show: true}
                }
            },
            calculable: true,
            dataZoom: [{
                show: true,
                realtime: true,
                start: 0,
                end: data.data.dataZoom_start
            }, {
                type: 'inside',
                realtime: true,
                start: 0,
                end: 10
            }],
            xAxis: [
                {
                    type: 'category',
                    boundaryGap: false,
                    data: data.data.week,
                    axisLabel: {
                        interval: 0
                    },
                }
            ],
            yAxis: [
                {
                    type: 'value'
                }
            ],
            series: data.data.series
        });
    });

    window.onresize = function () {
        resizeWorldMapContainer();
        myChart.resize();
    };
}
