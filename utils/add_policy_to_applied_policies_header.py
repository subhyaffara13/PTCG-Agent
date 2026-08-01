
def add_policy_to_applied_policies_header(
    request_data: Dict, policy_name: Optional[str]
):
    """
    Add a policy name to the applied_policies list in request metadata.

    This is used to track which policies were applied to a request,
    similar to how applied_guardrails tracks guardrails.
    """
    if policy_name is None:
        return
    _, _metadata = _get_or_create_proxy_metadata_bucket(request_data)
    if "applied_policies" in _metadata:
        if policy_name not in _metadata["applied_policies"]:
            _metadata["applied_policies"].append(policy_name)
    else:
        _metadata["applied_policies"] = [policy_name]

