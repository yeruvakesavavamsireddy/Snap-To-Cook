import os
import ast
import numpy as np
import pandas as pd
from PIL import Image

from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.models import Model


# --------------------------------
# PATHS
# --------------------------------

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

CSV_PATH = os.path.join(BASE_DIR, "dataset", "recipes_with_features.csv")
FEATURE_PATH = os.path.join(BASE_DIR, "dataset", "image_features.npy")
IMAGE_FOLDER = os.path.join(BASE_DIR, "dataset", "images")


# --------------------------------
# LOAD DATASET
# --------------------------------

RECIPES_DF = pd.read_csv(CSV_PATH)

DATASET_FEATURES = np.load(FEATURE_PATH)


# --------------------------------
# LOAD RESNET50 FEATURE MODEL
# --------------------------------

base_model = ResNet50(weights="imagenet")

feature_model = Model(
    inputs=base_model.input,
    outputs=base_model.get_layer("avg_pool").output
)


# --------------------------------
# FEATURE EXTRACTION
# --------------------------------

def extract_feature(image):

    img = image.convert("RGB").resize((224, 224))

    x = np.array(img)
    x = np.expand_dims(x, axis=0)

    x = preprocess_input(x)

    feature = feature_model.predict(x, verbose=0)

    feature = feature.flatten()

    feature = feature / np.linalg.norm(feature)

    return feature


# --------------------------------
# FIND MOST SIMILAR IMAGE
# --------------------------------

def find_similar(feature):

    similarities = DATASET_FEATURES @ feature

    best_idx = np.argmax(similarities)

    best_score = similarities[best_idx]

    row = RECIPES_DF.iloc[best_idx]

    return row, float(best_score)


# --------------------------------
# PARSE INGREDIENTS
# --------------------------------

def parse_ingredients(raw):

    try:
        value = ast.literal_eval(str(raw))

        if isinstance(value, list):
            return value

    except:
        pass

    return [str(raw)]


# --------------------------------
# PARSE INSTRUCTIONS
# --------------------------------

def parse_instructions(raw):

    if raw is None:
        return []

    return [x.strip() for x in str(raw).split("\n") if x.strip()]


# --------------------------------
# GET REFERENCE IMAGE
# --------------------------------

def get_reference_image(img_name):

    base = os.path.splitext(img_name)[0]

    for ext in [".jpg", ".jpeg", ".png"]:

        path = os.path.join(IMAGE_FOLDER, base + ext)

        if os.path.exists(path):
            return path

    return None


# --------------------------------
# MAIN FUNCTION
# --------------------------------

def generate_recipe(image, image_name=None):

    feature = extract_feature(image)

    row, score = find_similar(feature)

    title = row["Title"]

    ingredients = parse_ingredients(row.get("Ingredients"))

    steps = parse_instructions(row.get("Instructions"))

    similarity = round(score * 100, 2)

    confidence = min(95, similarity)

    reference = get_reference_image(row.get("Image_Name", ""))

    return title, ingredients, steps, confidence, similarity, reference