from sqlalchemy import Column, String, Float, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
   
# Define the base class for models
Base = declarative_base()

class LocationData(Base):
    __tablename__ = "location_data"

    location = Column(String(50), nullable=False)
    region = Column(String(50), nullable=False)
    region_code = Column(String(50), nullable=True)
    value = Column(Float, nullable=False)

    # Define composite primary key
    __table_args__ = (
        PrimaryKeyConstraint('location', 'region'),
    )

    def __init__(self, location, region, value, region_code = None):
        self.location = location
        self.region = region
        self.value = value
        self.region_code = region_code
        
    def __repr__(self):
        return f"LocationData(location='{self.location}',region='{self.region}', region_code='{self.region_code}', value={self.value})"
    
    def __eq__(self, other):
        return self.location == other.location and self.region == other.region and self.value == other.value
    
    def __hash__(self):
        return hash((self.location, self.region))  # Combine location and region for hashing
    
    @staticmethod
    def retrieve_location_from_row(key, value, country, regions):
        def try_float(float_value):
            try:
                return float(float_value)
            except (ValueError, TypeError):
                return 0
            
        value = try_float(value)
        
        if country.lower() in key:
            return LocationData(key, key, value)
        else:
            split_key = key.split(' - ')
            
            if len(split_key) == 2:
                region_code = split_key[1].strip().upper()
                return LocationData(split_key[0].strip().lower(),  regions[region_code], value, region_code)
            return LocationData(split_key[0].strip().lower(), country, value)
               
class LocationDataResponse(BaseModel):
    location: str
    region: str
    region_code: str
    value: float

    @classmethod
    def from_orm(cls, db_obj):
        return cls(
            location=db_obj.location,
            region=db_obj.region,
            region_code=db_obj.region_code,
            value=db_obj.value,
        )