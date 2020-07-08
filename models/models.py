from sqlalchemy import Column, Integer, String, Text, DateTime
from models.database import Base
#from datetime import datetime

#databaseファイルで作ったDB情報の入ってるBase変数を引数として受け取ってそこにテーブル作成及び列定義
class VtuberContent(Base):
    __tablename__ = 'vtubercontent'
    id = Column(Integer, primary_key=True)
    title = Column(String(500))
    name = Column(String(100))
    date = Column(String(20))
    url1 = Column(String(200))
    url2 = Column(String(200))

    #date = Column(DateTime, default=datetime.now())

    def __init__(self, title=None, name=None, date=None, url1=None, url2=None):
        self.title = title
        self.name = name
        self.date = date
        self.url1 = url1
        self.url2 = url2

    def __repr__(self):
        return '<Title %r>' % (self.title)

class VtuberName(Base):
    __tablename__ = 'vtubername'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    url = Column(String(200))

    #date = Column(DateTime, default=datetime.now())

    def __init__(self, name=None, url=None):
        self.name = name
        self.url = url

    def __repr__(self):
        return '<namae %r>' % (self.namae)