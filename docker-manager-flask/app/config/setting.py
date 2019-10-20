""" 
@Time    : 2018/7/15 20:20
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : setting.py
@Desc    : 通用设置配置文件
"""

TOKEN_EXPIRATION = 30 * 24 * 3600
EMAIL_TOKEN_EXPIRATION = 30*60

#分页每页的条数
PAGE_NUM = 10
#上传数据大小限制  超过限制返回413
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB