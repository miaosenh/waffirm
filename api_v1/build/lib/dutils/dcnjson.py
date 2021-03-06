#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# *********************************************************************
# Software : PyCharm
#
# dcnjson.py - json数据读取存储打印等相关操作
#
# Author    :yanwh(yanwh@digitalchina.com)
#
# Version 1.0.0
#
# Copyright (c) 2004-9999 Digital China Networks Co. Ltd 
#
#
# *********************************************************************
# Change log:
#       - 2018/1/4 12:45  add by yanwh
#
# *********************************************************************
import os as _os
import time
from datetime import datetime as _dt, date as _d
from json import dumps as _dumps, load as _load

__all__ = ['JsonHandle', 'json_pretty_print']
_FILTER_CHAR = ('ftplib.FTP', 'logging.Logger', 'utils.dcnlogs.LogHandle')  # 用于过滤vars()中过滤无效参数


class JsonHandle(object):
    """
    用于将确认测试用例执行中产生的所有参数转换成json格式存储，便于定位和调试.
    目前暂时还未考虑不同的测试类型后面参数会变化的场景
    使用方法
    j = JsonHandle(src,path,**kwargs)其中src为字典， path为json文件存放路径，二者不可同时传入
    j.save_data_to_file(_path) 将json数据存放到_path
    j.load_data_from_file(__path)  从指定路径__path读取json数据
    """
    
    def __init__(self, src_data='', src_load_path='', **kwargs):
        """
        :param src: 传入运行主函数脚本所在的模块的vars参数字典，_get_env_dict(**src)对字典进行过滤，获取有效信息，
        args_to_json(self.json_data)将参数转换成json格式文件默认存放在该模块所在同名目录，命名默认为
        waffirm_env_argument.json(其中xx取决于你运行脚本的模块名称)
        [说明]:
        file_to_save = os.path.split(__file__)[1].replace(r'.py', r'.json')
        通过该命令实现自动替换,不过目前由于平台(thread_pause模块)调用模块waffirm_main.py使用execfile(xxx, {}函数导致命名空间
        被初始化因此namespace中不存在__file__，所以如果修改会报错
        """
        self.raw_data = src_data
        self.load_path = src_load_path
        self.__init_env()
    
    def __init_env(self):
        """
        初始化变量,同时判断src_data和src_load_path不能同时存在，src_data必须为dict类型
        :return:
        """
        if self.raw_data and not self.load_path:
            del self.load_path
            if not isinstance(self.raw_data, dict):
                print('[Error] {0} should be Dict'.format(self.raw_data))
                raise TypeError
        elif not self.raw_data and self.load_path:
            del self.raw_data
        elif self.raw_data and self.load_path:
            print('raw_data and load_path should not exist at the same time')
            raise TypeError
        else:
            del self.load_path
            del self.raw_data
    
    def save_data_to_file(self, save_path, save_name=''):
        if hasattr(self, 'raw_data'):
            _res = self._get_valid_dict(**self.raw_data)
            if save_path and _os.path.isdir(save_path) and not save_name:
                _save_name = _os.path.join(save_path, _os.path.split(__file__)[1].replace(r'.py', r'.json'))
            elif save_path and _os.path.isdir(save_path) and save_name:
                _save_name = _os.path.join(save_path, save_name)
            elif save_path and _os.path.isfile(save_path):
                _save_name = save_path
            else:
                _save_name = save_path
            self._args_to_json_file(_save_name, _res)
        else:
            print('[Error] raw_data is not exsit')
            raise TypeError
    
    def load_data_from_file(self, src_path=''):
        if hasattr(self, 'load_path'):
            if _os.path.isfile(self.load_path):
                return self._json_file_to_args(self.load_path)
            else:
                print('save path is not a file')
                raise TypeError
        elif src_path:
            if _os.path.isfile(src_path):
                return self._json_file_to_args(src_path)
        else:
            print('[Error] src_load_path or src_path is not exist')
            raise TypeError
    
    @staticmethod
    def __default(obj):
        """
        :param obj:
        :return: 此处扩展json库时期支持对日期类型进行序列化，后面可以根据实际需求在此处扩展json支持的序列化的数据类型
        """
        if isinstance(obj, _dt):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, _d):
            return obj.strftime('%Y-%m-%d')
        else:
            raise TypeError('% r is not JSON serializable' % obj)
    
    @staticmethod
    def _get_valid_dict(constants=_FILTER_CHAR, **kwargs):
        # 过滤vars()中无效字典参数，constans用于过滤vars()里面有些变量值str之后不是以'<'开头
        # (默认大部分库和函数的值str之后都是以<打头)
        dic_data = {}
        for k, v in list(kwargs.items()):
            if k.startswith(r'__'):
                continue
            elif k.startswith(r'_'):
                continue
            else:
                if str(v).startswith('<'):
                    continue
                elif str(v).startswith('_'):
                    continue
                elif any(x in str(v) for x in constants):
                    continue
                else:
                    dic_data[k] = v
        return dic_data
    
    @staticmethod
    def _args_to_json_file(save_path, kwargs):
        # 将过滤后有效数据存储为json文件同时增加使用default和indent分别对序列化的json参数进行
        # 对日期类型序列化支持和显示出来的indent参数更加人性化
        with open(save_path, 'w+') as json_data:
            json_data.write(_dumps(kwargs, encoding='UTF-8', default=JsonHandle.__default, indent=4))
            time.sleep(0.1)
    
    @staticmethod
    def _json_file_to_args(src_path):
        with open(src_path, 'rb') as json_data:
            return _load(json_data, encoding='utf-8')


def json_pretty_print(_data):
    print(_dumps(_data, sort_keys=True, indent=4, ensure_ascii=False))
