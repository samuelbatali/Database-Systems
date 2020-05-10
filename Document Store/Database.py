import json
from Collection import Collection

class Database():
    """
    A NoSQL database for storing collections
    JSON file is used for storing data to ensure persistency
    """
    def __init__(self, filename):
        # The db file name (If file exist must be JSON)
        self.db_file = filename
        # Storing collections: key = collection name, value = collection object
        self.collections = {}
        
        # If file doesn't exist, then this is a new database creation
        self.read_json_file(filename)
        
    def check_collection(self, name):
        """
        Check if collection with the given name exist in DB
        """
        return name in self.collections
        
    def get_collection(self, name, or_create=False):
        """
        Return pointer to a collection with the provided name
        Create collection if don't exist
        """
        if name not in self.collections:
            self.collections[name] = Collection()
        
        return self.collections[name]
    
    
    def get_collections(self):
        """
        Return names of all collections in this database
        Which are keys for the self.collections
        """
        return self.collections.keys()
    
    def drop_collection(self, name):
        """
        Delete a whole collection from the database
        """
        if name in self.collections:
            del self.collections[name]
    
    def read_json_file(self, filename):
        """
        If database already exist, read the data from the db file (JSON)
        and store the results in self.collections
        """
        try:
            with open(filename,"r") as json_file:
                for name, data in json.load(json_file).items():
                    collection = self.get_collection(name)
                    collection.collection = data
        except:
            pass # Do nothing file doesn't exist
            # Will craete file and store data when closing the connection
        
    def write_json_file(self, filename):
        """
        Write the content of the database (self.collections) to a JSON file
        Create one if doen't exist
        """
        # Prepare data to be written in JSON file
        prepare_data = {}
        for name in self.collections:
            prepare_data[name] = self.collections[name].collection
        # Write the data
        with open(filename,mode="w") as json_file:
            json_file.truncate(0)
            json.dump(prepare_data, json_file)
            
    def close(self):
        """
        When closing the database, you must write current data to the JSON file
        for persistence
        """
        self.write_json_file(self.db_file)
    
if __name__ == "__main__":
    db = Database("file1")
    collection = db.get_collection("people")
    
    # Empty collection
    collection = Collection()
    assert collection.get_all() == []
    
    document1 = {"name":"John", "age":38, "children": {"child1":"James", "child2":"Jay"}}
    # First insertion
    collection.insert(document1)
    assert collection.get_all() == [document1]
    
    