
def _normalize_video_parameters(parameters: dict) -> dict:
    """Map HF inference-client conventions onto Together's video API parameter names."""
    parameters = filter_none(parameters)
    if "num_inference_steps" in parameters:
        parameters["steps"] = parameters.pop("num_inference_steps")
    if "target_size" in parameters:
        target_size = parameters.pop("target_size")
        if "width" in target_size:
            parameters["width"] = target_size["width"]
        if "height" in target_size:
            parameters["height"] = target_size["height"]
    return parameters

