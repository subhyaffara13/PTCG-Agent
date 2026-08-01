
def get_black_forest_labs_image_generation_config(
    model: str,
) -> BlackForestLabsImageGenerationConfig:
    """
    Get the appropriate image generation config for a Black Forest Labs model.

    Currently returns a single config class, but can be extended
    for model-specific configurations if needed.
    """
    return BlackForestLabsImageGenerationConfig()

