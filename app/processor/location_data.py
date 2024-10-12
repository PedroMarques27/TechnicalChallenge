class LocationData:
    def __init__(self, location, region, value):
        self.location = location
        self.region = region
        self.value = value

    def __repr__(self):
        return f"LocationData(location='{self.location}',region='{self.region}', value={self.value})"
    
    @staticmethod
    def get_table_definition():
        return '''
            CREATE TABLE IF NOT EXISTS LocationData (
                Location VARCHAR(50) NOT NULL,
                Region_Code VARCHAR(50) NOT NULL,
                Value VARCHAR(100),
                PRIMARY KEY (Location, Region_Code)
            );
        '''
