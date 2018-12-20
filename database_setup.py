import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class CarMake(Base):
    __tablename__ = 'carmake'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    creator = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
			'creator': self.creator,
        }


class CarModel(Base):
    __tablename__ = 'car_models'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    url = Column(String(250))
    msrp = Column(String(8))
    carType = Column(String(250))
    creator = Column(String(250), nullable=False)
    carmake_id = Column(Integer, ForeignKey('carmake.id'))
    carmake = relationship(CarMake)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'url': self.url,
            'id': self.id,
            'msrp': self.msrp,
            'carType': self.carType,
			'creator': self.creator,
        }


engine = create_engine('sqlite:///carlist.db')


Base.metadata.create_all(engine)