from app.src.services.scraper import Scraper
from app.src.services.data_processor import Processor
from app.src.repository import Repository
from app.src.services.file_finder import FileFinder
from app.src.config import Config

class ScraperInitializer:
    def __init__(self, configuration):
       self.config =configuration
        
    def scrape(self):
        self.scraper = Scraper(self.config.url , self.config.folder)
        filename_url_tuples = self.scraper.scrape_zip_links()
        self.scraper.download_zip_to_folder(filename_url_tuples)

    def process(self): 
        self.processor = Processor(self.config.folder, self.config.country)
        self.processor.extract_zip_files()
        self.locationsData = self.processor.combine_data()
    
    
    def save_to_repo(self):
        self.repo = Repository(self.config.configuration)
        for ld in self.locationsData:
            db = self.repo.connect()
            self.repo.create(db, ld)
            self.repo.close_session(db)
            
    def run(self):
        self.scrape()
        self.process()
        FileFinder.cleanup_files(self.config.folder, ".zip")
        FileFinder.cleanup_files(self.config.folder, ".XLS")
        self.save_to_repo()
        
    async def run_async(self):
        self.run()

