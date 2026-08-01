
def get_bedrock_image_edit_config_for_model(
    model: str,
) -> BaseImageEditConfig:
    """
    Return the correct Bedrock image-edit config for the model id.

    Same routing as ``BedrockImageEdit.get_config_class``: Stability edit models,
    Nova Canvas when marked in model_cost; otherwise raises ``ValueError``.
    """
    from litellm.llms.bedrock.image_edit.stability_transformation import (
        BedrockStabilityImageEditConfig,
    )

    if BedrockStabilityImageEditConfig._is_stability_edit_model(model):
        return BedrockStabilityImageEditConfig()
    if BedrockAmazonNovaCanvasImageEditConfig._is_nova_canvas_image_edit_model(model):
        return BedrockAmazonNovaCanvasImageEditConfig()
    raise ValueError(
        f"Unsupported Bedrock image-edit model: {model!r}. "
        "Use a stability.* image-edit model id or add supports_nova_canvas_image_edit "
        "in model_prices for this id."
    )

