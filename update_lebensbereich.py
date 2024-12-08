import pandas as pd
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Lebensbereiche-Kürzel Zuordnung (mit Unterkategorien für Persönlichkeitsentwicklung)
lebensbereiche_mapping = {
    "Gesundheit": "GesundheitWohlbefinden",
    "Karriere": "BerufKarriere",
    "Finanzen": "Finanzen",
    "Familie": "FamilieBeziehungen",
    "Selbstreflexion": "Selbstreflexion",
    "Zielsetzung": "ZieleMotivation",
    "Stressmanagement": "ZeitStressMgmt",
    "Produktivität": "Produktivität",
    "Weiterbildung": "LernenWeiterbildung",
    "Resilienz": "ResilienzStärke",
    "Kommunikation": "KommunikationSozFähig",
    "Selbstfürsorge": "Selbstfürsorge",
    "Kreativität": "KreativitätAusdruck",
    "Lebensplanung": "Lebensplanung",
    "Freizeit": "FreizeitErholung",
    "Spiritualität": "SpiritualitätSinn",
    "Umwelt": "UmgebungLebensstil",
    "Gemeinschaft": "GemeinschaftEngagement"
}

# Function to call the OpenAI model
def classify_lifesphere(prompt_text):
    """
    Classifies the life area of a given sentence.

    Parameters:
    - prompt_text (str): The text to classify.

    Returns:
    - str: The corresponding life area or Kürzel.
    """
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    messages = [
        (
            "system",
            "Analysiere den folgenden Satz und ordne ihn einem der Lebensbereiche zu: "
            "Gesundheit, Karriere, Finanzen, Familie, Selbstreflexion, Zielsetzung, Stressmanagement, "
            "Produktivität, Weiterbildung, Resilienz, Kommunikation, Selbstfürsorge, Kreativität, "
            "Lebensplanung, Freizeit, Spiritualität, Umwelt oder Gemeinschaft. "
            "Gib nur den Namen des Lebensbereichs oder der Unterkategorie zurück."
        ),
        ("human", prompt_text),
    ]

    ai_msg = llm.invoke(messages)
    return ai_msg.content.strip()

# File paths
input_file = 'PersonalityScoreFragen(in) (3).csv'
output_file = 'PersonalityScoreFragen_Updated.csv'

# Read the CSV file
df = pd.read_csv(input_file, sep=';', encoding='latin1')

# Add Lebensbereiche column if not already present
if 'Lebensbereiche' not in df.columns:
    df['Lebensbereiche'] = ''

# Ensure output file exists and write the header if it's empty
if not os.path.exists(output_file) or os.stat(output_file).st_size == 0:
    df.head(0).to_csv(output_file, sep=';', index=False, encoding='latin1')  # Write header only

# Process rows and save after each update
for index, row in df.iterrows():
    if pd.isna(row['Lebensbereiche']) or row['Lebensbereiche'] == '':
        print(f"Processing row {index}: {row['text']}")
        lebensbereich = classify_lifesphere(row['text'])
        kürzel = lebensbereiche_mapping.get(lebensbereich, "Unbekannt")
        df.at[index, 'Lebensbereiche'] = kürzel
        print(f"Assigned Lebensbereich: {lebensbereich} -> {kürzel}")
        
        # Save the updated row to the file immediately
        df.iloc[[index]].to_csv(output_file, sep=';', index=False, mode='a', header=False, encoding='latin1')
        print(f"Row {index} saved to '{output_file}'.")

print(f"Processing completed. Updated file saved as '{output_file}'.")
