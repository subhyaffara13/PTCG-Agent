
def supports_gemini_image_size(model: str) -> bool:
    try:
        model_info = litellm.get_model_info(model=model)
        value = model_info.get("supports_image_size")
        if value is not None:
            return bool(value)
    except Exception:
        pass
    return "2.5-flash" not in model

