
def get_modelscope_image_generation_config(
    model: str,
) -> BaseImageGenerationConfig:
    """
    Get the ModelScope config for image generation.

    Args:
        model: The model name (e.g., "modelscope/Qwen/Qwen-Image-Edit")

    Returns:
        BaseImageGenerationConfig instance for ModelScope
    """
    return ModelScopeImageGenerationConfig()

