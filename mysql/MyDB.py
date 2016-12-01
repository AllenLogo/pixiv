# -*- coding: utf-8 -*-

"""
数据库操作封装
"""

from sqlalchemy import Column, String, create_engine, Text, Integer, TIMESTAMP,MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:@localhost:3306/pixiv?charset=utf8')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

class MyDBBase:
    def save(self):
        # 创建session对象:
        session = DBSession()
        # 添加到session:
        session.add(self)
        # 提交即保存到数据库:
        session.commit()
        # 关闭session:
        session.close()

    def find(self, **kwargs):
        session = DBSession()
        lists = []
        lists = session.query(self.__class__).filter_by(**kwargs).all()
        #print(session.query(self.__class__).filter(self.__class__.pid == 1).first())
        return lists

class ImgDB(Base, MyDBBase):
    # 表的名字:
    __tablename__ = 'img'
    # 表的结构:
    pid = Column(String(12), primary_key=True)
    author = Column(String(12))
    url = Column(String(100))
    x = Column(Integer)
    y = Column(Integer)
    date = Column(TIMESTAMP)

class TagsDB(Base, MyDBBase):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    pid = Column(String(12))
    tag = Column(Text)
    date = Column(TIMESTAMP, autoincrement=True)

if __name__ == '__main__':
    #Base.metadata.create_all(engine)
    print(ImgDB().find(author='12'))