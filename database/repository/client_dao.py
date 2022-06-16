from database.models.client import Client
from database.db_engine import DatabaseEngine as db
from utils.my_exception import ExceptionType, MyException

class ClientDao():
    
    @staticmethod
    def save(client):
        session = None
        try:
            session = db.create_session()
            session.add(client)
            session.commit()
        except Exception as ex:
            exception = MyException(str(ex), ExceptionType.DB_ERROR)
            raise exception
        finally:
            if session is not None:
                session.close()
    
    @staticmethod
    def get_by_id(client_id):
        session = None
        client = None
        try:
            session = db.create_session()
            client = session.query(Client) \
                .filter(Client.id == client_id) \
                .first()
        except Exception as ex:
            exception = MyException(str(ex), ExceptionType.DB_ERROR)
            raise exception
        finally:
            if session is not None:
                session.close()
        return client
    
    @staticmethod
    def get_by_mail(client_mail):
        session = None
        client = None
        try:
            session = db.create_session()
            client = session.query(Client) \
                .filter(Client.mail == client_mail) \
                .first()
        except Exception as ex:
            exception = MyException(str(ex), ExceptionType.DB_ERROR)
            raise exception
        finally:
            if session is not None:
                session.close()
        return client

    @staticmethod
    def verify_authentication(mail, password):
        session = None
        authentication_response = True
        try:
            session = db.create_session()
            client = session.query(Client) \
                .filter(Client.mail == mail).first()
            if client is None or not client.verify_password(password):
                authentication_response = False
        except Exception as ex:
            exception = MyException(str(ex), ExceptionType.DB_ERROR)
            raise exception
        finally:
            if session is not None:
                session.close()
        return authentication_response


    