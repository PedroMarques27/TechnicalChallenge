from typing import List, Optional, Union
from fastapi import Depends, FastAPI, HTTPException
from requests import Session
from app.src.models import LocationData, LocationDataResponse
from app.src.repository import Repository
from app.src.scraper_initializer import ScraperInitializer
from app.src.config import Config

app = FastAPI()

config_loader = Config("app/src/configs.json")
config_loader.load_data()

scr = ScraperInitializer(config_loader)
scr.run()

repo = Repository(config_loader.configuration)

@app.get("/scrape")
async def run_scraper():
    try:
        await scr.run_async()
    except Exception as e:
        return {"status": "error", "message": str(e)}


# Dependency to get the DB session
def get_db():
    db = repo.connect()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def search_items(db: Session = Depends(get_db), location: Optional[str] = None, region: Optional[str] = None):
    results = repo.get_by(db, location, region)
    if not results or results.__len__() == 0:
        raise HTTPException(status_code=404, detail="No items found matching the criteria")
    return results


@app.delete("/")
def delete_items(location: Optional[str] = None, region: Optional[str] = None, db: Session = Depends(get_db)):
    results = repo.get_by(db, location, region)
    if not results or results.__len__() == 0:
        raise HTTPException(status_code=404, detail="No items found matching the criteria")
    repo.delete(db, results[0])
    

@app.put("/{region}/{location}")
def update_item(region: str, location: str, item_data: LocationDataResponse, db: Session = Depends(get_db)):

    results = repo.get_by(db, location, region)
    
    if not results or results.__len__() == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    item = results[0]
    item.location = item_data.location
    item.region = item_data.region
    item.region_code = item_data.region_code
    item.value = item_data.value

    repo.update(db, item)
