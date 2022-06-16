from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Date, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship
from .base import Base

class Vpn(Base):
    __tablename__ = 'vpn_tunnels'
    id = Column(Integer, primary_key=True)
    created_date = Column(Date)
    expiration_date = Column(Date)
    server_id = Column(Integer, ForeignKey('servers.id'), nullable=False)
    server = relationship('Server', back_populates="vpn_tunnels")
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    client = relationship('Client', back_populates="vpn_tunnels")
    running = Column(Boolean, default=True)
    subscripe = Column(Boolean, default=False)

    def __init__(self, created_date, expiration_date, client, server, subscribe=False) -> None:
        print('hello')
        self.created_date = created_date
        self.expiration_date = expiration_date
        self.client = client
        self.server = server
        self.subscripe = subscribe
    
    def __repr__(self):
        return "<VPN(created='{}', expiration='{}', server={}, client={})>"\
                .format(self.created_date, self.expiration_date, self.server_id, self.client_id)
    
    