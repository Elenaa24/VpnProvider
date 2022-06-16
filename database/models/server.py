from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Server(Base):
    __tablename__ = 'servers'
    id = Column(Integer, primary_key=True)
    ip = Column(String)
    name = Column(String)
    port = Column(Integer)
    vpn_tunnels = relationship("Vpn", back_populates="server")
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)
    country = relationship('Country', back_populates="server")

    def __init__(self, ip, name, port, country) -> None:
        self.ip = ip
        self.name = name
        self.port = port
        self.country = country
    
    def __repr__(self):
        return "<Server(name={}, ip={}, port={})>"\
            .format(self.name, self.ip, self.port)