# !/usr/bin/env python
# -*- coding: utf-8 -*-

import time


class ParamsModel(object):
    @staticmethod
    def get_params_list_all(cursor, condition, page=1, limit=10):
        """获取所有参数列表"""
        command = '''
        SELECT param_id, param_type, param_index, param_name, param_value, param_desc,
        source_name, a.is_deleted
        FROM tb_param_config AS a
        LEFT JOIN tb_datasource AS b USING(source_id)
        %s
        ORDER BY param_id
        LIMIT :limit OFFSET :offset
        '''

        command = command % condition
        result = cursor.query(command, {
            'limit': limit,
            'offset': (page - 1) * limit
        })
        return result if result else []

    @staticmethod
    def get_params_count_all(cursor, condition):
        """获取参数条数"""
        command = '''
        SELECT COUNT(*) AS count
        FROM tb_param_config AS a
        LEFT JOIN tb_datasource AS b USING(source_id)
        %s
        '''

        command = command % condition
        result = cursor.query_one(command)
        return result['count'] if result else 0

    @staticmethod
    def add_params_detail(cursor, param_type, param_name, param_index, source_id, param_value, param_desc,
                          user_id):
        """新增参数"""
        command = '''
        INSERT INTO tb_param_config(param_type, param_name, param_index, source_id, param_value, param_desc,
        insert_time, update_time, creator_id, updater_id)
        VALUES(:param_type, :param_name, :param_index, :source_id, :param_value, :param_desc,
        :insert_time, :update_time, :creator_id, :updater_id)
        '''
        result = cursor.insert(command, {
            'param_type': param_type,
            'param_name': param_name,
            'param_index': param_index,
            'source_id': source_id,
            'param_value': param_value,
            'param_desc': param_desc,
            'insert_time': int(time.time()),
            'update_time': int(time.time()),
            'creator_id': user_id,
            'updater_id': user_id
        })
        return result

    @staticmethod
    def add_param_many(cursor, data):
        """新增参数-批量"""
        command = '''
        INSERT INTO tb_param_config(param_type, param_name, param_index, source_id,
        param_value, param_desc, insert_time, update_time, creator_id, updater_id)
        VALUES(:param_type, :param_name, :param_index, :source_id, :param_value, :param_desc,
        :insert_time, :update_time, :creator_id, :updater_id)
        '''
        result = cursor.insert(command, args=data)
        return result

    @staticmethod
    def get_params_detail(cursor, param_id):
        """获取参数详情"""
        command = '''
        SELECT param_type, param_name, source_id, param_value, param_desc, a.is_deleted,
        param_index
        FROM tb_param_config AS a
        WHERE param_id = :param_id
        '''
        result = cursor.query_one(command, {
            'param_id': param_id
        })
        return result if result else {}

    @staticmethod
    def get_params_detail_by_name(cursor, param_name):
        """获取参数详情by参数名称"""
        command = '''
        SELECT *
        FROM tb_param_config
        WHERE param_name = :param_name
        '''
        result = cursor.query_one(command, {
            'param_name': param_name
        })
        return result if result else {}

    @staticmethod
    def update_params_detail(cursor, param_id, param_type, param_name, param_index, source_id, param_value, param_desc,
                             is_deleted, user_id):
        """修改参数详情"""
        command = '''
        UPDATE tb_param_config
        SET param_type = :param_type, param_name = :param_name, param_index = :param_index, source_id = :source_id,
        param_value = :param_value, param_desc = :param_desc,
        update_time = :update_time, updater_id = :updater_id, is_deleted = :is_deleted
        WHERE param_id = :param_id
        '''
        result = cursor.update(command, {
            'param_id': param_id,
            'param_type': param_type,
            'param_name': param_name,
            'param_index': param_index,
            'source_id': source_id,
            'param_value': param_value,
            'param_desc': param_desc,
            'is_deleted': is_deleted,
            'update_time': int(time.time()),
            'updater_id': user_id
        })
        return result

    @staticmethod
    def get_params_detail_not_delete(cursor, param_id):
        """获取非删除参数"""
        command = '''
        SELECT a.param_id, GROUP_CONCAT(b.job_id) AS job_id, a.param_type
        FROM tb_param_config AS a
        LEFT JOIN tb_job_param AS b ON a.param_id = b.param_id AND b.is_deleted = 0
        WHERE a.param_id = :param_id
        GROUP BY a.param_id
        '''
        result = cursor.query_one(command, {
            'param_id': param_id
        })
        return result if result else {}

    @staticmethod
    def delete_params_detail(cursor, param_id, user_id):
        """删除参数"""
        command = '''
        DELETE FROM tb_param_config
        WHERE param_id = :param_id
        '''
        result = cursor.update(command, {
            'update_time': int(time.time()),
            'updater_id': user_id,
            'param_id': param_id
        })
        return result

    @staticmethod
    def delete_params_many(cursor, condition, user_id):
        """删除参数"""
        command = '''
        DELETE FROM tb_param_config
        WHERE param_id IN %s
        '''
        command = command % condition

        result = cursor.update(command, {
            'updater_id': user_id,
            'update_time': int(time.time())
        })
        return result

    @staticmethod
    def get_params_all(cursor):
        """获取所有参数"""
        command = '''
        SELECT param_id, param_name
        FROM tb_param_config
        WHERE is_deleted = 0
        '''
        result = cursor.query(command)
        return result if result else []

    @staticmethod
    def get_params_index_all(cursor):
        """获取所有参数目录"""
        command = '''
        SELECT DISTINCT param_index
        FROM tb_param_config
        WHERE is_deleted = 0
        '''
        result = cursor.query(command)
        return result if result else []

    @staticmethod
    def get_param_by_source_id(cursor, source_id):
        """获取参数详情by数据源id"""
        command = '''
        SELECT COUNT(*) AS count
        FROM tb_param_config
        WHERE source_id = :source_id
        '''
        result = cursor.query_one(command, {
            'source_id': source_id
        })
        return result['count'] if result else 0
