# !/usr/bin/env python
# -*- coding: utf-8 -*-

import paramiko


class SftpLink(object):
    def __init__(self, host, port, user, password):
        conn = paramiko.Transport((host, port))
        conn.connect(username=user, password=password)
        self.sftp = paramiko.SFTPClient.from_transport(conn)

    def test_dir(self, remote_path):
        """检测文件夹是否存在"""
        try:
            self.sftp.stat(remote_path)
            return True
        except FileNotFoundError:
            return False