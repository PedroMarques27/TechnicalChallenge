import requests
import os
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, scraping_url, folder):
        self.url = scraping_url
        self.folder = folder
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
            self.available_zips = []
        else:
            self.available_zips = [f for f in os.listdir(self.folder) if f.endswith('.zip')]
            
        
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
        filtered_anchors = [(filename,url) for (filename,url) in anchors if filename not in self.available_zips]
        for filename, url  in filtered_anchors:
            file_path = os.path.join(self.folder, filename)
            response = requests.get(url)
            
            if response.status_code == 200:
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                print(f"File Saved {filename}")
            else:
                print(f"Failed To Save {filename}")
                
        