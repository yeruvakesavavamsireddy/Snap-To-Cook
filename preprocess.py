import pandas as pd
import os

df = pd.read_csv("dataset/recipes.csv")

print("Columns:", df.columns)

# Use correct columns
df["Cleaned_Ingredients"] = df["Cleaned_Ingredients"].astype(str).str.lower()
df["Instructions"] = df["Instructions"].astype(str).str.lower()
df["Title"] = df["Title"].astype(str).str.lower()

# Save cleaned dataset
os.makedirs("dataset", exist_ok=True)
df.to_csv("dataset/cleaned_recipes.csv", index=False)

print("Preprocessing completed successfully")
