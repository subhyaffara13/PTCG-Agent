
def get_azure_image_generation_config(model: str) -> BaseImageGenerationConfig:
    model = model.lower()
    model = model.replace("-", "")
    model = model.replace("_", "")
    if model == "" or "dalle2" in model:  # empty model is dall-e-2
        return AzureDallE2ImageGenerationConfig()
    elif "dalle3" in model:
        return AzureDallE3ImageGenerationConfig()
    elif AzureFoundryMAIImageGenerationConfig.is_mai_model(model):
        return AzureFoundryMAIImageGenerationConfig()
    else:
        verbose_logger.debug(
            f"Using AzureGPTImageGenerationConfig for model: {model}. This follows the gpt-image model format."
        )
        return AzureGPTImageGenerationConfig()

