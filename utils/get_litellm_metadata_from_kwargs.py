
def get_litellm_metadata_from_kwargs(kwargs: dict):
    """
    Helper to get litellm metadata from all litellm request kwargs

    Return `litellm_metadata` if it exists, otherwise return `metadata`
    """
    litellm_params = kwargs.get("litellm_params", {})
    if litellm_params:
        metadata = litellm_params.get("metadata", {})
        litellm_metadata = litellm_params.get("litellm_metadata", {})
        if litellm_metadata and metadata:
            litellm_metadata = add_missing_spend_metadata_to_litellm_metadata(
                litellm_metadata, metadata
            )
        if litellm_metadata:
            return litellm_metadata
        elif metadata:
            return metadata

    return {}

