from sqlalchemy import Column, INTEGER, String
from sqlalchemy.ext.declarative import declarative_base


# connect to db
from sqlalchemy import create_engine
engine = create_engine('sqlite:///data.db')

# mapping & schema
Base = declarative_base()
class Employee(Base):
    __tablename__ = 'employees'
    id = Column(INTEGER, primary_key=True)
    name = Column(String)
    age = Column(INTEGER)

    def __init__(self, age, name):
        self.age = age
        self.name = name

    def json(self):
        return {'name': self.name, 'age': self.age}

# create table
Base.metadata.create_all(engine)

# connect db wiht a session
from sqlalchemy.orm import sessionmaker
Session = sessionmaker()
Session.configure(bind=engine)
# can be reduce: Session = sessionmaker(bind=engine)
session = Session()

# try inserting a record
session.add(Employee('18', 'Long'))
session.commit()

# try query
print(session.query(Employee).filter_by(name='Long').first().json())

# try update object
long = session.query(Employee).filter_by(name='Long').first()
long.age = 20
session.commit()
print(session.query(Employee).filter_by(name='Long').first().json())

session.rollback()
session.commit()

