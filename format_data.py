import pandas as pd

# Load the dataset
df = pd.read_csv('email.csv', sep=';', encoding='latin1')

# Inspect the dataset (optional, for debugging)
print("Dataset Info:")
print(df.info())
print("\nFirst Few Rows:")
print(df.head())

# Standardize column names (remove special characters, spaces, parentheses)
df.columns = [col.strip().replace(' ', '_').replace('(', '').replace(')', '') for col in df.columns]

# Handle missing values (replace NaN with empty strings)
df = df.fillna('')

# Save the cleaned dataset to a new CSV file with commas as delimiters
output_file = 'email_Transformed.csv'
df.to_csv(output_file, sep=',', index=False, encoding='utf-8')

print(f"\nTransformed dataset saved as: {output_file}")
