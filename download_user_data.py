import os
import json
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1._helpers import DatetimeWithNanoseconds

# Load environment variables from .env file
load_dotenv()

# Get the path to the credentials from the environment variable
cred_path = os.getenv('FIREBASE_ADMIN_CREDENTIALS')
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

def serialize_data(data):
    """Convert Firestore data to a JSON-serializable format."""
    if isinstance(data, DatetimeWithNanoseconds):
        return data.isoformat()  # Convert timestamps to ISO 8601 strings
    elif isinstance(data, dict):
        return {k: serialize_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [serialize_data(i) for i in data]
    else:
        return data

def get_subcollections(doc_ref):
    subcollections = {}
    for subcollection_ref in doc_ref.collections():
        print(f"  Fetching sub-collection: {subcollection_ref.id}")
        subcollection_data = []
        for sub_doc in subcollection_ref.stream():
            sub_data = serialize_data(sub_doc.to_dict())
            sub_data['id'] = sub_doc.id  # Include the document ID
            print(f"    Retrieved sub-document ID: {sub_doc.id}")
            subcollection_data.append(sub_data)
        subcollections[subcollection_ref.id] = subcollection_data
    return subcollections

def download_users_as_json():
    # Reference to the users collection
    users_ref = db.collection('users')
    
    # Get all documents in the users collection
    docs = users_ref.stream()
    
    # Initialize a dictionary to hold all user data
    users_data = {}
    
    # Loop through each document and print progress
    for doc in docs:
        user_data = serialize_data(doc.to_dict())
        user_data['id'] = doc.id  # Include document ID if needed
        print(f"Downloading user document ID: {doc.id}")
        
        # Fetch all sub-collections of the user
        user_data['subcollections'] = get_subcollections(doc.reference)
        
        # Add the user data to the dictionary
        users_data[doc.id] = user_data
    
    # Save the users data to a JSON file
    with open('users_collection.json', 'w') as json_file:
        json.dump(users_data, json_file, indent=4)
    
    print("Downloaded users collection as 'users_collection.json'.")

if __name__ == "__main__":
    download_users_as_json()
