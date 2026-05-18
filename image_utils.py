import numpy as np
from PIL import Image

def preprocess_image(image):
    image = image.resize((224, 224))
    image = np.array(image) / 255.0

    if image.shape[-1] != 3:
        image = image[:, :, :3]

    return image.reshape(1, 224, 224, 3)
