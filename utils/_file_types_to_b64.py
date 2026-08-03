import os
from typing import Optional

def _file_types_to_b64(image: Optional[FileTypes]) -> str:
    """Encode OpenAI image input to base64 string for Nova Canvas."""
    if image is None:
        raise ValueError("Nova Canvas image edit requires an image input")
    if hasattr(image, "read") and callable(getattr(image, "read", None)):
        if hasattr(image, "seek"):
            image.seek(0)  # type: ignore[union-attr]
        image_bytes = image.read()  # type: ignore[union-attr]
        return base64.b64encode(image_bytes).decode("utf-8")
    if isinstance(image, bytes):
        return base64.b64encode(image).decode("utf-8")
    if isinstance(image, str):
        return image
    if isinstance(image, os.PathLike):
        with open(image, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    if isinstance(image, tuple):
        raise ValueError(
            "Nova Canvas image edit does not support tuple FileTypes. "
            "Pass a file-like object, bytes, or a base64-encoded string."
        )
    return base64.b64encode(bytes(image)).decode("utf-8")  # type: ignore[arg-type]

