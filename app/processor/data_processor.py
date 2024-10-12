import zipfile
import os 
import pandas as pd
from location_data import LocationData

class Processor:
    def __init__(self, folder, origin_country = "brasil"):
        current_path = os.getcwd()
        self.folder = os.path.join(current_path, folder)
        self.unique_location_data = set()
        self.country = origin_country.lower()
    
    def extract_zip_files(self):
        zip_files = [f"{self.folder}/{f}" for f in os.listdir(self.folder) if f.endswith('.zip')]
        for zf in zip_files:
            with zipfile.ZipFile(zf, 'r') as zf_reader:
                zf_reader.extractall(self.folder)
            
    def combine_data(self):
        self.location_mappings = {}
        for file in [f for f in os.listdir(self.folder) if f.endswith('.XLS')]:
            dataset = pd.read_excel(f"{self.folder}/{file}", engine="xlrd")
            available_rows = [row for index, row in dataset.dropna().iterrows() if row.shape[0] == 2]
           
            region_code = file.replace('GINI91', '').replace('.XLS', '')
            
            for key, value in available_rows:
                location_data = LocationData(self.country, self.country, value)
                if self.country in key.lower():
                    continue
                else:
                    location_data.region_code = region_code
                    location_data.location = key.lower().strip()
                
                self.unique_location_data.add(location_data)
        return self.unique_location_data
    
    
    def cleanup_files(self, extension):
        [os.remove(f"{self.folder}/{f}") for f in os.listdir(self.folder) if f.endswith(extension)]
        
              

