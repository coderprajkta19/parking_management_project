from pydantic import BaseModel, ConfigDict, StrictBool

class ParkingSpaceBase(BaseModel):
    level: int
    spot_number: int
    
    model_config = ConfigDict(from_attributes=True)

class ParkingSpaceOut(ParkingSpaceBase):
    id: int
    is_available: bool
    
    model_config = ConfigDict(from_attributes=True)

class ParkingUpdate(BaseModel):
    spot_id: int
    level: int
    spot_number: int
    is_available: StrictBool
    
    model_config = ConfigDict()
