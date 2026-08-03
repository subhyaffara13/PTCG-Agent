import json
from typing import Any, Dict, Optional

def map_openai_image_params_to_gemini(
    params: Dict[str, Any],
    model: str,
    supported_params: Sequence[str],
    optional_params: Optional[Dict[str, Any]] = None,
    parse_image_config_string: bool = False,
) -> Dict[str, Any]:
    optional_params = optional_params or {}
    filtered_params = {
        key: value for key, value in params.items() if key in supported_params
    }

    mapped_params: Dict[str, Any] = {}

    if "n" in filtered_params and "n" not in optional_params:
        mapped_params["sampleCount"] = filtered_params["n"]

    if "size" in filtered_params and "size" not in optional_params:
        image_config = map_openai_size_to_gemini_image_config(
            filtered_params["size"],
            model,
        )
        if image_config is not None:
            if is_gemini_image_model(model):
                mapped_params["imageConfig"] = image_config
            else:
                mapped_params["aspectRatio"] = image_config["aspectRatio"]
                if "imageSize" in image_config:
                    mapped_params["imageSize"] = image_config["imageSize"]

    image_config_param = filtered_params.get("imageConfig")
    if isinstance(image_config_param, str) and parse_image_config_string:
        try:
            image_config_param = json.loads(image_config_param)
        except json.JSONDecodeError as exc:
            raise litellm.UnsupportedParamsError(
                model=model,
                message="`imageConfig` must be valid JSON when provided as a string.",
            ) from exc
    if isinstance(image_config_param, dict):
        mapped_params["imageConfig"] = image_config_param

    for key, value in filtered_params.items():
        if (
            key not in ("n", "size", "imageConfig", "tools", "web_search_options")
            and key not in optional_params
        ):
            mapped_params[key] = value

    return mapped_params

