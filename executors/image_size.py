"""
Image size executor.

This file checks whether the edited image preserves the original image size.
It compares the width and height of the original and edited images.
"""

from PIL import Image


def execute_image_size(original_path: str, edited_path: str):
    # Open original and edited images
    original = Image.open(original_path)
    edited = Image.open(edited_path)

    # PIL size format is (width, height)
    original_size = original.size
    edited_size = edited.size

    # Pass only if width and height are exactly the same
    passed = original_size == edited_size

    # Decide failure type
    failure_type = "none" if passed else "image size changed"

    # Return module-level result
    return {
        "op": "Preserve",
        "concept": "ImageSize",
        "pass": passed,
        "original_size": original_size,
        "edited_size": edited_size,
        "failure_type": failure_type,
        "explanation": (
            "The image size is preserved."
            if passed
            else f"Image size changed from {original_size} to {edited_size}."
        ),
    }
