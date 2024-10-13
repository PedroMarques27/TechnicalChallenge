import os

class FileFinder:
    @staticmethod
    def find_files_extension( folder, extension):
        return [(f"{folder}/{f}", f) for f in os.listdir(folder) if f.endswith(extension)]
    
    @staticmethod
    def cleanup_files(folder, extension):
        [os.remove(f"{folder}/{f}") for f in os.listdir(folder) if f.endswith(extension)]