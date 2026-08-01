
def add_policy_sources_to_metadata(request_data: Dict, policy_sources: Dict[str, str]):
    """
    Store policy match reasons in metadata for x-litellm-policy-sources header.

    Args:
        request_data: The request data dict
        policy_sources: Map of policy_name -> matched_via reason
    """
    if not policy_sources:
        return
    _, _metadata = _get_or_create_proxy_metadata_bucket(request_data)
    existing = _metadata.get("policy_sources", {})
    if not isinstance(existing, dict):
        existing = {}
    existing.update(policy_sources)
    _metadata["policy_sources"] = existing

