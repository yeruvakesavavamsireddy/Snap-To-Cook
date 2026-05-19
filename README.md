
---

## Introduction

Snap To Cook is an intelligent deep learning-based application designed to generate recipes from food
images. Instead of searching recipes by dish name, users can simply upload a food image, and the system
predicts the dish and generates the recipe title, ingredients, and cooking steps. It uses CNN for image
feature extraction and LSTM for recipe text generation. The application is developed using Python,
TensorFlow, and Streamlit, providing a simple and real-time web interface.



---


## Key Contributions


* **CNN-LSTM based recipe generation**
* **Food image recognition with similarity scoring**
* **Multi-label ingredient prediction**
* **Voice assistant support**
* **Real-time web-based application**



---


## Problem Statement

* **Users may not know the dish name**
* **Manual recipe search is time-consuming**
* **Existing systems lack image-based recognition**
* **Recipes online may be unclear or inconsistent**
* **No integrated system combining image + text generation**




---


## Objectives



* **Develop an AI system to generate recipes from food images.**
* **Identify food items and ingredients using CNN.**
* **Generate recipe text using LSTM.**
* **Provide real-time user-friendly interface.**
* **Evaluate performance using standard metrics.**




---

## System Architecture & Methodology

Our pipeline is engineered for speed, accuracy, and real-time execution:

1. **Input:** User uploads a food image via the Streamlit interface.
2. **Preprocessing:** The image is resized to `224x224` and normalized.
3. **Feature Extraction:** A Convolutional Neural Network (ResNet50) extracts high-dimensional visual features.
4. **Prediction:** A Multi-Label Classification model predicts the exact ingredients.
5. **Generation:** An LSTM language model sequences the recipe title and cooking instructions.
6. **Matching:** Cosine similarity compares the input against a vast dataset.
7. **Output:** A complete, beautifully formatted recipe is served to the user.

---

## Technology Stack

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white" />
 
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white" />
</p>

* **Model Development:** TensorFlow
* **Architectures:** ResNet50 (CNN), LSTM, Multi-label Classification
* **Optimization:** Adam Optimizer, Tokenization strategies
* **Frontend UI:** Streamlit

---

## Performance & Results

We evaluate our models with the rigor expected of global-scale products. Based on an 80:20 train-test split of the Kaggle Recipe1M dataset:

* **CNN Feature Extraction:** `91%` Training Accuracy | `88%` Validation Accuracy
* **Ingredient Prediction:** `84%` Overall Accuracy | `F1-Score: 0.82`
* **LSTM Text Generation:** `82%` Validation Accuracy
* **User Impact:** 90% user-friendly rating, with a **60% reduction** in manual search time.

---

## The Future Horizon

Great products are never finished; they simply evolve. Our roadmap for SnapToCook includes:

* **Real-Time Camera Integration:** Direct food scanning for instantaneous results.
* **Multilingual Support:** Making recipes globally accessible with localized voice and text.
* **Advanced Transformers:** Upgrading from LSTM to state-of-the-art Transformer models for even deeper contextual generation.
* **Personalization & Health:** Calorie estimation, nutritional analysis, and dietary-specific ingredient substitutions.
* **Cloud & Mobile Deployment:** Scaling infrastructure for a dedicated mobile ecosystem.

---



## Conclusion


Snap To Cook provides an intelligent and efficient solution for generating cooking recipes from food
images using deep learning. By combining computer vision and natural language processing, the
application eliminates the need for manual recipe searches and enhances the cooking experience. This
project demonstrates the effective use of AI in real-world applications and can be further extended by
adding nutritional analysis, multiple recipe suggestions, and real-time camera integration.


---
