from typing import Any, Dict

def get_gemini_image_generation_config(
    model: str,
    optional_params: Dict[str, Any],
) -> Dict[str, Any]:
    generation_config: Dict[str, Any] = {"response_modalities": ["IMAGE", "TEXT"]}

    image_config: Dict[str, Any] = {}
    if isinstance(optional_params.get("imageConfig"), dict):
        image_config.update(optional_params["imageConfig"])

    if not supports_gemini_image_size(model):
        image_config.pop("imageSize", None)

    if image_config:
        generation_config["imageConfig"] = image_config

    candidate_count = next(
        (
            optional_params[key]
            for key in ("candidateCount", "candidate_count", "sampleCount", "n")
            if optional_params.get(key) is not None
        ),
        None,
    )
    if candidate_count is not None:
        generation_config["candidateCount"] = candidate_count

    return generation_config


def get_gemini_image_generation_config(model: str) -> BaseImageGenerationConfig:
    return GoogleImageGenConfig()

