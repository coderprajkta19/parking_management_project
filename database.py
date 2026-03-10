from sqlalchemy import create_engine
#from sqlalchemy.ext.declarative import 
from sqlalchemy.orm import sessionmaker,declarative_base
 
DATABASE_URL = "postgresql://postgres:Prajkta%40123@localhost:5432/parking_data"
 
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()