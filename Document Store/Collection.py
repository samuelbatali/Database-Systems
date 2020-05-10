class Collection():
    """
    A collection of documents
    Documents are in dictionary format
    """
    def __init__(self):
        
        # Store list of documents (dicts)
        self.collection = []
        
    def insert(self, document):
        """
        Adds a new document to the collection
        """
        self.collection.append(document)
        
    def find(self, where_dict):
        """
        Return all documents in the collection that matches the where clause (where_dict)
        """
        def checker(document):
            return self.check_document(document, where_dict)
        return list(filter(checker, self.collection))
            
    def find_one(self, where_dict):
        """
        Return only one document that matches the where clause (where_dict)
        in the collection
        """
        result = self.find(where_dict)
        return result[0] if result else None
        
    def get_all(self):
        """
        Return all documents in the collection
        """
        return self.collection
    
    def count(self, where_dict={}):
        """
        Return the total number of documents present in the collection
        That Matches the where clause (Return count of all if not where clause provided)
        """
        return len(self.find(where_dict))
    
    def update(self, where_dict, changes_dict):
        """
        Apply the changes to documents that matches the where clause
        """
        def updater(document):
            # If document matches where clause, update
            if self.check_document(document, where_dict):
                document.update(changes_dict)
            return document
                    
        self.collection = list(map(updater, self.collection))
    
    def delete(self, where_dict):
        """
        Delete all documents that matches the where clause (where_dict)
        in the collection
        """
        def checker(document):
            return not self.check_document(document, where_dict)
        self.collection = list(filter(checker, self.collection))
    
    def delete_all(self):
        """
        Delete all documents in this collection
        """
        self.collection = []
        
    def check_document(self, document, where_dict):
        """
        Checking Where Clause
        """
        def more_check(item):
            if type(item[1]) is dict and item[0] in document:
                if type(document[item[0]]) is dict:
                    return all( itm in document[item[0]].items() or more_check(itm)
                               for itm in item[1].items())
            return False
        # return True element in where clause is in document
        return all( item in document.items() or more_check(item)
                   for item in where_dict.items())
    
    ########### Working with external functions ################
        
    def map_func(self, map_function):
        """
        Applying external map function to documents
        """
        return list(map(map_function, self.collection))
    
    def reduce_func(self, reduce_function):
        """
        Applying external reduce function to documents
        """
        return reduce_function(self.collection)
        
    def map_reduce(self, map_function, reduce_function):
        """
        Applying external map and reduce functions to documents
        """
        return reduce_function(list(map(map_function, self.collection)))
    
    
if __name__ == "__main__":
    document1 = {"name":"John", "age":38, "children": {"child1":"James", "child2":"Jay"}}
    document2 = {"name":"Doe", "age":17, "children": "None"}
    document3 = {"name":"Mary", "age":55, "children": "Jay"}
    
    # Empty collection
    collection = Collection()
    assert collection.get_all() == []
    
    # First insertion
    collection.insert(document1)
    assert collection.get_all() == [document1]
    
    # Order of insertion
    collection.insert(document2)
    collection.insert(document3)
    assert collection.get_all() == [document1, document2, document3]
    
    # find
    assert collection.find({"name":"Doe"}) == [document2]
    assert collection.find({}) == [document1, document2, document3]
    
    # Nested documents
    assert collection.find({"children":{"child2":"Jay"}}) == [document1]
    assert collection.find({"children":{"child2":"Jay"}, "age":0}) == []
    
    # multiple creteria
    assert collection.find({"children":{"child2":"Jay"}, "age":38}) == [document1]
    
    # Find one
    assert collection.find_one({"children":{"child2":"Jay"}, "age":38}) == document1
    assert collection.find_one({"children":{"child2":"Jay"}, "age":0}) == None
    
    # Count
    assert collection.count() == 3
    assert collection.count({"name":"Doe"}) == 1
    
    # Test for all other functions continues
    
    
    