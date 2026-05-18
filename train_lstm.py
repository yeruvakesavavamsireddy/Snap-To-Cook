from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense

model = Sequential([
    Embedding(input_dim=5000, output_dim=256),
    LSTM(256),
    Dense(5000, activation="softmax")
])

model.compile(loss="categorical_crossentropy", optimizer="adam")
model.save("models/recipe_generator.h5")
