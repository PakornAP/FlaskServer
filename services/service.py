import tensorflow as tf
import os
import numpy as np
def Helloname(name : str):
    return f"hello {name}"

def MaskDetection(img) -> bool:
    model_path = os.path.abspath("./models/model.h5")
    try:
        mask_detector = tf.keras.models.load_model(model_path,compile=False)
    except OSError or ValueError or Exception as e:
        print(f"Error: {e}. Load model failed")
    face = tf.keras.applications.mobilenet_v2.preprocess_input(img)
    face = np.expand_dims(face, axis=0)
    mask, withoutMask = mask_detector.predict(face)[0]
    print(f"mask {mask} nomask {withoutMask}")
    return True if mask > withoutMask else False