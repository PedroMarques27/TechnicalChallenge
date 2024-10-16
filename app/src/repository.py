# repositories/location_repository.py
from typing import Optional
from sqlalchemy.orm import Session, sessionmaker
from app.src.models import LocationData
from sqlalchemy import create_engine
from app.src.models import Base
import time

class Repository:
    def __init__(self, db_configuration: dict):
        self.config = db_configuration
        self.db_url = f"mysql+pymysql://{self.config['user']}:{self.config['password']}@{self.config['host']}/{self.config['database']}"
        
        def create_db_engine(db_url):
            engine = create_engine(db_url)
            for _ in range(5):
                try:
                    with engine.connect() as connection:
                        return engine
                except Exception as e:
                    print("Database not ready yet. Waiting...")
                    time.sleep(5) 
            raise Exception("Database connection failed after multiple attempts")
        engine = create_db_engine(self.db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base.metadata.create_all(bind=engine)

     
        
    def connect(self) -> Session:
        return self.SessionLocal()

    def close_session(self, session: Session):
        session.close()

        
    def create(self, db: Session, location_data: LocationData) -> None:
        try:
            db.add(location_data)
            db.commit()
            db.refresh(location_data)
        except Exception as e:
            print("Error adding location: ", e)
            
    def get_by(self, db: Session, location: Optional[str], region: Optional[str]) -> list[LocationData]:
        query = db.query(LocationData)
        if location:
            query = query.filter(LocationData.location == location)
        if region:
            query = query.filter(LocationData.region == region)
        return query.all()

    def get_all(self, db: Session) -> list[LocationData]:
        return db.query(LocationData).all()

    def update(self, db: Session, location_data: LocationData) -> None:
        db.commit()
        db.refresh(location_data)

    def delete(self, db: Session, location_data: LocationData) -> None:
        db.delete(location_data)
        db.commit()
