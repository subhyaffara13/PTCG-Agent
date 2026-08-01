
def get_azure_ai_image_edit_config(model: str) -> BaseImageEditConfig:
    """
    Get the appropriate image edit config for an Azure AI model.

    - MAI models use /mai/v1/images/edits with multipart form data and size
    - FLUX 2 models use JSON with base64 image
    - FLUX 1 models use multipart/form-data
    """
    if AzureFoundryMAIImageGenerationConfig.is_mai_model(model):
        return AzureFoundryMAIImageEditConfig()

    # Check if it's a FLUX 2 model
    if AzureFoundryFluxImageGenerationConfig.is_flux2_model(model):
        return AzureFoundryFlux2ImageEditConfig()

    # Default to FLUX 1 config for other FLUX models
    model_normalized = model.lower().replace("-", "").replace("_", "")
    if model_normalized == "" or "flux" in model_normalized:
        return AzureFoundryFluxImageEditConfig()

    raise ValueError(f"Model {model} is not supported for Azure AI image editing.")

