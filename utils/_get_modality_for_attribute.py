
def _get_modality_for_attribute(attribute_name: str) -> str:
    """
    Get the canonical modality type for a given attribute name.

    For example:
    - "image_processor" -> "image_processor"
    - "encoder_image_processor" -> "image_processor"
    - "text_tokenizer" -> "tokenizer"
    - "my_feature_extractor" -> "feature_extractor"
    """
    for modality in MODALITY_TO_AUTOPROCESSOR_MAPPING.keys():
        if modality in attribute_name:
            return modality
    raise ValueError(
        f"Cannot determine modality for attribute '{attribute_name}'. "
        f"Attribute name must contain one of: {list(MODALITY_TO_AUTOPROCESSOR_MAPPING.keys())}"
    )

