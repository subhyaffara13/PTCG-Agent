
def _get_or_create_proxy_metadata_bucket(
    request_data: Dict,
) -> tuple[Literal["metadata", "litellm_metadata"], dict]:
    """
    Return the proxy-internal metadata bucket for this request.

    Batch/file routes store proxy state in ``litellm_metadata`` so the OpenAI
    ``metadata`` field can remain provider-safe (string values only).
    """
    metadata_key = get_metadata_variable_name_from_kwargs(request_data)
    metadata_bucket = request_data.get(metadata_key)
    if not isinstance(metadata_bucket, dict):
        metadata_bucket = {}
        request_data[metadata_key] = metadata_bucket
    return metadata_key, metadata_bucket

