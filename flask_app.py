import flask
import pandas as pd
import pymongo 
import certifi

# Create the application.
APP = flask.Flask(__name__)

# No database right now
db = None
# No collection right now
collection = None
# Holds ALL the UNIQUE entries from the CSV
unique_entries = None
# Number of unique entries
numEntries = -1
# Display 20 records at a time
DISPLAY_ENTRIES = 10
# Our current entry offset is 0
curEntry = 0
# Very first time we initalize database/collection
firstTime = True


@APP.route('/')
def index():
    """ Displays the index page accessible at '/'
    """
    return flask.render_template('home.html')


# Preliminary setup stuff for mongoDB (connects to database, creates empty collection)
def mongo_connect():
    # connect to mongodb instance
    client = pymongo.MongoClient("mongodb+srv://Kunal:Kunal2020@cluster1.3pjbhfu.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
    # find the database
    global db
    # initialize the global variable which holds the database
    db = client['cluster1']
    # Now, let's create a collection
    global collection
    collection = db['kunal_data']
    # wipe the entire collection, in case anything existed in it before
    # collection.delete_many({})

# Upload the csv the user selected to mongoDB
@APP.route("/upload_data", methods=['POST'])
def upload_data():
    # Grab the data (json) from the ajax call
    json = flask.request.get_json()
    # Before we begin, let's connect to the mongoDB database, only if it's our
    # first time
    global firstTime
    if firstTime:
        mongo_connect()
        collection.delete_many({})
        firstTime = False
    # put the JSON into the collection
    collection.insert_many(json)
    # add new field to collection: call it 'category'
    collection.update_many({}, {'$set': {"Business Type": ""}})
    # Grab all UNIQUE entries in the collection
    inter = pd.DataFrame(list(collection.aggregate([
    # Removes the id field
    {"$unset" : ["_id"]},
    # Finds all the UNIQUE entries and keeps them as documents
    {"$group" : { 
        "_id" : "$Name", 
        "doc" : { "$first": "$$ROOT" }}},
    {"$replaceRoot" : {
        "newRoot" : "$doc"}}
    ])))
    # If unique_entries is already defined, we only want to add the NEW unique
    # entries from the query to unique_entries
    # If it is not defined, the entire query is new
    global unique_entries
    # Check if unique_entries is defined
    if unique_entries is not None:
        # Iterate through inter
        for index in inter.index:
            # Check if the transaction name in inter is already in unique_entries
            if inter['Name'][index] in unique_entries.values:
                # Looks like it is, let's remove it from inter
                inter.drop(axis = 0, labels = index, inplace= True)
    # Concatenate the rest of the entries in inter with unique_entries
    unique_entries = pd.concat([unique_entries, inter], ignore_index = True, sort = False)
    # Move Business_Type to the last column in case it got shifted
    last_column = unique_entries.pop('Business Type')
    unique_entries.insert(unique_entries.shape[1], 'Business Type', last_column)
    
    # Set the number of unique entries
    global numEntries
    numEntries = unique_entries.shape[0]
    # Return number of unique entries back to frontend as a string
    return str(numEntries)

@APP.route("/getEntries", methods=['POST', 'GET'])
def getEntries():
    # Get the direction the cursor needs to move in from the AJAX call
    dir = flask.request.get_json()["direction"]
    global curEntry
    # Update curEntry
    curEntry += dir * DISPLAY_ENTRIES
    # Wrap around if we need to
    if curEntry < 0:
        curEntry = numEntries - (numEntries % DISPLAY_ENTRIES)
    elif curEntry > numEntries:
        curEntry = 0
    # We need DISPLAY_ENTRIES entries starting from curEntry
    df = unique_entries.loc[curEntry : min(curEntry + DISPLAY_ENTRIES - 1, numEntries)]
    # Format to JSON
    json = df.to_json(orient='records')
    # Give the JSON to the frontend to display
    return json

@APP.route("/saveCategories", methods=['POST', 'GET'])
def saveCategories():
    # Get the data from the AJAX call
    data = flask.request.get_json()
    # Let's classify each transaction in the collection with this JSON 
    for transaction in data:
        # Get name of transaction
        name = transaction["Transaction"]
        # Get category of transaction
        category = transaction["Business_Type"]
        # Create query
        query = {"Name" : name}
        newValue = {"$set" : {"Business Type" : category}}
        # Update the category field in mongoDB for ALL instances of this name
        collection.update_many(query, newValue)
    return "PAGE SAVED!"

if __name__ == '__main__':
    APP.debug=True
    APP.run()