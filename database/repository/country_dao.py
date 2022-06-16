from database.models.country import Country
from database.db_engine import DatabaseEngine as db
from utils.my_exception import ExceptionType, MyException

class CountryDao():
    
    @staticmethod
    def save(country):
        session = None
        try:
            session = db.create_session()
            session.add(country)
            session.commit()
        except Exception as ex:
            exception = MyException(str(ex), ExceptionType.DB_ERROR)
            raise exception
        finally:
            if session is not None:
                session.close()
    
    @staticmethod
    def get_all():
        session = None
        countries = []
        try:
            session = db.create_session()
            countries = session.query(Country).all()
        except Exception as ex:
            exception = MyException(str(ex), ExceptionType.DB_ERROR)
            raise exception
        finally:
            if session is not None:
                session.close()
        return countries
    
    @staticmethod
    def get_all_names_and_ids():
        session = None
        countries = []
        try:
            session = db.create_session()
            countries = session.query(Country.name).all()
        except Exception as ex:
            exception = MyException(str(ex), ExceptionType.DB_ERROR)
            raise exception
        finally:
            if session is not None:
                session.close()
        return countries