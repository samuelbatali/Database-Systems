"""
        File Formats Conversions
        ------------------------
        
   Python functions for reading data from CSV, JSON, and XML files
   And can convert data read from one file format to another.
   
   The read string/datacan be retrieved for use in a program 
   or it can be saved to a file CSV, JSON, or XML file

  @uthor: Samuel Batali
  Year:   2020
"""
import csv
import json
import xml.etree.ElementTree as ET


def read_csv_string(input_):
    """
    Takes a string which is the contents of a CSV file.
    Returns an object (dict) containing the data from the file.
    """
    data = csv.DictReader(input_.splitlines())
    # return dict key = column name, value = list(column data)
    return [dict(row) for row in data]


def write_csv_string(data):
    """
    Takes a data object (created by one of the read_*_string functions).
    Returns a string in the CSV format.
    """
    
    keys = data[0].keys()
    result = ','.join(keys)
    result += '\n'
    
    # Didn't find a way of convertng to csv
    # using the csv module
    
    # So I be doing it manually
    
    for row in data:
        subList = []
        for key in keys:
            subList.append( row[key] )
            
        result += ','.join(subList)
        result += '\n'
        
    return result


def read_json_string(input_):
    """
    Similar to read_csv_string, except works for JSON files.
    """
    return json.loads(input_)


def write_json_string(data):
    """
    Writes JSON strings. Similar to write_csv_string.
    """
    # No sweat –– straight from the documentation
    # data is list of dicts btw
    return json.dumps(data)


def read_xml_string(input_):
    """
    Similar to read_csv_string, except works for XML files.
    """
    data =  ET.fromstring(input_)
    result = []
    
    
    for child in data:
        subDict = {}
        for subChild in list(child):
            subDict[subChild.tag] = subChild.text
        result.append(subDict)
        
    # Reconstructed a list of dictionaries 
    # dicts = child attributes with no children
    return result


def write_xml_string(data):
    """
    Feel free to write what you want here.
    """
    
    root = ET.Element("data")
    
    # More like appending Nodes in Graphs
    # I bet this module is implemented using Graph DS
    
    keys = data[0].keys()
    for row in data:
        child = ET.Element("record")
        for key in keys:
            subChild = ET.Element(key)
            subChild.text = row[key]
            child.append(subChild)
    
        root.append(child)
    
    # ET.tostring(root) -- Apparently returns a byte string
    # Found a way to decode a byte string to string from stactOverflow
    return ET.tostring(root).decode("utf-8") 