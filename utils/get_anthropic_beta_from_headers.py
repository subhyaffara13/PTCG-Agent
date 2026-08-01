
def get_anthropic_beta_from_headers(headers: dict) -> List[str]:
    """
    Extract anthropic-beta header values and convert them to a list.
    Supports both JSON array format and comma-separated values from user headers.

    Used by both converse and invoke transformations for consistent handling
    of anthropic-beta headers that should be passed to AWS Bedrock.

    Args:
        headers (dict): Request headers dictionary

    Returns:
        List[str]: List of anthropic beta feature strings, empty list if no header
    """
    anthropic_beta_header = headers.get("anthropic-beta")
    if not anthropic_beta_header:
        return []

    # If it's already a list, return it
    if isinstance(anthropic_beta_header, list):
        return anthropic_beta_header

    # Try to parse as JSON array first (e.g., '["interleaved-thinking-2025-05-14", "claude-code-20250219"]')
    if isinstance(anthropic_beta_header, str):
        anthropic_beta_header = anthropic_beta_header.strip()
        if anthropic_beta_header.startswith("[") and anthropic_beta_header.endswith(
            "]"
        ):
            try:
                parsed = json.loads(anthropic_beta_header)
                if isinstance(parsed, list):
                    return [str(beta).strip() for beta in parsed]
            except json.JSONDecodeError:
                pass  # Fall through to comma-separated parsing

        # Fall back to comma-separated values
        return [beta.strip() for beta in anthropic_beta_header.split(",")]

    return []

