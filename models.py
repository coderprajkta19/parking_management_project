from sqlalchemy import Column, Integer, Boolean
from backend.database import Base
 
class ParkingSpace(Base):
    __tablename__ = "parking_spaces"
 
    id = Column(Integer, primary_key=True, index=True)
    level = Column(Integer, nullable=False)
    spot_number = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=True)