from database.models.country import Country
from database.models.server import Server
from database.db_engine import DatabaseEngine as db
from database.models.vpn import Vpn
from utils.my_exception import ExceptionType, MyException

class ServerDao():
    
    @staticmethod
    def save(server):
        session = None
        try:
            session = db.create_session()
            session.add(server)
            session.commit()
        except Exception as ex:
            exception = MyException(str(ex), ExceptionType.DB_ERROR)
            raise exception
        finally:
            if session is not None:
                session.close()
        
    @staticmethod
    def get_servers_with_given_country(country:str) -> list[Server]:
        session = None
        servers = []
        try:
            session = db.create_session()
            servers = session.query(Server) \
                .join(Country) \
                .filter(Country.name == country) \
                .all()
        except Exception as ex:
            exception = MyException(str(ex), ExceptionType.DB_ERROR)
            raise exception
        finally:
            if session is not None:
                session.close()   
        return servers

    @staticmethod
    def get_by_id(server_id):
        session = None
        server = None
        try:
            session = db.create_session()
            server = session.query(Server) \
                .filter(Server.id == server_id) \
                .first()
        except Exception as ex:
            exception = MyException(str(ex), ExceptionType.DB_ERROR)
            raise exception
        finally:
            if session is not None:
                session.close()
        return server
            