import requests
import os
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self):
        self.url = "https://ftp.ibge.gov.br/Censos/Censo_Demografico_1991/Indice_de_Gini/"
        self.folder = "Archives"
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
            
        
    def scrape_zip_links(self):
        get_request_response = requests.get(self.url)
        soup = BeautifulSoup(get_request_response.content, 'html.parser')
        
        # Return All TD Elements
        cells = [c for row in soup.find_all('tr') for c in row.find_all('td')] 
        
        # Return all Anchors
        for cell in cells:
            if (anchor:= cell.find('a', href = True)) is not None and anchor['href'].endswith('.zip'):
                print(f"Found File {anchor.text}")
                yield (anchor.text, self.url+anchor['href'])
                
       
    def download_zip_to_folder(self, anchors):
        for filename, url  in anchors:
            file_path = os.path.join(self.folder, filename)
            response = requests.get(url)
            
            if response.status_code == 200:
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                print(f"File Saved {filename}")
            else:
                print(f"Failed To Save {filename}")
                    
    
    
        
    