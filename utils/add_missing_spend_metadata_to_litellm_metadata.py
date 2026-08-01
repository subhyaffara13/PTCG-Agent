
def add_missing_spend_metadata_to_litellm_metadata(
    litellm_metadata: dict, metadata: dict
) -> dict:
    """
    Helper to get litellm metadata for spend tracking

    PATCH for issue where both `litellm_metadata` and `metadata` are present in the kwargs
    and user_api_key values are in 'metadata'.
    """
    potential_spend_tracking_metadata_substring = "user_api_key"
    for key, value in metadata.items():
        if potential_spend_tracking_metadata_substring in key:
            litellm_metadata[key] = value
    return litellm_metadata

