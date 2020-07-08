from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os


#database.pyと同じパスにonegai.dbというファイルを絶対パスで定義
databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'vtuber.db')
#SQLiteを利用して上で定義した絶対パスにDBを構築
engine = create_engine('sqlite:///' + databese_file, convert_unicode=True)
#DB接続用インスタンスを生成
db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
#Baseオブジェクトを生成して、
Base = declarative_base()
#そこにDBの情報を流し込む
Base.query = db_session.query_property()


def init_db():
    import models.models
    Base.metadata.create_all(bind=engine)