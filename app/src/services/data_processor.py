import zipfile
import os 
import pandas as pd
from app.src.services.file_finder import FileFinder
from app.src.models import LocationData

class Processor:
    def __init__(self, folder, origin_country):
        current_path = os.getcwd()
        self.folder = os.path.join(current_path, folder)
        self.unique_location_data = set()
        self.country = origin_country.lower()
        self.regions = {}
    
    def extract_zip_files(self):
        for zf, filename in FileFinder.find_files_extension(self.folder, '.zip'):
            with zipfile.ZipFile(zf, 'r') as zf_reader:
                zip_contents = zf_reader.namelist()
                xls_file = [file for file in zip_contents if file.endswith('.XLS')][0]
                region_code = xls_file.replace('GINI91','').split(".")[0]
                self.regions[region_code] = filename.split(".")[0].replace("_", " ").lower()
                zf_reader.extractall(self.folder)
            
    def combine_data(self):
        for file, filename in FileFinder.find_files_extension(self.folder, '.XLS'):
            dataset = pd.read_excel(file, engine="xlrd")
            available_rows = [row for _, row in dataset.dropna().iterrows() if row.shape[0] == 2]
            
            for key, value in available_rows:
                location_data = LocationData.retrieve_location_from_row(key, value, self.country, self.regions)    
                self.unique_location_data.add(location_data)
            print(self.regions)
       
        return self.unique_location_data
    
    
        
              

