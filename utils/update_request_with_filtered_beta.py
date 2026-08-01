
def update_request_with_filtered_beta(
    headers: dict,
    request_data: dict,
    provider: str,
) -> tuple[dict, dict]:
    """
    Update both headers and request body beta fields based on provider support.
    Modifies both dicts in place and returns them.

    Args:
        headers: Request headers dict (will be modified in place)
        request_data: Request body dict (will be modified in place)
        provider: Provider name

    Returns:
        Tuple of (updated headers, updated request_data)
    """
    headers = update_headers_with_filtered_beta(headers=headers, provider=provider)

    existing_body_betas = request_data.get("anthropic_beta")
    if not existing_body_betas:
        return headers, request_data

    filtered_body_betas = filter_and_transform_beta_headers(
        beta_headers=existing_body_betas,
        provider=provider,
    )

    if filtered_body_betas:
        request_data["anthropic_beta"] = filtered_body_betas
    else:
        request_data.pop("anthropic_beta", None)

    return headers, request_data

