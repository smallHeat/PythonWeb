function haha() {
    alert("哈哈");
}

/**
 * 展开图标变换
 * */
function toggleExpend() {
    var className = jQuery("#expend_operator").attr("class");
    if(className.indexOf("plus") != -1){
        jQuery("#expend_operator").attr("class","glyphicon glyphicon-minus");
    }else{
        jQuery("#expend_operator").attr("class","glyphicon glyphicon-plus");
    }
}