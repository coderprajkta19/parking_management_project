from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from backend import models, schemas, crud
from backend.database import engine, SessionLocal, Base


# Base.metadata.create_all(bind=engine)

app = FastAPI()

# @app.get("/")
# def root():
#     return {"message": "Parking API is running 🚗"}

app.mount("/static", StaticFiles(directory="backend/static"), name="static")

def get_db(): 
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()
        

@app.get("/parking-spaces", response_model=list[schemas.ParkingSpaceOut])
def read_all_parking(db: Session = Depends(get_db)): 
    return crud.get_all_spaces(db)

@app.get("/parking-spaces/empty", response_model=list[schemas.ParkingSpaceOut])
def read_empty_parking(db: Session = Depends(get_db)):
    empty_spots = crud.get_empty_spaces(db)
    if not empty_spots:
        raise HTTPException(status_code=404, detail="No empty parking spots available")
    return empty_spots

@app.get("/parking-spaces/empty/{level}", response_model=list[schemas.ParkingSpaceOut])
def read_empty_by_level(level: int, db: Session = Depends(get_db)):
    if not (1 <= level <= 3):
        raise HTTPException(status_code=400, detail="Level not found")
    
    empty_spots = crud.get_empty_by_level(db, level)
    if not empty_spots:
        raise HTTPException(status_code=404, detail="No empty parking spots available in this level")
    return empty_spots
    

@app.post("/parking-spaces/update", response_model=schemas.ParkingSpaceOut)
def update_exit_space(data: schemas.ParkingUpdate, db: Session = Depends(get_db)):
    
    if not (1 <= data.level <= 3):
        raise HTTPException(status_code=400, detail="Level not found")
    if not (1 <= data.spot_number <= 10):
        raise HTTPException(status_code=400, detail="Spot number not found")
    
    spot = crud.update_availability(
        db,
        spot_id=data.spot_id,
        level=data.level,
        spot_number=data.spot_number,
        is_available=data.is_available
    )
    if spot is None:
        raise HTTPException(status_code=404, detail="Parking spot id not found")
    elif spot == "Notmatch":
        raise HTTPException(status_code=400, detail="Spot ID not match level and spot number")
    elif spot == "Duplicate":
        raise HTTPException(status_code=409, detail="No change — spot is already in same status")
    else:
        return spot

@app.get("/parking-spaces/full-capacity")
def check_full_capacity(db: Session = Depends(get_db)):
    empty_spots = crud.is_full_capacity(db)
    if not empty_spots:
        raise HTTPException(status_code=404, detail="No , Parking is still available, you can park your car")
    return {"full": crud.is_full_capacity(db)}

@app.get("/", include_in_schema=False)
async def serve_index():
    return FileResponse("backend/static/index.html")