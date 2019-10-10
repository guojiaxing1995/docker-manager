""" 
@Time    : 2018/7/16 20:06
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : redprint.py
@Desc    : 自定义红图
"""

class Redprint:
    def __init__(self,name):
        self.name = name
        self.mound = []

    def route(self,rule,**options):
        def decorator(f):
            self.mound.append((f,rule,options))
            return f
        return decorator

    def register(self,bp,url_prefix=None):
        if url_prefix == None:
            url_prefix = '/' + self.name
        for f,rule,options in self.mound:
            endpoint = self.name + '+' + options.pop("endpoint",f.__name__)
            bp.add_url_rule(url_prefix+rule,endpoint,f,**options)