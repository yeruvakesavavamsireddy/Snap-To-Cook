import os
import numpy as np
import pandas as pd
from PIL import Image

from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.models import Model


# -----------------------------------
# PROJECT PATHS
# -----------------------------------

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

CSV_PATH = os.path.join(BASE_DIR, "dataset", "cleaned_recipes.csv")
IMAGE_FOLDER = os.path.join(BASE_DIR, "dataset", "images")

FEATURE_PATH = os.path.join(BASE_DIR, "dataset", "image_features.npy")
FILTERED_CSV_PATH = os.path.join(BASE_DIR, "dataset", "recipes_with_features.csv")


# -----------------------------------
# LOAD DATASET
# -----------------------------------

df = pd.read_csv(CSV_PATH)

print("Total recipes in dataset:", len(df))


# -----------------------------------
# LOAD RESNET50 FEATURE EXTRACTOR
# -----------------------------------

print("Loading ResNet50 model...")

base_model = ResNet50(weights="imagenet")

feature_model = Model(
    inputs=base_model.input,
    outputs=base_model.get_layer("avg_pool").output
)

print("Model loaded.")


# -----------------------------------
# IMAGE FEATURE EXTRACTION FUNCTION
# -----------------------------------

def extract_feature(img_path):

    img = Image.open(img_path).convert("RGB").resize((224, 224))

    x = np.array(img)
    x = np.expand_dims(x, axis=0)

    x = preprocess_input(x)

    feature = feature_model.predict(x, verbose=0)

    feature = feature.flatten()

    # Normalize vector
    feature = feature / np.linalg.norm(feature)

    return feature


# -----------------------------------
# EXTRACT FEATURES FOR DATASET
# -----------------------------------

features = []
valid_rows = []

print("Extracting image features...\n")

for idx, row in df.iterrows():

    image_name = str(row.get("Image_Name", ""))

    base = os.path.splitext(image_name)[0]

    img_path = None

    for ext in [".jpg", ".jpeg", ".png"]:

        path = os.path.join(IMAGE_FOLDER, base + ext)

        if os.path.exists(path):
            img_path = path
            break

    if img_path is None:
        continue

    print("Processing:", base)

    feature = extract_feature(img_path)

    features.append(feature)

    valid_rows.append(idx)


# -----------------------------------
# CONVERT TO NUMPY ARRAY
# -----------------------------------

features = np.array(features)


# -----------------------------------
# STORAGE OPTIMIZATION (float16)
# -----------------------------------

features = features.astype("float16")

print("\nFeature matrix shape:", features.shape)
print("Feature dtype:", features.dtype)


# -----------------------------------
# SAVE FEATURES
# -----------------------------------

np.save(FEATURE_PATH, features)

print("\nSaved features to:", FEATURE_PATH)


# -----------------------------------
# SAVE FILTERED DATASET
# -----------------------------------

df_valid = df.iloc[valid_rows]

df_valid.to_csv(FILTERED_CSV_PATH, index=False)

print("Saved filtered dataset to:", FILTERED_CSV_PATH)


# -----------------------------------
# STORAGE INFO
# -----------------------------------

size_mb = os.path.getsize(FEATURE_PATH) / (1024 * 1024)

print(f"\nFeature file size: {size_mb:.2f} MB")


print("\nFeature extraction complete!")