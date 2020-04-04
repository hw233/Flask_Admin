/**
 二次确认框
 **/
function comfirmDialog(url, method, jsonStr, text) {
    var comfirmTxt = text || '是否确定此操作';

    layer.open({
        title: [
            '后台系统提醒您',
        ]
        , anim: 'up'
        , content: comfirmTxt
        , btn: ['确认', '取消']
        , fixed: true
        , skin: 'demo-class'
        , style: 'position:fixed;left:0;top:0px;'
        , yes: function (index) {
            formAjax(url, method, jsonStr);
            layer.close(index);
        }
    });
}

/**
 * formAjax
 * @params:
 url :  请求的url地址
 method : 请求方法
 jsonStr : 携带的参数,json格式
 message : 请求等待时的文字信息
 **/
function formAjax(url, method, dataJson) {
    $.ajax({
        type: method,
        url: url,
        data: dataJson,
        dataType: 'JSON',

        success: function (data) {
            layer.closeAll();
            reCode = parseInt(data.code);
            reIcon = data.icon || 5;
            reAnim = data.anim || 6;
            reTime = data.time || 3000;
            reMsg = data.msg;
            reJumpUrl = data.jumpUrl || '';
            switch (reCode) {
                /** 提示 **/
                case -1:
                    layer.msg(reMsg, {icon: reIcon, anim: reAnim, time: reTime}, function () {
                        // do somethings..
                    });
                    break;

                /** 跳转地址 **/
                case 0:
                    layer.load(1, {
                        shade: [0.1, '#fff'],
                        content: reMsg,
                        time: 5000,
                        success: function (layero) {
                            layero.find('.layui-layer-content').css({
                                'padding-top': '39px',
                                'width': '60px'
                            });
                            location.href = reJumpUrl;
                            layer.close(index);
                        }
                    });
                    break;

                /** 跳转提示 **/
                case 1:
                    layer.open({
                        title: [
                            '后台系统提醒您'
                        ]
                        , content: reMsg
                        , btn: '确认'
                        , style: 'position:fixed;left:0;top:0px;'
                        , time: 3000
                        , end: function () {
                            location.href = reJumpUrl;
                            layer.close(index);
                        }
                        , yes: function (index) {
                            location.href = reJumpUrl;
                            layer.close(index);
                        }
                    });
                    break;

                default: //错误信息提示,不刷新页面
                    layer.open({
                        content: data.msg
                        , time: 2 //2秒后自动关闭
                    });
            }
        },
    });
}

/**
 字符串格式化
 **/
String.format = function () {
    if (arguments.length == 0) {
        return null;
    }
    var str = arguments[0];
    for (var i = 1; i < arguments.length; i++) {
        var re = new RegExp('\\{' + (i - 1) + '\\}', 'gm');
        str = str.replace(re, arguments[i]);
    }
    return str;
}


/**
 表格鼠标提示文字
 **/
function tdTitle() {
    $('th').each(function (index, element) {
        $(element).attr('title', $(element).text());
    });
    $('td').each(function (index, element) {
        $(element).attr('title', $(element).text());
    });
}

/**
 子表方法
 **/
function getSub() {
    return '<div style="position: relative;padding: 0 10px 0 20px;">' + '<i style="left: 0px;" lay-tips="展开子表" class="layui-icon layui-colla-icon layui-icon-right"></i></div>'
}

/**
 子表
 **/
function collapseTable(options) {
    var trObj = options.elem;
    if (!trObj) return;
    var accordion = options.accordion,
        success = options.success,
        content = options.content || '';
    var tableView = trObj.parents('.layui-table-view'); //当前表格视图
    var id = tableView.attr('lay-id'); //当前表格标识
    var index = trObj.data('index'); //当前行索引
    var leftTr = tableView.find('.layui-table-fixed.layui-table-fixed-l tr[data-index="' + index + '"]'); //左侧当前固定行
    var rightTr = tableView.find('.layui-table-fixed.layui-table-fixed-r tr[data-index="' + index + '"]'); //右侧当前固定行
    var colspan = trObj.find('td').length; //获取合并长度
    var trObjChildren = trObj.next(); //展开行Dom
    var indexChildren = id + '-' + index + '-children'; //展开行索引
    var leftTrChildren = tableView.find('.layui-table-fixed.layui-table-fixed-l tr[data-index="' + indexChildren + '"]'); //左侧展开固定行
    var rightTrChildren = tableView.find('.layui-table-fixed.layui-table-fixed-r tr[data-index="' + indexChildren + '"]'); //右侧展开固定行
    var lw = leftTr.width() + 15; //左宽
    var rw = rightTr.width() + 15; //右宽
    //不存在就创建展开行
    if (trObjChildren.data('index') != indexChildren) {
        //装载HTML元素
        var tr = '<tr data-index="' + indexChildren + '"><td colspan="' + colspan + '"><div style="height: auto;padding-left:' + lw + 'px;padding-right:' + rw + 'px" class="layui-table-cell">' + content + '</div></td></tr>';
        trObjChildren = trObj.after(tr).next().hide(); //隐藏展开行
        var fixTr = '<tr data-index="' + indexChildren + '"></tr>';//固定行
        leftTrChildren = leftTr.after(fixTr).next().hide(); //左固定
        rightTrChildren = rightTr.after(fixTr).next().hide(); //右固定
    }
    //展开|折叠箭头图标
    trObj.find('td[lay-event="collapse"] i.layui-colla-icon').toggleClass("layui-icon-right layui-icon-down");
    //显示|隐藏展开行
    trObjChildren.toggle();
    //开启手风琴折叠和折叠箭头
    if (accordion) {
        trObj.siblings().find('td[lay-event="collapse"] i.layui-colla-icon').removeClass("layui-icon-down").addClass("layui-icon-right");
        trObjChildren.siblings('[data-index$="-children"]').hide(); //展开
        rightTrChildren.siblings('[data-index$="-children"]').hide(); //左固定
        leftTrChildren.siblings('[data-index$="-children"]').hide(); //右固定
    }
    success(trObjChildren, indexChildren); //回调函数
    heightChildren = trObjChildren.height(); //展开高度固定
    rightTrChildren.height(heightChildren + 115).toggle(); //左固定
    leftTrChildren.height(heightChildren + 115).toggle(); //右固定
}

/**
 **/
function showIframe(title, url) {
    layer.open({
        type: 2,
        title: title,
        shadeClose: true,
        shade: false,
        maxmin: true, //开启最大化最小化按钮
        area: ['80%', '90%'],
        content: url
    });
    ;
}