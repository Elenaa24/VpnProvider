from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates
from .base import Base


class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    mail = Column(String, unique=True)
    password_hash = Column(String)
    register_date = Column(Date)
    vpn_tunnels = relationship("Vpn", back_populates="client")

    @property
    def password(self):
        raise AttributeError('Password is not readable attribute!')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, given_password):
        return check_password_hash(self.password_hash, given_password)

    def __init__(self, mail, register_date) -> None:
        self.mail = mail
        self.register_date = register_date
    
    def __repr__(self):
        return "<Client(mail={}, register_date={})>"\
                .format(self.mail, self.register_date)
