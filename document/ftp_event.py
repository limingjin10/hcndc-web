# !/usr/bin/env python
# -*- coding: utf-8 -*-

from configs import api

from flask_restplus import fields

# 文件事件列表请求值
ftp_event_list_request = api.doc(params={
    'event_name': '文件事件名称',
    'status': '调度状态:0全部, 1失效, 2运行中, 3暂停',
    'page': '页码',
    'limit': '条数'
})

# 文件事件修改请求值
ftp_event_update_request = api.doc(body=api.model('ftp_event_update_request', {
    'ftp_event_id': fields.Integer(description='文件事件id'),
    'event_name': fields.String(description='事件名称'),
    'event_desc': fields.String(description='事件描述'),
    'ftp_id': fields.Integer(description='FTP配置id'),
    'data_path': fields.String(description='文件路径'),
    'file_name': fields.String(description='文件名称'),
    'interface_id': fields.String(description='任务流id列表'),
    'start_time': fields.String(description='开始时间: 默认00:00'),
    'end_time': fields.String(description='结束时间: 默认23:59'),
    'interval_value': fields.Integer(description='间隔值: 单位(分钟)'),
    'old_status': fields.Integer(description='旧调度状态: 0.失效, 1.运行中, 2.暂停'),
    'new_status': fields.Integer(description='新调度状态: 0.失效, 1.运行中, 2.暂停')
}, description='调度修改请求参数'))

# 文件事件新增请求值
ftp_event_add_request = api.doc(body=api.model('ftp_event_add_request', {
    'event_name': fields.String(description='事件名称'),
    'event_desc': fields.String(description='事件描述'),
    'ftp_id': fields.Integer(description='FTP配置id'),
    'data_path': fields.String(description='文件路径'),
    'file_name': fields.String(description='文件名称'),
    'interface_id': fields.String(description='任务流id列表'),
    'start_time': fields.String(description='开始时间: 默认00:00'),
    'end_time': fields.String(description='结束时间: 默认23:59'),
    'interval_value': fields.Integer(description='间隔值: 单位(分钟)'),
}, description='调度修改请求参数'))

# 测试FTP文件目录是否存在
ftp_event_test_request = api.doc(body=api.model('ftp_event_test_request', {
    'ftp_id': fields.String(description='FTP配置id'),
    'ftp_type': fields.Integer(description='ftp类型: 1.ftp, 2.sftp'),
    'ftp_host': fields.String(description='ftp域名'),
    'ftp_port': fields.Integer(description='ftp端口'),
    'ftp_user': fields.String(description='ftp用户名'),
    'ftp_passwd': fields.String(description='ftp密码'),
    'data_path': fields.String(description='文件路径')
}, description='测试FTP文件目录是否存在'))

# 立即执行调度事件请求
ftp_event_run_request = api.doc(body=api.model('ftp_event_run_request', {
    'ftp_event_id': fields.List(fields.Integer, description='文件事件id列表'),
    'run_date': fields.String(description='数据日期'),
    'date_format': fields.String(description='数据日期格式')
}, description='立即执行调度请求'))

# 调度事件暂停/恢复请求
ftp_event_action_request = api.doc(body=api.model('ftp_event_action_request', {
    'ftp_event_id': fields.List(fields.Integer, description='文件事件id列表'),
    'action': fields.Integer(description='1.暂停, 2.恢复')
}, description='调度事件暂停/恢复请求参数'))

# 删除调度详情请求
ftp_event_delete_request = api.doc(body=api.model('ftp_event_delete_request', {
    'ftp_event_id': fields.List(fields.Integer, description='文件事件id列表')
}, description='删除调度详情请求'))