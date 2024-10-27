import pandas as pd
import json

# Load data
with open("users_collection.json", "r") as f:
    users_data = json.load(f)

# Define the datasets and columns
datasets = ["BewussteInkompetenz", "Kompetenz", "Individual", "LifeArtist", "Reacher", "Resident", "BewussteKompetenz"]
columns = ["user_id", "displayName", "finalCharacter", "combinedTotalScore"] + [f"{dataset}_totalScore" for dataset in datasets]

# Initialize list to store each user's data row
user_data_rows = []

# Process each user and capture scores
for user_id, user_info in users_data.items():
    # Initialize dictionary to hold row data for this user
    user_row = {col: None for col in columns}
    user_row["user_id"] = user_id
    user_row["displayName"] = user_info.get("displayName", "Unknown")
    
    # Process each result in the user's subcollections
    for result in user_info.get("subcollections", {}).get("results", []):
        set_name = result.get("set")
        total_score = result.get("totalScore")
        
        # Capture total scores for each dataset if available
        if set_name in datasets:
            user_row[f"{set_name}_totalScore"] = total_score

        # Capture finalCharacter and combinedTotalScore if present
        if result.get("id") == "finalCharacter":
            user_row["finalCharacter"] = result.get("finalCharacter")
            user_row["combinedTotalScore"] = result.get("combinedTotalScore")

    # Add the user's row to the list
    user_data_rows.append(user_row)

# Convert to DataFrame and save to CSV
output_df = pd.DataFrame(user_data_rows, columns=columns)
output_df.to_csv("user_total_scores.csv", index=False)
print("CSV file 'user_total_scores.csv' created successfully.")
