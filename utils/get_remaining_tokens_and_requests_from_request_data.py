
def get_remaining_tokens_and_requests_from_request_data(data: Dict) -> Dict[str, str]:
    """
    Helper function to return x-litellm-key-remaining-tokens-{model_group} and x-litellm-key-remaining-requests-{model_group}

    Returns {} when api_key + model rpm/tpm limit is not set

    """
    headers = {}
    _metadata = data.get("metadata", None) or {}
    model_group = get_model_group_from_request_data(data)

    # The h11 package considers "/" or ":" invalid and raise a LocalProtocolError
    h11_model_group_name = (
        model_group.replace("/", "-").replace(":", "-") if model_group else None
    )

    # Remaining Requests
    remaining_requests_variable_name = f"litellm-key-remaining-requests-{model_group}"
    remaining_requests = _metadata.get(remaining_requests_variable_name, None)
    if remaining_requests:
        headers[f"x-litellm-key-remaining-requests-{h11_model_group_name}"] = (
            remaining_requests
        )

    # Remaining Tokens
    remaining_tokens_variable_name = f"litellm-key-remaining-tokens-{model_group}"
    remaining_tokens = _metadata.get(remaining_tokens_variable_name, None)
    if remaining_tokens:
        headers[f"x-litellm-key-remaining-tokens-{h11_model_group_name}"] = (
            remaining_tokens
        )

    return headers

