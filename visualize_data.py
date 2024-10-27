import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np
from textwrap import wrap

# Load data
questions_df = pd.read_csv('PersonalityScoreFragen(Fragen) (16).csv', sep=';', encoding='latin1')
with open("users_collection.json", "r") as f:
    users_data = json.load(f)

# Filter for 'Kompetenz' set questions
kompetenz_questions_df = questions_df[questions_df['set'] == 'Kompetenz']
if kompetenz_questions_df.empty:
    print("No questions found in 'Kompetenz' set.")
else:
    print(f"Total questions in 'Kompetenz' set: {len(kompetenz_questions_df)}")

# Initialize data storage
kompetenz_scores = {}
kompetenz_question_scores = {q['text']: [] for _, q in kompetenz_questions_df.iterrows()}
character_counts = {}

# Process user data for 'Kompetenz' set
for user_id, user_info in users_data.items():
    if "subcollections" in user_info and "results" in user_info["subcollections"]:
        for result in user_info["subcollections"]["results"]:
            # Count finalCharacter occurrences
            if "finalCharacter" in result:
                char_name = result["finalCharacter"]
                if char_name:  # Ensure char_name is not None
                    character_counts[char_name] = character_counts.get(char_name, 0) + 1

            # Capture 'Kompetenz' set scores if completed
            if result.get("set") == 'Kompetenz' and result.get("isCompleted"):
                total_score = result.get("totalScore", 0)
                kompetenz_scores[user_info["displayName"]] = total_score

                for idx, score in enumerate(result["answers"]):
                    if score is not None and idx < len(kompetenz_questions_df):
                        question_text = kompetenz_questions_df.iloc[idx]['text']
                        kompetenz_question_scores[question_text].append(score)

# Visualization 1: Final Character Count
plt.figure(figsize=(10, 6))
plt.bar(character_counts.keys(), character_counts.values(), color='skyblue')
plt.title("Final Character Counts")
plt.xlabel("Character Type")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.show()

# Visualization 2: Total Score for Each User in 'Kompetenz' Set
plt.figure(figsize=(10, 6))
plt.bar(kompetenz_scores.keys(), kompetenz_scores.values(), color='skyblue')
plt.title("Total Score for Each User in 'Kompetenz' Set")
plt.xlabel("User Display Name")
plt.ylabel("Total Score")
plt.xticks(rotation=45)
plt.show()

# Calculate average scores per question in 'Kompetenz' set and sort
avg_kompetenz_question_scores = {q: np.mean(scores) for q, scores in kompetenz_question_scores.items() if scores}
sorted_kompetenz_questions = sorted(avg_kompetenz_question_scores.items(), key=lambda x: x[1])
lowest_kompetenz_questions = sorted_kompetenz_questions[:5]
highest_kompetenz_questions = sorted_kompetenz_questions[-5:]

# Visualization 3: Lowest Ranked Questions in 'Kompetenz' Set
plt.figure(figsize=(12, 8))
plt.barh([wrap(q[0], 50) for q in lowest_kompetenz_questions], [q[1] for q in lowest_kompetenz_questions], color='salmon')
plt.title("Lowest Ranked Questions (Kompetenz Set Only)")
plt.xlabel("Average Score")
plt.show()

# Visualization 4: Highest Ranked Questions in 'Kompetenz' Set
plt.figure(figsize=(12, 8))
plt.barh([wrap(q[0], 50) for q in highest_kompetenz_questions], [q[1] for q in highest_kompetenz_questions], color='lightgreen')
plt.title("Highest Ranked Questions (Kompetenz Set Only)")
plt.xlabel("Average Score")
plt.show()
