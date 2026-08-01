
def get_fal_ai_image_generation_config(model: str) -> BaseImageGenerationConfig:
    """
    Get the appropriate Fal AI image generation configuration based on the model.

    Args:
        model: The Fal AI model name (e.g., "fal-ai/imagen4/preview", "fal-ai/recraft/v3/text-to-image")

    Returns:
        The appropriate configuration class for the specified model
    """
    model_lower = model.lower()

    # Map model names to their corresponding configuration classes
    if "nano-banana" in model_lower or "gemini-25-flash-image" in model_lower:
        return FalAINanoBananaConfig()
    elif "imagen4" in model_lower or "imagen-4" in model_lower:
        return FalAIImagen4Config()
    elif "recraft" in model_lower:
        return FalAIRecraftV3Config()
    elif "bria" in model_lower:
        return FalAIBriaConfig()
    elif "flux-pro" in model_lower:
        if "ultra" in model_lower:
            return FalAIFluxProV11UltraConfig()
        return FalAIFluxProV11Config()
    elif (
        "flux/schnell" in model_lower
        or "flux-schnell" in model_lower
        or "schnell" in model_lower
    ):
        return FalAIFluxSchnellConfig()
    elif "bytedance/seedream" in model_lower:
        return FalAIBytedanceSeedreamV3Config()
    elif "bytedance/dreamina" in model_lower:
        return FalAIBytedanceDreaminaV31Config()
    elif "ideogram" in model_lower:
        return FalAIIdeogramV3Config()
    elif "stable-diffusion" in model_lower:
        return FalAIStableDiffusionConfig()

    # Default to generic Fal AI configuration
    return FalAIImageGenerationConfig()

