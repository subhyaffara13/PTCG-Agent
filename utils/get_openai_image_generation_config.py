
def get_openai_image_generation_config(model: str) -> BaseImageGenerationConfig:
    if model.startswith("dall-e-2") or model == "":  # empty model is dall-e-2
        return DallE2ImageGenerationConfig()
    elif model.startswith("dall-e-3"):
        return DallE3ImageGenerationConfig()
    else:
        return GPTImageGenerationConfig()

