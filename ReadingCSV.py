import pandas as pd
from pymongo import MongoClient
import certifi

def main():
    # connect to mongodb instance
    client = MongoClient("mongodb+srv://Kunal:Kunal2020@cluster1.3pjbhfu.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
    # find database
    db = client['cluster1']
    # creating a collection
    collection = db['data']
    # get entire data frame from csv
    df = pd.read_csv('/Users/kunal/Documents/Internship/Data.csv')
    # convert csv to dictionary
    dictionary = df.to_dict(orient = 'records')
    # add entire dictionary to collection
    collection.insert_many(dictionary)
    # add new field to collection: call it 'category'
    collection.update_many({}, {'$set': {"Category:": ""}})
    # iterate through each record, and ask the user what its category is
    for record in collection.find({}):
        category = input("What is " + record['Name'] + "'s category?")
        # assign the record the category the user gave it
        
    

if __name__ == "__main__":
    main()