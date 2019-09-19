from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.types import DateTime

class Items(Base):
    """Items table"""
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    quantity = Column(Integer)
    description = Column(String(256))
    date_added = Column(DateTime())

    def __init__(self, name=None, quantity=0, description=None, date_added=None):
        self.name = name
        self.quantity = quantity
        self.description = description
        self.date_added = date_added
    
    def __repr__(self):
        return '<Item %s (%d), %s, %s>' % (self.name, self.quantity, self.description, self.date_added)

    def __str__(self):
    	return 'Name: %s | Quantity: %d | Description: %s | Date_added: %s' % (self.name, self.quantity, self.description, self.date_added)
