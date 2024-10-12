import mysql.connector 
from location_data import LocationData
class Repository:
    
    def __init__(self, configuration):
        self.db_configuration = configuration
        self.table_query = LocationData.get_table_definition()
    
    def connect(self):
        self.db = mysql.connector.connect(
                    host=self.db_configuration["host"],
                    user= self.db_configuration["user"],
                    password=self.db_configuration["password"],
                    database = self.db_configuration["database"]
                    ) 
    def generate_schema(self):
        mycursor = self.db.cursor()
        mycursor.execute("SHOW Tables")
        if self.db_configuration["table_name"] not in mycursor:
            mycursor.execute(self.table_query)
    
    def insert(self, locationData):
        cursor = self.db.cursor()
        try: 
            sql = f"INSERT INTO LocationData (location, region_code, value) VALUES (%s, %s, %s)"
            cursor.execute(sql, (locationData.location, locationData.region_code, locationData.value))
            self.db.commit()
        except Exception as e:
            print("Error inserting Data into LocationData: ", e)
            
        
        
        