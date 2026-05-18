import pandas as pd
import pickle
import os
from tensorflow.keras.preprocessing.text import Tokenizer

df = pd.read_csv("dataset/cleaned_recipes.csv")

df["Cleaned_Ingredients"] = df["Cleaned_Ingredients"].fillna("").astype(str)
df["Instructions"] = df["Instructions"].fillna("").astype(str)

# Create tokenizer folder
os.makedirs("tokenizer", exist_ok=True)

# ---------------- INGREDIENTS TOKENIZER ----------------
ingredients_tokenizer = Tokenizer(num_words=5000, oov_token="<OOV>")
ingredients_tokenizer.fit_on_texts(df["Cleaned_Ingredients"])

with open("tokenizer/ingredients_tokenizer.pkl", "wb") as f:
    pickle.dump(ingredients_tokenizer, f)

# ---------------- INSTRUCTIONS TOKENIZER ----------------
instructions_tokenizer = Tokenizer(num_words=8000, oov_token="<OOV>")
instructions_tokenizer.fit_on_texts(df["Instructions"])

with open("tokenizer/instructions_tokenizer.pkl", "wb") as f:
    pickle.dump(instructions_tokenizer, f)

print("Tokenizers created successfully")
