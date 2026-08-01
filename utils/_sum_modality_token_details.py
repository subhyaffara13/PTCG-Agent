
def _sum_modality_token_details(
    usage_metadata: dict, *details_keys: str
) -> ImageUsageInputTokensDetails:
    tokens_details = ImageUsageInputTokensDetails(
        image_tokens=0,
        text_tokens=0,
    )

    for details in _get_modality_token_details(usage_metadata, *details_keys):
        if isinstance(details, dict):
            modality = str(details.get("modality", "")).upper()
            token_count = _get_token_count(details)
            if modality == "TEXT":
                tokens_details.text_tokens += token_count
            elif modality == "IMAGE":
                tokens_details.image_tokens += token_count

    return tokens_details

