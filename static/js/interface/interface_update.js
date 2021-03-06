/**
 * Created by xx on 2018/11/14.
 */
(function () {
    let Controller = function () {
        this.init();
    };

    Controller.prototype = {
        init: function () {
            // 任务流列表请求
            this.interface_list_req();
            // 日期组件渲染
            this.restart('run_time');
            // 表单验证规则
            this.form_verify();
            // 数据初始化赋值
            this.form_data_init();
            // 表单提交
            this.form_event();
        },
        // 任务流列表请求
        interface_list_req: function () {
            $.ajax({
                url: BASE.uri.interface.id_list_api,
                type: 'get',
                success: function (res) {
                    let formSelects = layui.formSelects;
                    let html = [];
                    for (let i = 0; i < res.data.length; i++) {
                        html.push(sprintf(
                            '<option value="%s">%s(%s)</option>',
                            res.data[i].interface_id,
                            res.data[i].interface_id,
                            res.data[i].interface_name
                        ))
                    }
                    $('select[xm-select=parent_interface]').append(html.join(''));
                    formSelects.render('parent_interface');
                }
            })
        },
        // 表单验证
        form_verify: function () {
            layui.use('form', function () {
                let form = layui.form;
                form.verify({
                    // 多选目录验证规则
                    index_verify: function (value, item) {
                        if (!value) {
                            return '必填项不能为空'
                        }
                        if (/,/.test(value)) {
                            return '任务流目录中不得出现逗号字符","'
                        }
                    },
                    // 重试次数验证
                    retry: function (value, item) {
                        if (!value) {
                            return '必填项不能为空'
                        }
                        if (Number(value) < 0 || Number(value) > 10) {
                            return '重试次数请为在0-10之内整数'
                        }
                    }
                })
            })
        },
        // 表单提交
        form_event: function () {
            layui.use('form', function () {
                let form = layui.form;
                form.on('submit(interface-save)', function (data) {
                    data = data.field;
                    // 添加原前置任务流
                    data.old_parent = window.old_parent.join(',');
                    $.ajax({
                        url: BASE.uri.interface.detail_api + window.interface_id + '/',
                        contentType: "application/json; charset=utf-8",
                        type: 'put',
                        data: JSON.stringify(data),
                        success: function (result) {
                            if (result.status === 200) {
                                layer.msg('修改成功', {icon: 6});
                                // 关闭自身iframe窗口
                                setTimeout(function () {
                                    let index = parent.layer.getFrameIndex(window.name);
                                    parent.layer.close(index);
                                }, 2000);
                            } else {
                                layer.msg(sprintf('修改失败[%s]', result.msg), {icon: 5, shift: 6});
                            }
                        },
                        error: function (error) {
                            let result = error.responseJSON;
                            layer.msg(sprintf('修改失败[%s]', result.msg), {icon: 5, shift: 6});
                        }
                    });
                });
            });
        },
        // 数据初始化赋值
        form_data_init: function () {
            $.ajax({
                url: BASE.uri.interface.detail_api + window.interface_id + '/',
                type: 'get',
                success: function (result) {
                    let data = result.data.detail;
                    // 原前置任务流
                    window.old_parent = data.parent_interface;
                    layui.use(['form', 'laydate'], function () {
                        // 详情参数初始化
                        let form = layui.form;
                        let formSelects = layui.formSelects;
                        form.val('interface_detail', {
                            'interface_name': data.interface_name,
                            'interface_desc': data.interface_desc,
                            'interface_index': data.interface_index,
                            'retry': data.retry,
                            'is_deleted': data.is_deleted === 1
                        });
                        form.render();
                        // 数据日期参数初始化
                        if (data.run_time) {
                            let laydate = layui.laydate;
                            laydate.render({
                                elem: 'input[name=run_time]',
                                value: data.run_time
                            })
                        }
                        // 前置任务流依赖初始化
                        formSelects.value('parent_interface', data.parent_interface);
                    });
                }
            });
        },
        // 日期组件渲染
        restart: function (field) {
            layui.use('laydate', function () {
                let laydate = layui.laydate;
                laydate.render({
                    elem: sprintf('input[name=%s]', field),
                    theme: '#393D49',
                    format: 'yyyy-MM-dd',
                    calendar: true,
                    range: false
                })
            });
        },
        element_init: function () {
            // 元素渲染刷新
            layui.use('element', function () {
                let element = layui.element;
                element.init();
            });
        }
    };
    new Controller();
})();