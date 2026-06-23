"""
Warmth executor.

This file measures image warmth by comparing the average red and blue values.
It checks whether the edited image becomes warmer than the original image.
"""

from PIL import Image
import numpy as np


def compute_warmth(image_path: str) -> float:
    # Load image and convert it to RGB
    image = Image.open(image_path).convert("RGB")

    # Convert image to a normalized NumPy array
    arr = np.asarray(image).astype(np.float32) / 255.0

    # Compute average red channel value
    red_mean = arr[:, :, 0].mean()

    # Compute average blue channel value
    blue_mean = arr[:, :, 2].mean()

    # Warmth score: higher red minus blue means warmer
    return float(red_mean - blue_mean)


def execute_warmth(original_image: str, edited_image: str, direction: str = "increase"):
    # Compute warmth score for the original image
    original_score = compute_warmth(original_image)

    # Compute warmth score for the edited image
    edited_score = compute_warmth(edited_image)

    # Difference between edited and original warmth
    diff = edited_score - original_score

    # Minimum required warmth change
    threshold = 0.03

    # Check whether warmth increased enough
    if direction == "increase":
        passed = diff > threshold
    else:
        passed = diff < -threshold

    # Return the module-level result
    return {
        "op": "Modify",
        "concept": "Warmth",
        "pass": passed,
        "original_score": original_score,
        "edited_score": edited_score,
        "diff": diff,
        "failure_type": "none" if passed else "insufficient warmth",
        "explanation": (
            "The edited image is warmer."
            if passed
            else "The edited image is not sufficiently warmer."
        ),
    }
