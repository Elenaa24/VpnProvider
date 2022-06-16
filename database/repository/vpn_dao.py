from datetime import datetime, timedelta
from database.models.vpn import Vpn
from database.db_engine import DatabaseEngine as db
from utils.my_exception import ExceptionType, MyException

class VpnDao():
    
    @staticmethod
    def save(vpn):
        session = None
        try:
            session = db.create_session()
            session.add(vpn)
            session.commit()
        except Exception as ex:
            exception = MyException(str(ex), ExceptionType.DB_ERROR)
            raise exception
        finally:
            if session is not None:
                session.close()
    
    @staticmethod
    def set_subscribe(vpn_id, value):
        session = None
        vpn = None
        try:
            session = db.create_session()
            vpn = session.query(Vpn) \
                .filter(Vpn.id == vpn_id).first()
            vpn.subscripe = value
            session.commit()
        except Exception as ex:
            exception = MyException(str(ex), ExceptionType.DB_ERROR)
            raise exception
        finally:
            if session is not None:
                session.close()
    
    @staticmethod
    def get_by_id(id):
        session = None
        vpn = None
        try:
            session = db.create_session()
            vpn = session.query(Vpn) \
                .filter(Vpn.id == id).first()
        except Exception as ex:
            exception = MyException(str(ex), ExceptionType.DB_ERROR)
            raise exception
        finally:
            if session is not None:
                session.close()
        return vpn
    
    @staticmethod
    def get_client_by_vpn_id(id):
        session = None
        client = None
        try:
            session = db.create_session()
            vpn = session.query(Vpn) \
                .filter(Vpn.id == id).first()
            client = vpn.client
        except Exception as ex:
            exception = MyException(str(ex), ExceptionType.DB_ERROR)
            raise exception
        finally:
            if session is not None:
                session.close()
        return client
    
    @staticmethod
    def get_server_by_vpn_id(id):
        session = None
        server = None
        try:
            session = db.create_session()
            vpn = session.query(Vpn) \
                .filter(Vpn.id == id).first()
            server = vpn.server
        except Exception as ex:
            exception = MyException(str(ex), ExceptionType.DB_ERROR)
            raise exception
        finally:
            if session is not None:
                session.close()
        return server
    
    @staticmethod
    def get_current_vpn_by_server_and_client(server_id, client_id):
        session = None
        vpn = None
        try:
            session = db.create_session()
            vpn = session.query(Vpn) \
                .filter(Vpn.server_id == server_id, Vpn.client_id == client_id) \
                .filter(Vpn.running == True) \
                .first()
        except Exception as ex:
            exception = MyException(str(ex), ExceptionType.DB_ERROR)
            raise exception
        finally:
            if session is not None:
                session.close()
        return vpn
    
    @staticmethod
    def get_all_vpns_for_client(client_id:int):
        session = None
        vpn = []
        try:
            session = db.create_session()
            vpn = session.query(Vpn) \
                .filter(Vpn.client_id == client_id) \
                .all()
            for v in vpn:
                # v.server
                v.server.country
        except Exception as ex:
            exception = MyException(str(ex), ExceptionType.DB_ERROR)
            raise exception
        finally:
            if session is not None:
                session.close()
        return vpn
    
    @staticmethod
    def get_all_expired_vpns():
        session = None
        vpn = []
        try:
            session = db.create_session()
            vpn = session.query(Vpn) \
                .filter(Vpn.expiration_date < datetime.date(datetime.now()))  \
                .filter(Vpn.running == True) \
                .all()
        except Exception as ex:
            exception = MyException(str(ex), ExceptionType.DB_ERROR)
            raise exception
        finally:
            if session is not None:
                session.close()
        return vpn
    
    @staticmethod
    def get_all_vpns_which_needs_reminder_email():
        session = None
        vpn = []
        try:
            session = db.create_session()
            vpn = session.query(Vpn) \
                .filter((Vpn.expiration_date - datetime.date(datetime.now())) < 10)  \
                .filter(Vpn.running == True) \
                .filter(Vpn.subscripe == True) \
                .all()
        except Exception as ex:
            exception = MyException(str(ex), ExceptionType.DB_ERROR)
            raise exception
        finally:
            if session is not None:
                session.close()
        return vpn
    
    @staticmethod
    def modify_running(id_vpn:int, value:bool):
        session = None
        try:
            session = db.create_session()
            vpn = session.query(Vpn) \
                .filter(Vpn.id == id_vpn)  \
                .first()
            vpn.running = value
            session.commit()
        except Exception as ex:
            exception = MyException(str(ex), ExceptionType.DB_ERROR)
            raise exception
        finally:
            if session is not None:
                session.close()