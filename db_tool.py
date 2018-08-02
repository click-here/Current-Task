import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
import datetime

Base = declarative_base()

class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task_name = Column(String(250), nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, unique=False, default=True)

class Water(Base):
    __tablename__ = 'WaterConsumption'
    id = Column(Integer, primary_key=True)
    amount = Column(Integer,nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    
 
engine = create_engine('sqlite:///task.db')
 
# create table if needed
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


if __name__ == '__main__':
    if len(sys.argv[1:]) != 0:
        task_name = ' '.join(sys.argv[1:])
        task = Task(task_name=task_name)
        session = Session()
        session.add(task)
        session.commit()
