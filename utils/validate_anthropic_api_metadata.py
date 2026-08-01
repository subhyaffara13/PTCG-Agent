
def validate_anthropic_api_metadata(metadata: Optional[Dict] = None) -> Optional[Dict]:
    """
    Validate Anthropic API metadata - This is done to ensure only allowed `metadata` fields are passed to Anthropic API

    If there are any litellm specific metadata fields, use `litellm_metadata` key to pass them.
    """
    if metadata is None:
        return None
    anthropic_metadata_obj = AnthropicMetadata(**metadata)
    return anthropic_metadata_obj.model_dump(exclude_none=True)

