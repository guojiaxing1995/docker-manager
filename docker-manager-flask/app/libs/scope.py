""" 
@Time    : 2018/7/22 10:08
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : scope.py
@Desc    :
"""
class Scope:
    allow_api = []
    allow_module = []

    def __add__(self,other):
        self.allow_api = self.allow_api + other.allow_api
        #去重
        self.allow_api =list(set(self.allow_api))

        self.allow_module = self.allow_module + other.allow_module
        # 去重
        self.allow_module = list(set(self.allow_module))
        return self

class AdminScope(Scope):
    allow_api = ['v1.user+super_create_user']

class UserScope(Scope):
    allow_module = ['v1.client']
    allow_api = ['v1.user+super_create_user']

class SuperScope(Scope):
    allow_api = []
    def __init__(self):
        self + AdminScope() + UserScope()
        print(self.allow_api)

def is_in_socpe(scope,endpoint):
    #反射获取当前模块的类
    gl = globals()
    scope = globals()[scope]()
    #获取红图的名字 为模块下的所有试图函数赋予权限
    red_name = endpoint.split('+')[0]
    if endpoint in scope.allow_api:
        return True
    if red_name in scope.allow_module:
        return True
    else:
        False


