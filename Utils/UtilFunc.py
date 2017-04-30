#!/usr/bin/python3

import re

def PackException(outerargs):
    """
    用来包装excetion的
    :param args: 装饰器的参数
    :return:
    """
    def _PackException(func):
        def __PackException(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print("{0}失败，错误原因:{1}".format(str(outerargs), e))
        return __PackException
    return _PackException

def IsStringProxy(aString):
    pattern = re.compile(r"\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}:\d{1,5}")
    return True if pattern.match(aString) else False

