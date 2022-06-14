from typing import Dict, Any
import cv2
from cv2 import dnn_superres
from cv2.dnn_superres import DnnSuperResImpl
import os
from pathlib import Path


WIDTH = 1200

def get_models() -> Dict:
    """Getting all available upscale models."""
    models = []
    models_folder = f"{Path(__file__).parent}/models/"
    models_list = os.listdir(models_folder)
    for model in models_list:
        model_name = model.split("_")[0]
        model_multiplier = int(model.split("_")[1].split(".")[0].replace("x", ""))
        sr = dnn_superres.DnnSuperResImpl_create()
        sr.readModel(models_folder + model)
        sr.setModel(model_name.lower(), model_multiplier)
        model_info = {
            "model": sr,
            "model_name": model_name,
            "model_multiplier": model_multiplier
        }
        models.append(model_info)
    
    return models



def upscale_img(model: DnnSuperResImpl, image, resize: bool = False):
    """Upscale given image.
        Args:
            model: Upscale model
            image: Given image
            resize: Whether to resize the image
        Returns:
            Upscaled image
    """
    # Upscale the image
    image = model.upsample(image)
    # Resize the image
    if resize:
        resize_ratio = WIDTH / image.shape[1]
        dim = (1200, int(image.shape[0] * resize_ratio))
        image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

    return image
