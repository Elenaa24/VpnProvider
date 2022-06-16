from sqlalchemy.orm.session import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from .models.country import Country
from .models.client import Client
from .models.server import Server
from .models.vpn import Vpn

from .models.base import Base


POSTGRES_USER = 'postgres'
POSTGRES_PW = 'pass'
POSTGRES_URL = '127.0.0.1:5432'
POSTGRES_DB = 'VPN'
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)

class DatabaseEngine:
    
    ENGINE = create_engine(DB_URL)
    SESSION = sessionmaker(bind=ENGINE, autoflush=False)

    
    @classmethod
    def create_tables(cls):
        Base.metadata.create_all(cls.ENGINE)
    
    @classmethod
    def create_session(cls) -> Session:
        return cls.SESSION()