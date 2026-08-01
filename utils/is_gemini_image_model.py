
def is_gemini_image_model(model: str) -> bool:
    base_model = model.split("/", 1)[-1]
    return "gemini" in base_model

