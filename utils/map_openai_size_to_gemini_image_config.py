from typing import Dict, Optional

def map_openai_size_to_gemini_image_config(
    size: str, model: str
) -> Optional[Dict[str, str]]:
    dimensions = _parse_openai_image_size(size)
    if dimensions is None:
        return None

    width, height = dimensions
    image_config = {
        "aspectRatio": _map_dimensions_to_gemini_aspect_ratio(width, height)
    }
    image_size = _map_dimensions_to_gemini_image_size(width, height)
    if is_gemini_image_model(model):
        if supports_gemini_image_size(model):
            image_config["imageSize"] = image_size
    else:
        image_config["imageSize"] = image_size
    return image_config

