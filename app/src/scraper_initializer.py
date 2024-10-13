from app.src.services.scraper import Scraper
from app.src.services.data_processor import Processor
from app.src.repository import Repository
from app.src.services.file_finder import FileFinder
class ScraperInitializer:
    def __init__(self):
        self.folder = "Archives"
        self.url = "https://ftp.ibge.gov.br/Censos/Censo_Demografico_1991/Indice_de_Gini/"
        self.country = "Brasil"
        self.configuration = {
            "host": "localhost",
            "user":"user",
            "password":"root",
            "database": "technicalchallenge",
            "table_name":"locationData"
        }
        
    def scrape(self):
        self.scraper = Scraper(self.url , self.folder)
        filename_url_tuples = self.scraper.scrape_zip_links()
        self.scraper.download_zip_to_folder(filename_url_tuples)

    def process(self): 
        print("1")
        self.processor = Processor(self.folder, self.country)
        print("2")
        self.processor.extract_zip_files()
        print("3")
        self.locationsData = self.processor.combine_data()
    
    
    def save_to_repo(self):
        self.repo = Repository(self.configuration)
        
        for ld in self.locationsData:
            db = self.repo.connect()
            self.repo.create(db, ld)
            self.repo.close_session(db)
            
    async def run(self):
        self.scrape()
        print("Scraped")
        self.process()
        print("process")
        FileFinder.cleanup_files(self.folder, ".zip")
        print("cleanup_zip_files")
        FileFinder.cleanup_files(self.folder, ".XLS")
        print("cleanup_xls_files")
        self.save_to_repo()
        