import pandas as pd
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Function to call the OpenAI model
def openai_prompt(prompt_text):
    """
    Sends a prompt to the OpenAI GPT model and retrieves the generated response.

    Parameters:
    - prompt_text (str): The text prompt to be sent to the OpenAI model.

    Returns:
    - str: The content of the response generated by the OpenAI model.
    """
    # Instantiate the OpenAI model object
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    # Define the messages for the OpenAI call
    messages = [
        (
            "system",
            "Erkläre den Satz so, dass er in zwei Sätzen eine spezifische Beispielsituation beschreibt, als würde sie immer so in dem Leben der Person passieren. Die Beispielsituation sollte zeigen, wie sich die Person mit dem Thema identifizieren könnte. Der Fokus liegt auf Persönlichkeitsentwicklung in verschiedenen Lebensbereichen. Mit der Situation sollte die Person sich selbst identifizieren können, deswegen sprichst du sie mit 'du' an. Mache klar, dass es sich um ein Beispiel zum besseren Verständnis des Satzes handelt."
        ),
        ("human", prompt_text),
    ]

    # Invoke the OpenAI model with the messages
    ai_msg = llm.invoke(messages)

    # Return the content of the response
    return ai_msg.content

# File paths
input_file = 'PersonalityScoreFragen(in) (3).csv'
output_file = 'PersonalityScoreFragen_Updated.csv'

# Read the CSV file using pandas
df = pd.read_csv(input_file, sep=';', encoding='latin1')

# Ensure the output file exists, and write the header if it is empty
if not os.path.exists(output_file) or os.stat(output_file).st_size == 0:
    with open(output_file, 'w', encoding='latin1') as f:
        df.head(0).to_csv(f, sep=';', index=False)  # Write header only

# Process rows where 'backgroundInfo' is empty
for index, row in df.iterrows():
    if row['backgroundInfo'] == 'empty':
        print(f"Found empty 'backgroundInfo' for text: {row['text']}")
        explanation = openai_prompt(row['text'])
        print(f"Generated explanation: {explanation}")

        # Append the updated row to the output file
        updated_row = row.copy()
        updated_row['backgroundInfo'] = explanation
        updated_row.to_frame().T.to_csv(output_file, sep=';', index=False, mode='a', header=False, encoding='latin1')

        print(f"Row {index} appended to '{output_file}'.")

print(f"Processing completed. Updated file saved as '{output_file}'.")