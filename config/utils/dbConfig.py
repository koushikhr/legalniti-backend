import pymongo

def createDbInstance():
    # Define your MongoDB connection settings
    mongo_uri = "mongodb+srv://legalniti6690:KwsOCH4aTnVJ4PAe@legalniti-ai.m6mfcwk.mongodb.net/?retryWrites=true&w=majority"
    client = pymongo.MongoClient(mongo_uri)
    database = client["lnai-platform-db"]  # Replace with your database name

    return database

def getUsersCollection():
    db = createDbInstance()
    collection = db["users-collection"]  # Replace with the name of your first collection
    return collection

def getRelationsCollection():
    db = createDbInstance()
    collection = db["relations-collection"]  # Replace with the name of your second collection
    return collection

def export_collections():
    collection1 = getUsersCollection()
    collection2 = getRelationsCollection()

    # Add code here to perform any desired operations on the collections
    # For example, you can query data, insert documents, update, or delete as needed.

    # Then, return or process the data as required.

if __name__ == "__main__":
    export_collections()
