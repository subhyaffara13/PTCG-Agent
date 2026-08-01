
def update_headers_with_filtered_beta(
    headers: dict,
    provider: str,
) -> dict:
    """
    Update headers dict by filtering and transforming anthropic-beta header values.
    Modifies the headers dict in place and returns it.

    Args:
        headers: Request headers dict (will be modified in place)
        provider: Provider name

    Returns:
        Updated headers dict
    """
    existing_beta = headers.get("anthropic-beta")
    if not existing_beta:
        return headers

    # Parse existing beta headers
    beta_values = [b.strip() for b in existing_beta.split(",") if b.strip()]

    # Filter and transform based on provider
    filtered_beta_values = filter_and_transform_beta_headers(
        beta_headers=beta_values,
        provider=provider,
    )

    # Update or remove the header
    if filtered_beta_values:
        headers["anthropic-beta"] = ",".join(filtered_beta_values)
    else:
        # Remove the header if no values remain
        headers.pop("anthropic-beta", None)

    return headers

