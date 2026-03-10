from sqlalchemy.orm import Session
from backend import models, schemas
from backend.models import ParkingSpace
# session for manage database transactions

def sort(spaces: list[models.ParkingSpace]):
    return sorted(spaces, key=lambda x: (x.level, x.spot_number))
 
def get_all_spaces(db: Session): #i pass session object to function so i can use it to  database queries
    spaces = db.query(models.ParkingSpace).all()
    return sort(spaces)
 
def get_empty_spaces(db: Session):
    spaces = db.query(models.ParkingSpace).filter_by(is_available=True).all()
    return sort(spaces)
 
def get_empty_by_level(db: Session, level: int):
    spaces = db.query(models.ParkingSpace).filter_by(level=level, is_available=True).all()
    return sort(spaces)
 
def update_availability(db: Session, spot_id: int, level: int, spot_number: int, is_available: bool):
    spot = db.query(models.ParkingSpace).filter_by(id=spot_id).first() 
    if not spot:
        return None  
    if spot.level != level or spot.spot_number != spot_number:
        return "Notmatch"  
    if spot.is_available == is_available:
        return "Duplicate"
    spot.is_available = is_available
    
    db.commit()
    db.refresh(spot)
    return spot

def is_full_capacity(db: Session):
    return db.query(models.ParkingSpace).filter_by(is_available=True).count() == 0