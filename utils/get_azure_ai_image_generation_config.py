
def get_azure_ai_image_generation_config(model: str) -> BaseImageGenerationConfig:
    model = model.lower()
    model = model.replace("-", "")
    model = model.replace("_", "")
    if model == "" or "dalle2" in model:  # empty model is dall-e-2
        return AzureFoundryDallE2ImageGenerationConfig()
    elif "dalle3" in model:
        return AzureFoundryDallE3ImageGenerationConfig()
    elif AzureFoundryMAIImageGenerationConfig.is_mai_model(model):
        return AzureFoundryMAIImageGenerationConfig()
    elif "flux" in model:
        return AzureFoundryFluxImageGenerationConfig()
    else:
        verbose_logger.debug(
            f"Using AzureGPTImageGenerationConfig for model: {model}. This follows the gpt-image-1 model format."
        )
        return AzureFoundryGPTImageGenerationConfig()

