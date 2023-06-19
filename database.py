from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer,String,Numeric,create_engine
from sqlalchemy.schema import UniqueConstraint
engine = create_engine('sqlite:///database.db')
factory = sessionmaker(bind=engine)
session = factory()
Base=declarative_base()
class Pole(Base):
    __tablename__="pole"
    id=Column(Integer,primary_key=True)
    address=Column(String(300))
class Customer(Base):
    __tablename__="customer"
    pole_id = Column(Integer, ForeignKey('pole.id'),primary_key=True)
    name=Column(String(300))
    capacity=Column(Integer)
class Resource(Base):
    __tablename__="resource"
    pole_id = Column(Integer, ForeignKey('pole.id'),primary_key=True)
    name=Column(String(300))
    capacity=Column(Integer)
class Line(Base):
    __tablename__="Line"
    line_id=Column(Integer,autoincrement=True,primary_key=True)
    from_pole=Column(Integer, ForeignKey('pole.id'))
    to_pole=Column(Integer, ForeignKey('pole.id'))
    investment_cost=Column(Integer)
    flow_cost=Column(Integer)
    init_resistance=Column(Integer)
    max_resistance=Column(Integer)
    length=Column(Integer)
    __table_args__ = (
        UniqueConstraint('from_pole', 'to_pole'),
    )
class RequiredEnergy(Base):
    __tablename__="requiredenergy"
    year=Column(Integer,primary_key=True)
    energy=Column(Integer)
if __name__=="__main__":                                                                         
    Base.metadata.create_all(engine)