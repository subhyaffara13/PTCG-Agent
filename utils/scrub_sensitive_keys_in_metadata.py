from typing import Optional

def scrub_sensitive_keys_in_metadata(litellm_params: Optional[dict]):
    if litellm_params is None:
        litellm_params = {}

    metadata = litellm_params.get("metadata", {}) or {}

    ## Extract provider-specific callable values (like langfuse_masking_function)
    ## Store them separately so only the intended logger can access them
    ## This prevents callables from leaking to other logging integrations
    if "langfuse_masking_function" in metadata:
        masking_fn = metadata.pop("langfuse_masking_function", None)
        if callable(masking_fn):
            litellm_params["_langfuse_masking_function"] = masking_fn
        litellm_params["metadata"] = metadata

    ## check user_api_key_metadata for sensitive logging keys
    cleaned_user_api_key_metadata = {}
    if "user_api_key_metadata" in metadata and isinstance(
        metadata["user_api_key_metadata"], dict
    ):
        for k, v in metadata["user_api_key_metadata"].items():
            if k == "logging":  # prevent logging user logging keys
                cleaned_user_api_key_metadata[k] = (
                    "scrubbed_by_litellm_for_sensitive_keys"
                )
            else:
                cleaned_user_api_key_metadata[k] = v

        metadata["user_api_key_metadata"] = cleaned_user_api_key_metadata
        litellm_params["metadata"] = metadata

    return litellm_params

