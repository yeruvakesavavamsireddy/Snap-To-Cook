import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Model

base_model = ResNet50(weights="imagenet", include_top=False)
x = tf.keras.layers.GlobalAveragePooling2D()(base_model.output)

model = Model(inputs=base_model.input, outputs=x)
model.save("models/cnn_encoder.h5")
