
/**
 * 对话框提示
 * */
function modalTip(hideMoal,showModal,contentKey,color,html) {
    //先关掉原来的modal对话框
    jQuery(hideMoal).modal('hide');
    //显示提示对话框
    jQuery(showModal).modal('show');
    //修改字体颜色
    jQuery(showModal + "Label").css("color",color);
    jQuery(contentKey).css("color",color);
    //修改提示内容
    jQuery(contentKey).html(html);
}

/**
 * 注册用户
 * */
function registUser() {

    //点击开始就应该置灰
    jQuery("#regist_btn").attr("disabled",true);

    var username_regist = jQuery("#username_regist").val();
    var password_regist = jQuery("#password_regist").val();
    var password2_regist = jQuery("#password2_regist").val();
    var super_password_regist = jQuery("#super_password_regist").val();

    //所有表单都填了才能提交
    if(username_regist != "" && password_regist != "" && password2_regist != ""
        && super_password_regist != ""){
        //只有2次密码输入一致并且超级密码和密码不一致才能提交
        if(password_regist == password2_regist && super_password_regist != password_regist){
            var params = jQuery("#regist_form").serialize();//参数序列化
            jQuery.ajax({
                url:"/main/regist",
                data:params,
                type:"post",
                success:function (result) {
                    jQuery("#regist_btn").attr("disabled",false);
                    var jsonObject = JSON.parse(result);
                    var status = jsonObject.status;//-2 重复 -1 失败 0成功
                    if(status == "-2"){//重复
                        tip("#username_regist","用户名已存在！");
                    }else{
                        var htmlStr = "<i class='glyphicon glyphicon-info-sign'></i>&nbsp;";
                        var color = "";
                        if(status == "-1"){//注册失败了
                            htmlStr += "注册失败";
                            color = "#a94442";
                        }else{//成功
                            //jQuery("#registModal").modal('hide');
                            htmlStr += "注册成功";
                            color = "#3c763d";
                        }
                        modalTip("#registModal","#registTipModal","#regist_tip_content",color,htmlStr);
                    }
                }
            })
        }else{
            if(password_regist != password2_regist){//2次密码输入不一致，需要提示并重新输入
                tip("#password2_regist","2次密码输入不一致！");
                jQuery("#password2_regist").val("");
                jQuery("#password2_regist").focus();
                jQuery("#regist_btn").attr("disabled",false);
            }else{
                if(super_password_regist == password_regist){//2次密码输入一致，才验证超级密码和密码的一致性
                    tip("#super_password_regist","超级密码不能和密码一致！");
                    jQuery("#super_password_regist").val("");
                    jQuery("#super_password_regist").focus();
                    jQuery("#regist_btn").attr("disabled",false);
                }
            }
        }
    }else{
        if(username_regist == ""){
            tip("#username_regist","用户名不能为空！");
        }
        if(password_regist == ""){
            tip("#password_regist","密码不能为空！");
        }
        if(password2_regist == ""){
            tip("#password2_regist","密码不能为空！");
        }
        if(super_password_regist == ""){
            tip("#super_password_regist","密码不能为空！");
        }
        jQuery("#regist_btn").attr("disabled",false);
    }
}

/**
 * 找回密码
 * */
function resetPassword() {

    jQuery("#forget_btn").attr("disabled",true);

    var username_forget = jQuery("#username_forget").val();
    var super_password_forget = jQuery("#super_password_forget").val();
    var new_password = jQuery("#new_password").val();
    var confirm_password = jQuery("#confirm_password").val();

    if(username_forget != "" && super_password_forget != "" && new_password != ""
        && confirm_password != ""){
        if(super_password_forget != new_password && new_password == confirm_password){
            var params = jQuery("#forget_form").serialize();
            jQuery.ajax({
                url:"/main/resetPassword",
                data:params,
                type:"post",
                success:function (result) {
                    jQuery("#forget_btn").attr("disabled",false);
                    var jsonObject = JSON.parse(result);
                    var status = jsonObject.status;
                    var htmlStr = "<i class='glyphicon glyphicon-info-sign'></i>&nbsp;";
                    var color = "";
                    if(status == "-1"){//注册失败了
                        htmlStr += "重置密码失败";
                        color = "#a94442";
                    }else{//成功
                        //jQuery("#registModal").modal('hide');
                        htmlStr += "重置密码成功";
                        color = "#3c763d";
                    }
                    modalTip("#forgetModal","#forgetTipModal","#forget_tip_content",color,htmlStr);
                }
            })
        }else{
            if(super_password_forget == new_password){
                tip("#new_password","密码不能和超级密码一致！");
                jQuery("#new_password").val("");
                jQuery("#confirm_password").val("");
                jQuery("#new_password").focus();
                jQuery("#forget_btn").attr("disabled",false);
            }else{
                if(new_password != confirm_password){
                    tip("#confirm_password","2次密码输入不一致！");
                    jQuery("#confirm_password").val("");
                    jQuery("#confirm_password").focus();
                    jQuery("#forget_btn").attr("disabled",false);
                }
            }
        }

    }else{
        if(username_forget == ""){
            tip("#username_forget","用户名不能为空！");
        }
        if(super_password_forget == ""){
            tip("#super_password_forget","密码不能为空！");
        }
        if(new_password == ""){
            tip("#new_password","密码不能为空！");
        }
        if(confirm_password == ""){
            tip("#confirm_password","密码不能为空！");
        }
        jQuery("#forget_btn").attr("disabled",false);
    }
}

/**
 * 输入校验，不能输入中文和特殊字符
 */
function onInput(domkey) {
    var selectorName = "#" + domkey;
    var value = jQuery(selectorName).val();//获取到输入元素的表单值

    if(value.length > 11){
        //提示
        if(domkey.indexOf("username") != -1){
            tip(selectorName,"用户名不能超过11个字符！");
        }else{
            tip(selectorName,"密码不能超过11个字符！");
        }
    }

    //替换所有非法字符
    value = value.replace(/[^a-zA-Z0-9]/g,"");//所有非字母和数字都被替换成空字符串

    //截取长度
    value = value.substring(0,11);

    jQuery(selectorName).val(value);

    if(domkey == "password2_regist" || domkey == 'confirm_password'){//注册
        passwordValidate(domkey);
    }else{
        jQuery(selectorName).focus();
    }
}

/**
 * 密码验证
 */
function passwordValidate(domkey) {
    var selectorName = "";
    if(domkey == "password2_regist") {
        selectorName = "#password_regist";
    }else{
        selectorName = "#new_password";
    }
    var password_prefix = jQuery(selectorName).val();
    if(password_prefix == ""){
        tip(selectorName,"请输入密码！");
        jQuery("#" + domkey).val("");
        jQuery(selectorName).focus();
    }
}

/**
 * 提示
 * */
function tip(selectorName, text) {
    jQuery(selectorName + "_tip").text(text);//利用div clear both属性可以做隐藏提示功能
    setTimeout(function () {
        jQuery(selectorName + "_tip").text("");
    },2000);//延时取消提示
}

/**
 * 登录验证
 * */
function login() {
    //开始就应该将登录按钮置灰
    jQuery("#login_btn").attr("disabled",true);

    var username = jQuery("#username").val();//获取用户输入用户名
    var password = jQuery("#password").val();//获取用户输入密码
    if(username != "" && password != ""){//不为空
        //字符长度全部限制为11位以下
        var params = jQuery("#login_form").serialize();
        jQuery.ajax({
            url:"/main/login",
            data:params,
            type:"post",
            success:function (result) {
                //提示
                var jsonObject = JSON.parse(result);//先解析成json对象
                var status = jsonObject.status;
                if(status != "-1"){
                    window.location.href = "/main/main?result=" + status;
                }else{
                    tip("#username","用户名或密码错误！");
                    jQuery("#password").val("");
                    //失败了，不应该重新请求该页面
                    //window.location.href = "/main/index?result=" + status;
                }
                jQuery("#login_btn").attr("disabled",false);
            },
            error:function () {
                alert("请求失败，请联系管理员！");
                jQuery("#login_btn").attr("disabled",false);
            }
        })
    }else{
        //提示
        if(username == ""){
            tip("#username","用户名不能为空！");
        }
        if(password == ""){
            tip("#password","密码不能为空！");
        }
        jQuery("#login_btn").attr("disabled",false);
    }
}

/**
 * 清理表单
 * */
function clearForm(flag) {
    if(flag == 0){
        jQuery("#forget_form input").val("");
    }else{
        jQuery("#regist_form input").val("");
    }
}