import json
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
import jsonpickle

from .base import Base


class Country(Base):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    server = relationship('Server', back_populates="country")

    def __init__(self, name, server) -> None:
        self.name = name
        self.server = server

    
    