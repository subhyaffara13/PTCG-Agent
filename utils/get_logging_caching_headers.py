
def get_logging_caching_headers(request_data: Dict) -> Optional[Dict]:
    _metadata: Dict = {}
    metadata_bucket = request_data.get("metadata")
    litellm_metadata_bucket = request_data.get("litellm_metadata")
    if isinstance(metadata_bucket, dict):
        _metadata.update(metadata_bucket)
    if isinstance(litellm_metadata_bucket, dict):
        # Batch/file routes store proxy tracking in litellm_metadata while
        # user-facing metadata stays in metadata; merge both for headers.
        _metadata.update(litellm_metadata_bucket)
    headers = {}
    if "applied_guardrails" in _metadata:
        headers["x-litellm-applied-guardrails"] = ",".join(
            _metadata["applied_guardrails"]
        )

    if "applied_policies" in _metadata:
        headers["x-litellm-applied-policies"] = ",".join(_metadata["applied_policies"])

    if "policy_sources" in _metadata:
        sources = _metadata["policy_sources"]
        if isinstance(sources, dict) and sources:
            # Use ';' as delimiter — matched_via reasons may contain commas
            headers["x-litellm-policy-sources"] = "; ".join(
                f"{name}={reason}" for name, reason in sources.items()
            )

    if "semantic-similarity" in _metadata:
        headers["x-litellm-semantic-similarity"] = str(_metadata["semantic-similarity"])

    is_trusted_pillar_metadata = (
        _metadata.get(TRUSTED_PILLAR_RESPONSE_HEADERS_METADATA_KEY) is True
    )
    pillar_headers = _metadata.get("pillar_response_headers")
    if is_trusted_pillar_metadata and isinstance(pillar_headers, dict):
        headers.update(
            {
                key: str(value)
                for key, value in pillar_headers.items()
                if isinstance(key, str) and key.lower().startswith("x-pillar-")
            }
        )
    elif is_trusted_pillar_metadata and "pillar_flagged" in _metadata:
        headers["x-pillar-flagged"] = str(_metadata["pillar_flagged"]).lower()

    return headers

