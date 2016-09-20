# -*- coding: utf-8 -*-

"""
数据库操作封装
"""

from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:@localhost:3306/pixiv?charset=utf8')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

# 定义User对象:
class Up(Base):
    # 表的名字:
    __tablename__ = 'up'
    # 表的结构:
    pid = Column(String(12), primary_key=True)
    name = Column(String(50))
    url = Column(String(100))
    recdate = Column(Integer)
    padate = Column(Integer)

    def save(self):
        # 创建session对象:
        session = DBSession()
        # 添加到session:
        session.add(self)
        # 提交即保存到数据库:
        session.commit()
        # 关闭session:
        session.close()