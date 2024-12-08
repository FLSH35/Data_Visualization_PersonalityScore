import os
import pandas as pd
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Load environment variables from .env file
load_dotenv()

# Get the path to the credentials from the environment variable
cred_path = os.getenv('FIREBASE_ADMIN_CREDENTIALS')
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

def delete_all_questions():
    # Reference to the questions collection
    questions_ref = db.collection('questions')

    # Get all documents in the questions collection
    docs = questions_ref.stream()

    # Delete each document
    for doc in docs:
        questions_ref.document(doc.id).delete()
        print(f"Deleted question set '{doc.id}'.")

def main1():
    delete_all_questions()


import os
import pandas as pd
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def add_question_to_firestore(question):
    # Each question is a separate document in the 'questions' collection
    question_ref = db.collection('questions').add(question)
    print(f"Added question: {question['text']} ")

def main():
    # Read the CSV file with the specified encoding
    df = pd.read_csv('PersonalityScoreFragen(in) (6).csv', sep=',', encoding='latin1')

    # Iterate through the DataFrame and add each question to Firestore
    for _, row in df.iterrows():
        # Create a dictionary for each question
        question_data = {
            'text': row['text'],
            'value': row['value'],
            'relevancy': row['relevancy'],
            'set': row['set'],  # Include the set as a field
            'backgroundInfo': row['backgroundInfo'],  # Include the set as a field
            'id': row['id'],  # Include the set as a field
        }

        # Add the question to Firestore
        add_question_to_firestore(question_data)

if __name__ == "__main__":
    main1()
    main()
