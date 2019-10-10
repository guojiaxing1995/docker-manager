""" 
@Time    : 2018/7/17 20:10
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : base.py
@Desc    :
"""
from contextlib import contextmanager
from datetime import datetime

from flask_sqlalchemy import BaseQuery,SQLAlchemy as _SQLAlchemy
from sqlalchemy import Column, Integer, SmallInteger, orm, DateTime

from app.libs.error_code import NotFound


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

class Query(BaseQuery):
    def filter_by(self,**kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query,self).filter_by(**kwargs)

    #重写get_or_404
    def get_or_404(self, ident):
        rv = self.get(ident)
        if not rv:
            raise NotFound()
        return rv

    def first_or_404(self):
        rv = self.first()
        if not rv:
            raise NotFound()
        return rv

db = SQLAlchemy(query_class=Query)

class Base(db.Model):
    __abstract__ = True
    create_time = Column(DateTime, default=datetime.now, nullable=False)
    status = Column(SmallInteger, default=1)

    def __getitem__(self, item):
        return getattr(self,item)

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.item():
            if hasattr(self,key) and key != 'id':
                setattr(self,key,value)

    def delete(self):
        self.status = 0

    @classmethod
    def paginate(cls,data,page,pages,total):
        paginate_result = {
            'data': data,
            'page': page,
            'pages': pages,
            'total': total
        }

        return paginate_result


