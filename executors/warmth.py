from PIL import Image
import numpy as np


def compute_warmth(image_path: str) -> float:
    image = Image.open(image_path).convert("RGB")
    arr = np.asarray(image).astype(np.float32) / 255.0

    red_mean = arr[:, :, 0].mean()
    blue_mean = arr[:, :, 2].mean()

    return float(red_mean - blue_mean)


def execute_warmth(original_image: str, edited_image: str, direction: str = "increase"):
    original_score = compute_warmth(original_image)
    edited_score = compute_warmth(edited_image)

    diff = edited_score - original_score
    threshold = 0.03

    if direction == "increase":
        passed = diff > threshold
    else:
        passed = diff < -threshold

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
